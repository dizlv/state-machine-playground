import random
import logging
import enum

from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FSM:
    def __init__(self):
        self._stack = deque()

    def update(self):
        try:
            state_function = self.pop_state()

        except IndexError:
            raise StopActionException

        else:
            state_function.run()

    def pop_state(self):
        return self._stack.popleft()

    def push_state(self, state):
        try:
            is_same_action = self.state == state

        except IndexError:
            self._stack.append(state)

        else:
            if not is_same_action:
                self._stack.append(state)

    @property
    def state(self):
        return self._stack[-1]


class Ant:
    def __init__(self, location):
        self.brain = FSM()

        self.location = location
        self.leaves = 0

    def perform_action(self, action):
        self.brain.push_state(action)


class StopActionException(Exception):
    pass


class Locations(enum.Enum):
    HOME = 1
    FOREST = 2


class AntAction:
    def __init__(self, instance: Ant):
        self.instance = instance

    def run(self):
        raise NotImplementedError


class FindLeafAction(AntAction):
    def collect_leaf(self):
        self.instance.leaves += 1

    def seek_leaves(self):
        while True:
            enemy_spotted = random.choice([True, False])

            logger.info('Looking for leaves.')

            found_leaf = random.choice([True, False])

            if found_leaf:
                logger.info('Leaf found.')

                if enemy_spotted:
                    logger.info('Enemy is protecting leaf. Going back home.')

                    break

                self.collect_leaf()

    def run(self):
        if self.instance.location == Locations.FOREST:
            return self.seek_leaves()

        else:
            logger.info('Ant should be in forest.')

            raise StopActionException


class GoHomeAction(AntAction):
    def run(self):
        if self.instance.location != Locations.HOME:
            logger.info('Going home.')

        else:
            logger.info('Ant is already at home.')

            raise StopActionException


class GoForestAction(AntAction):
    def run(self):
        if self.instance.location != Locations.FOREST:
            logger.info('Going to the forest.')

            self.instance.location = Locations.FOREST

        else:
            logger.info('Ant is already in forest.')

            raise StopActionException


if __name__ == '__main__':
    ant = Ant(location=Locations.HOME)

    ant.perform_action(action=GoForestAction(ant))
    ant.perform_action(action=FindLeafAction(ant))

    while True:
        try:
            ant.brain.update()

        except StopActionException:
            logger.info(f'Leaves collected: {ant.leaves}')

            break

