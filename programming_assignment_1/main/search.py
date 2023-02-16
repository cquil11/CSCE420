# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import time
import util
import os
import heapq                # Python's PQ implementation


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def breadth_first_search(problem, a=None):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = []
    start_state = problem.get_start_state()

    if problem.is_goal_state(start_state):
        return visited

    frontier = util.Queue()
    frontier.push((start_state, []))
    visited.append(start_state)

    while not frontier.is_empty():
        current, path = frontier.pop()

        if problem.is_goal_state(current):
            return path

        for neighbor, action, cost in problem.get_successors(current):
            if neighbor not in visited:
                visited.append(neighbor)
                next_step = path + [action]
                frontier.push((neighbor, next_step))


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = []
    start_state = problem.get_start_state()

    if problem.is_goal_state(start_state):
        return visited

    frontier = util.PriorityQueue()
    frontier.push((start_state, [], 0), 0)

    while not frontier.is_empty():
        current, path, current_cost = frontier.pop()
        # print(len(path))

        if current not in visited:
            visited.append(current)

            if problem.is_goal_state(current):
                # print(path)
                return path

            for neighbor, action, new_cost in problem.get_successors(current):
                next_step = path + [action]
                priority = current_cost + new_cost
                frontier.push((neighbor, next_step, priority), priority)


#
# heuristics
#
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)


def null_heuristic(state, problem=None):
    return 0


def heuristic1(state, problem=None):
    from search_agents import FoodSearchProblem
    #
    # heuristic for the find-the-goal problem
    #
    if isinstance(problem, SearchProblem):
        # data
        pacman_x, pacman_y = state
        goal_x, goal_y = problem.goal

        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)

        optimisitic_number_of_steps_to_goal = 0
        return optimisitic_number_of_steps_to_goal
    #
    # traveling-salesman problem (collect multiple food pellets)
    #
    elif isinstance(problem, FoodSearchProblem):
        # the state includes a grid of where the food is (problem isn't ter)
        position, food_grid = state
        pacman_x, pacman_y = position

        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)

        optimisitic_number_of_steps_to_goal = 0
        return optimisitic_number_of_steps_to_goal


def a_star_search(problem, heuristic=heuristic1):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # A list of total moves for Pacman to consume all food particles
    visited = []
    start_state = problem.get_start_state()

    # To be pedantic, this code is included. However, in the case where the starting
    # grid has no food particles to eat, the program would terminate here.
    if problem.is_goal_state(start_state):
        return visited

    # Use the already implemented PQ data structure provided in util.py and push the
    # triple which represents a (state, path to state, g(n) A.K.A. depth)
    frontier = util.PriorityQueue()
    frontier.push((start_state, [], 0), 0)

    # Run this loop until there are no more nodes to check in the PQ
    while not frontier.is_empty():
        current, path, current_cost = frontier.pop()

        # See observation below...
        if current not in visited:
            visited.append(current)

            # If the goal state is reached (i.e., all food has been eaten), then return
            # the path of actions that Pacman should take
            if problem.is_goal_state(current):
                print(path)
                return path

            # Otherwise, iterate through each neighbor of the current node, store the 
            # move it would take to get there and add it to the end of the total path of actions.
            # Then, calculate the depth (g(n)) by adding the next cost to the current cost.
            # Calculate the heuristic (h(n)) on the neighbor. Finally, add h and g up and push
            # the neighbor, its path, and its depth to the PQ with h + g as its priority value.
            for neighbor, action, next_cost in problem.get_successors(current):
                next_step = path + [action]
                g = current_cost + next_cost
                h = heuristic(neighbor, problem)
                hg = h + g
                frontier.push((neighbor, next_step, g), hg)

        # Observation: I originally wrote the code for a_start_search and breadth_first_search
        # differently. That is, I followed a more "standard" implementation where you check
        # if the current node is NOT already visited INSIDE of the loop where you check each
        # neighbor. However, this did not pass the autograder so I made this change and it worked.


# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


# if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try:
        function(None)
    except util.NotDefined as error:
        exec(f"{function.__name__} = a_star_search", globals(), globals())
    except:
        pass

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
