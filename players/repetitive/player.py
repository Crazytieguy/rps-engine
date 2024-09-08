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
        actions = [RockAction(), RockAction(), PaperAction(), PaperAction(), ScissorsAction(), ScissorsAction()]
        return actions[len(self.history) % len(actions)]

    def random_action(self):
        return random.choice([RockAction(), PaperAction(), ScissorsAction()])


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
