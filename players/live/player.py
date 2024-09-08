'''
Simple example bot, written in Python.
'''
from skeleton.actions import RockAction, PaperAction, ScissorsAction
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
from collections import Counter
from dataclasses import dataclass

import random


class Player(Bot):
    '''
    A bot for playing Rock-Paper-Scissors.
    '''

    history: list["Turn"]

    def __init__(self):
        '''
        Called when a new matchup starts. Called exactly once.
        '''
        
        self.my_profit = 0
        self.history = []
        self.their_action_counter = Counter()

    def handle_results(self, *, my_action, their_action, my_payoff, match_clock):
        '''
        Called after a round. Called NUM_ROUNDS times.
        '''
        
        self.history.append(Turn(my_action, their_action))
        self.my_profit += my_payoff
        self.their_action_counter[their_action] += 1

    def get_action(self, *, match_clock):
        '''
        Where the magic happens. Called when the engine needs an action from
        your bot. Called NUM_ROUNDS times.

        Returns a RockAction(), PaperAction(), or ScissorsAction().
        '''
        if self.my_profit < -20 or not self.history:
            return self.random_action()
    
        if (action := self.counter_sequence()) is not None:
            return action
        if (action := self.counter_copycat()) is not None:
            return action
        if (action := self.counter_simple_countering()) is not None:
            return action
        if (action := self.counter_biased()) is not None:
            return action
        return self.random_action()

    def random_action(self):
        return random.choice([RockAction(), PaperAction(), ScissorsAction()])


    def counter_sequence(self):
        if len(self.history) < 5:
            return None
        last_5_set = {turn.their_action for turn in self.history[-5:]}
        match last_5_set:
            case ConstantSets.ROCK_ONLY:
                return PaperAction()
            case ConstantSets.PAPER_ONLY:
                return ScissorsAction()
            case ConstantSets.SCISSORS_ONLY:
                return RockAction()
            case _:
                return None

    def counter_biased(self):
        their_action_ratios = {action: count / len(self.history) for action, count in self.their_action_counter.items()}
        max_ratio = max(their_action_ratios.items(), key=lambda x: x[1])
        if max_ratio[1] > 0.4:
            if isinstance(max_ratio[0], RockAction):
                return PaperAction()
            elif isinstance(max_ratio[0], PaperAction):
                return ScissorsAction()
            elif isinstance(max_ratio[0], ScissorsAction):
                return RockAction()
        return None
    
    def counter_copycat(self):
        if len(self.history) < 5:
            return None
        for i in range(4):
            if type(self.history[-i-1].their_action) != type(self.history[-i-2].my_action):
                return None
        if isinstance(self.history[-1].my_action, RockAction):
            return PaperAction()
        elif isinstance(self.history[-1].my_action, PaperAction):
            return ScissorsAction()
        elif isinstance(self.history[-1].my_action, ScissorsAction):
            return RockAction()
        

    def counter_simple_countering(self):
        if len(self.history) < 5:
            return None
        for i in range(4):
            if isinstance(self.history[-i-2].my_action, RockAction) and not isinstance(self.history[-i-1].their_action, PaperAction):
                return None
            if isinstance(self.history[-i-2].my_action, PaperAction) and not isinstance(self.history[-i-1].their_action, ScissorsAction):
                return None
            if isinstance(self.history[-i-2].my_action, ScissorsAction) and not isinstance(self.history[-i-1].their_action, RockAction):
                return None
        my_last_action = self.history[-1].my_action
        if isinstance(my_last_action, RockAction):
            return ScissorsAction()
        elif isinstance(my_last_action, PaperAction):
            return RockAction()
        elif isinstance(my_last_action, ScissorsAction):
            return PaperAction()


@dataclass
class Turn:
    my_action: RockAction | PaperAction | ScissorsAction
    their_action: RockAction | PaperAction | ScissorsAction


class ConstantSets:
    EMPTY = set()
    ROCK_ONLY = set([RockAction()])
    PAPER_ONLY = set([PaperAction()])
    SCISSORS_ONLY = set([ScissorsAction()])


if __name__ == '__main__':
    run_bot(Player(), parse_args())
