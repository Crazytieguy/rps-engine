'''
Simple example bot, written in Python.
'''
from skeleton.actions import RockAction, PaperAction, ScissorsAction
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
from collections import Counter

import random


class Player(Bot):
    '''
    A bot for playing Rock-Paper-Scissors.
    '''

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
        
        self.history.append((my_action, their_action))
        self.my_profit += my_payoff
        self.their_action_counter[their_action] += 1

    def get_action(self, *, match_clock):
        '''
        Where the magic happens. Called when the engine needs an action from
        your bot. Called NUM_ROUNDS times.

        Returns a RockAction(), PaperAction(), or ScissorsAction().
        '''
        if self.my_profit < -20 or not self.history:
            return random.choice([RockAction(), PaperAction(), ScissorsAction()])
    
        if (action := self.counter_sequence()) is not None:
            return action
        if (action := self.counter_biased()) is not None:
            return action
        if (action := self.counter_counter_action()) is not None:
            return action


    def counter_sequence(self):
        if len(self.history) < 5:
            return None
        last_5_set = {action for _, action in self.history[-5:]}
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
    
    def counter_counter_action(self):
        action = self.history[-1][0]
        if isinstance(action, RockAction):
            return ScissorsAction()
        elif isinstance(action, PaperAction):
            return RockAction()
        elif isinstance(action, ScissorsAction):
            return PaperAction()



class ConstantSets:
    EMPTY = set()
    ROCK_ONLY = set([RockAction()])
    PAPER_ONLY = set([PaperAction()])
    SCISSORS_ONLY = set([ScissorsAction()])


if __name__ == '__main__':
    run_bot(Player(), parse_args())
