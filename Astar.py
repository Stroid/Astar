
import numpy as np  # for array stuff and random
from PIL import Image  # for creating visual of our env
import cv2  # for show visual

SIZE = 10
SCL = 30

START_COLOR = (0, 255, 0)
END_COLOR = (255, 175, 0)


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def Astar(wals, start, end):
    """Returns a list of tuples as a path from given start to given end"""

    openSet = []
    closedSet = []

    # Create start and end node
    start_n = node(None, start)
    end_n = node(None, end)

    openSet.append(start_n)

    while(len(openSet) > 0):
        # Find the node width the lowest "f"score
        current_node = openSet[0]
        current_index = 0
        for index, node in enumerate(openSet):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        openSet.pop(index)
        closedSet.append(current_node)

        # Check if current node are on end node
        if current_node.position == end_n.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path(:: -1) # Return reversed path

        neighbours = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]

            # Get the new possition
            new_x = current_node.position[0] + new_position[0]
            new_y = current_node.position[1] + new_position[1]
            new_node_position = (new_x, new_y)

            # Check if the new node is inside the maze
            if new_node_position[0] < 0 or new_node_position[0] > SIZE or new_node_position[1] > 0 or new_node_position[1] > SIZE:
                continue

            # Check if new node is on a wall
            on_wall = False
            for wall in walls:
                if wall == new_node_position:
                    on_wall = True
                    break
            if on_wall:
                continue

            # Create new node
            new_node = Node(current_node, new_node_position)

            # Add the new node to the list
            neighbours.append(new_node)



class Blob:
    '''A class to display squares on the display'''

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, env):
        env[self.x][self.y] = self.color
        return env


start_blob = Blob(1, 1, START_COLOR)
end_blob = Blob(8, 8, END_COLOR)


def main():
    """ Where the main code lives """

    """----------Environment-----------"""
    env = np.zeros((SIZE, SIZE, 3),
                   dtype=np.uint8)  # Init a black image at a given size

    # Place the blobs on the environment...
    env = start_blob.draw(env)  # Draw start blob
    env = end_blob.draw(env)

    # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = Image.fromarray(env, 'RGB')
    # Recizeing the image at the given scale value.
    img = img.resize((SIZE * SCL, SIZE * SCL))
    cv2.imshow('Astar', np.array(img))

    cv2.waitKey(0)  # Whait for the Esc key to be pressed
    cv2.destroyAllWindows()  # Close the window


if(__name__ == '__main__'):
    main()
