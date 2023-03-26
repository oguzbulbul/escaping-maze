import pygame
import os
# Define colors
WALL_COLOR = (50, 50, 50)  # Grey
ROAD_COLOR = (170, 170, 170)  # White
VISITED_ROAD_COLOR = (220, 220, 220)  # White
SEEN_WALL_COLOR = (80, 80, 80)  # Grey
START_END_POINT_COLOR = (255, 0, 0)  # Red
SHORTEST_PATH_COLOR = (255, 255, 102)  # Yellow


ROAD_WIDTH = 20
WALL_WIDTH = 20


class Road:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.is_visited = False
        self.is_part_of_shortestpath = False
        self.color = ROAD_COLOR
        if self.is_part_of_shortestpath:
            self.color = SHORTEST_PATH_COLOR
        if self.is_visited:
            self.color = VISITED_ROAD_COLOR

    def control_part_of_shortestpath(self):
        self.is_part_of_shortestpath = True
        self.color = SHORTEST_PATH_COLOR

    def changestatus(self):
        self.is_visited = True
        self.color = VISITED_ROAD_COLOR


class Wall:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.is_seen = False
        self.color = WALL_COLOR
        if self.is_seen:
            self.color = SEEN_WALL_COLOR


class Robot:
    def __init__(self, x, y, screen):
        self.x = x*20
        self.y = y*20
        # set the image to  20x20
        self.image = pygame.image.load(os.path.join('robot.png'))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.screen = screen

    # change robot's position and show it on the screen

    def move_robot(self, x, y):
        self.x = x
        self.y = y
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.update()


# self.screen.blit(self.image, (self.x, self.y))
#         pygame.display.update()


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        # Draw button rectangle
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height), 0)

        # Draw button text
        font = pygame.font.SysFont('ariel', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                    self.y + (self.height/2 - text.get_height()/2)))

        # Draw button outline
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,
                             self.y-2, self.width+4, self.height+4), 0)

    def is_clicked(self, pos):
        # Check if button is clicked
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


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
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
