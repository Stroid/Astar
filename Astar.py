
import numpy as np  # for array stuff
from PIL import Image  # for creating visual of our env
import cv2  # for show visual

SHOW_SIZE = 300  # Scalefactor when we draw the matrix
SIZE = 10  # Width and height of the matrix

AGENT_N = 1  # Agent key in dict
FOOD_N = 2  # Food key in dict
PATH_N = 3
WALL_N = 4
CLOSED_N = 5
OPEN_N = 6

d = {1: (255, 175, 0),
     2: (0, 255, 0),
     3: (245, 66, 218),
     4: (125, 125, 125),
     5: (0, 0, 255),
     6: (125,0,125)}


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# astar ################¤¤
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        print(len(open_list))
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return open_list, closed_list, path[::-1]  # Return reversed path

        #(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)
        # Generate neighbours
        neighbours = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within the maze 
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            neighbours.append(new_node)

        # Loop through neighbours
        for neighbour in neighbours:

            # neighbour is on the closed list
            not_in_closed_list = True
            for closed_neighbour in closed_list:
                if neighbour.position == closed_neighbour.position:
                    not_in_closed_list = False

            if(not_in_closed_list):
	            # Create the f, g, and h values
	            neighbour.g = current_node.g + 1
	            neighbour.h = ((neighbour.position[0] - end_node.position[0]) ** 2) + (
	                (neighbour.position[1] - end_node.position[1]) ** 2)
	            neighbour.f = neighbour.g + neighbour.h

	            # neighbour is already in the open list
	            not_in_open_list = True
	            for open_node in open_list:
	                if neighbour.position == open_node.position and neighbour.g > open_node.g:
	                    not_in_open_list = False

	            if(not_in_open_list):
	            	# Add the neighbour to the open list
	                open_list.append(neighbour)

############# astar ################


def place_on_env(env, pos, color):
    x, y = pos
    env[x][y] = color
    return env


def main():
    print("main")
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    agent_pos = (np.random.randint(1, 10), np.random.randint(1, 10))
    food_pos = (np.random.randint(1, 10), np.random.randint(1, 10))
    print("start path")
    openset, closedset, path = astar(maze, agent_pos, food_pos)
    print("end path")
    ###### Environment #######
    env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # Make a black rbg image

    # Add the walls to the environment
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[x][y] == 1:
                env = place_on_env(env, (x, y), d[WALL_N])


    # Add the closed nodes to the environment
    for node in closedset:
    	env = place_on_env(env, node.position, d[CLOSED_N])

    for node in openset:
        env = place_on_env(env, node.position, d[OPEN_N])

    # Add the path to the environment
    for node in path:
        env = place_on_env(env, node, d[PATH_N])

    env = place_on_env(env, agent_pos, d[AGENT_N]) # Add the agent to the environment
    env = place_on_env(env, food_pos, d[FOOD_N])   # Add the foot to the environment

    # reading to rgb. Apparently. Even tho color definitions are bgr. ??? why..? I DO NOT KNOW!!
    img = Image.fromarray(env, 'RGB')
    img = img.resize((SHOW_SIZE, SHOW_SIZE))  # Resizing!
    cv2.imshow('Environment', np.array(img))  # Show the beutiful matrix!
    ###########################

    print("done")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
