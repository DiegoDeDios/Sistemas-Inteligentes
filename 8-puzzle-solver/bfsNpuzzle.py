#!/usr/bin/env python3
import random
import math


def swap (list, position_a, position_b):
    list[position_a], list[position_b] = list[position_b], list[position_a]
class Graph:
    def __init__(self, root, size):
        self.root = root
        self.visited = [root]
        self.queue = []
        self.leaves = [root]
        self.size =size

    def bfs(self, goal):
        self.queue.append(self.root)
        while self.queue:
            s = self.queue.pop(0)
            if s.data == goal:
                return s
            if s not in self.visited:
                self.visited.append(s)
            for move in s.moves:
                self.queue.append(move)
        self.queue = []
        return None

    def new_level(self):
        count = len(self.leaves)
        for i in range(0, count):
            node = self.leaves.pop(0)
            node.new_moves(self.size)
            for n in node.moves:
                if n not in self.visited:
                    self.leaves.append(n)

    def print_path(self, node):
        path = [node]
        moves = []
        while node.parent is not None:
            path.append(node.parent)
            node = node.parent
        path.reverse()
        for node in path:
            print("{}\n{}\n{}\n".format(node.data[0:3],node.data[3:6],node.data[6:]))

class Node:
    def __init__(self, data, position, previous, parent):
        self.moves = []
        self.data = data
        self.position = position
        self.previous = previous
        self.parent = parent

    def new_moves(self, size):
        if self.position % size != 0 and self.previous != 'r':
            left_move = self.data.copy()
            swap(left_move, self.position, self.position - 1)
            self.moves.append(Node(left_move, self.position - 1, 'l', self))
        if self.position % size != size-1 and self.previous != 'l':
            right_move = self.data.copy()
            swap(right_move, self.position, self.position + 1)
            self.moves.append(Node(right_move, self.position + 1, 'r', self))
        if self.position > size-1 and self.previous != 'd':
            up_move = self.data.copy()
            swap(up_move, self.position, self.position - size)
            self.moves.append(Node(up_move, self.position - size, 'u', self))
        if self.position < (len(self.data)-size) and self.previous != 'u':
            down_move = self.data.copy()
            swap(down_move, self.position, self.position + size)
            self.moves.append(Node(down_move, self.position + size, 'd', self))

    def __str__(self):
        return self.data


def solve(size, input, goal):
    puzzle = input
    print("Puzzle:\n{}\n{}\n{}\n".format(puzzle[0:3],puzzle[3:6],puzzle[6:]))
    print("Goal:\n{}\n{}\n{}\n". format(goal[0:3],goal[3:6],goal[6:]))

    if puzzle != goal:
        root = Node(puzzle, puzzle.index(0), "", None)
        graph = Graph(root, int(size))
        node = None
        max = math.factorial(size**2)/2
        while node is None:
            graph.new_level()
            node = graph.bfs(goal)
            if len(graph.visited) > max:
                print("Puzzle has no solution")
                return 0
        graph.print_path(node)
        print("# of nodes: {}".format(len(graph.visited)))
        return len(graph.visited)
    return 0


def samples(goal, size):
    inputs = []
    for i in range(0, 100):
        new_puzzle = goal.copy()
        for j in range(0, random.randrange(1, 30)):
            move(new_puzzle, random.randrange(4), size, new_puzzle.index(0))
        inputs.append(new_puzzle)
    return inputs


def move(list, move_number, size, position):
    if position % size != 0 and move_number == 0:
        swap(list, position, position - 1)
    if position % size != size - 1 and move_number == 1:
        swap(list, position, position + 1)
    if position > size - 1 and move_number == 2:
        swap(list, position, position - size)
    if position < (len(list) - size) and move_number == 3 :
        swap(list, position, position + size)


if __name__ == '__main__':
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    inputs = samples(goal, 3)
    mean = 0
    for puzzle in inputs:
        mean += solve(3, puzzle,goal)
    mean = mean /100
    print("Mean: {}".format(mean))