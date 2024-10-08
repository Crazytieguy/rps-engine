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

    def handle_results(self, *, my_action, their_action, my_payoff, match_clock):
        '''
        Called after a round. Called NUM_ROUNDS times.
        '''
        
        self.history.append(Turn(my_action, their_action))
        self.my_profit += my_payoff

    def get_action(self, *, match_clock):
        '''
        Where the magic happens. Called when the engine needs an action from
        your bot. Called NUM_ROUNDS times.

        Returns a RockAction(), PaperAction(), or ScissorsAction().
        '''
        if self.my_profit < -20 or len(self.history) < 4:
            return self.random_action()
    
        if (action := self.counter_copycat()) is not None:
            return action
        if (action := self.counter_simple_countering()) is not None:
            return action
        if (action := self.counter_deterministic_cycle()) is not None:
            return action
        if (action := self.counter_full_pattern_big()) is not None:
            return action
        if (action := self.counter_their_pattern_big()) is not None:
            return action
        if (action := self.counter_biased()) is not None:
            return action
        if (action := self.counter_full_pattern_small()) is not None:
            return action
        if (action := self.counter_their_pattern_small()) is not None:
            return action
        return self.random_action()

    def random_action(self):
        return random.choice([RockAction(), PaperAction(), ScissorsAction()])

    def counter_biased(self):
        their_action_counter = Counter([turn.their_action for turn in self.history])
        their_action_ratios = {action: count / len(self.history) for action, count in their_action_counter.items()}
        max_ratio = max(their_action_ratios.items(), key=lambda x: x[1])
        if max_ratio[1] > 0.38:
            return counter(max_ratio[0])
        return None
    
    def counter_copycat(self):
        for i in range(1, len(self.history) - 1):
            if type(self.history[i].their_action) != type(self.history[i-1].my_action):
                return None
        return counter(self.history[-1].my_action)
        

    def counter_simple_countering(self):
        for i in range(1, len(self.history) - 1):
            if type(self.history[i].their_action) != type(counter(self.history[i-1].my_action)):
                return None
        my_last_action = self.history[-1].my_action
        return counter(counter(my_last_action))


    def counter_full_pattern_small(self):
        for pattern_length in range(7, 2, -1):
            if len(self.history) <= pattern_length:
                continue
            pattern = self.history[-pattern_length:]
            for start in range(len(self.history) - pattern_length - 1, -1, -1):
                if self.history[start:start+pattern_length] == pattern:
                    their_next_action = self.history[start+pattern_length].their_action
                    return counter(their_next_action)
        return None


    def counter_full_pattern_big(self):
        for pattern_length in range(20, 7, -1):
            if len(self.history) <= pattern_length:
                continue
            pattern = self.history[-pattern_length:]
            for start in range(len(self.history) - pattern_length - 1, -1, -1):
                if self.history[start:start+pattern_length] == pattern:
                    their_next_action = self.history[start+pattern_length].their_action
                    return counter(their_next_action)
        return None
    
    def counter_deterministic_cycle(self):
        for cycle_turns in range(1, int(len(self.history) // 2)):
            is_cycle = True
            for i in range(cycle_turns):
                if not is_cycle:
                    break
                action = self.history[i].their_action
                for j in range(i + cycle_turns, len(self.history), cycle_turns):
                    if type(self.history[j].their_action) != type(action):
                        is_cycle = False
                        break
            if is_cycle:
                their_next_action = self.history[len(self.history) % cycle_turns].their_action
                return counter(their_next_action)
        return None

    def counter_their_pattern_small(self):
        for pattern_length in range(7, 2, -1):
            if len(self.history) <= pattern_length:
                continue
            pattern = [t.their_action for t in self.history[-pattern_length:]]
            for start in range(len(self.history) - pattern_length - 1, -1, -1):
                if [t.their_action for t in  self.history[start:start+pattern_length]] == pattern:
                    their_next_action = self.history[start+pattern_length].their_action
                    return counter(their_next_action)
        return None

    def counter_their_pattern_big(self):
        for pattern_length in range(20, 7, -1):
            if len(self.history) <= pattern_length:
                continue
            pattern = [t.their_action for t in self.history[-pattern_length:]]
            for start in range(len(self.history) - pattern_length - 1, -1, -1):
                if [t.their_action for t in  self.history[start:start+pattern_length]] == pattern:
                    their_next_action = self.history[start+pattern_length].their_action
                    return counter(their_next_action)
        return None


def counter(action):
    if isinstance(action, RockAction):
        return PaperAction()
    elif isinstance(action, PaperAction):
        return ScissorsAction()
    elif isinstance(action, ScissorsAction):
        return RockAction()
    return None


@dataclass(frozen=True)
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
