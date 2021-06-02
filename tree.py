"""
Each reached states can be sotred s a lookup table (dict) where each key is a state and each value is the node for that state. 
"""

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action



