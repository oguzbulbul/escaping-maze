from ıtems import Robot, Road, Wall, astar, Button
from urllib.request import urlopen
import pygame
import random
import os
import tkinter as tk
# Set the size of the window
WINDOW_SIZE = (1400, 800)

# Define colors
WALL_COLOR = (50, 50, 50)  # Grey
ROAD_COLOR = (170, 170, 170)  # White
VISITED_ROAD_COLOR = (220, 220, 220)  # White
SEEN_WALL_COLOR = (80, 80, 80)  # Grey
START_END_POINT_COLOR = (255, 0, 0)  # Red
SHORTEST_PATH_COLOR = (255, 255, 102)  # Yellow


# Define dimensions
WALL_WIDTH = 20
ROAD_WIDTH = 20

# Define delay
DELAY = 200


def read_url_turn_to_matrix(url):
    """Read the url and turn it into a matrix"""
    save_data_to_txt_file(
        f"\n1)read_url_turn_to_matrix(url) is called with url = {url}\n")
    tempmatrix = []
    response = urlopen(url=url)
    data = response.read()
    text = data.decode('utf-8')
    locx = 1
    locy = 1
    ix = 0
    iy = 0
    for line in text.splitlines():
        row = []
        for char in line.strip():
            # Convert the character to an integer and append it to the row
            row.append(int(char))
            if char == "0":
                if ix == 0 or ix == len(text.splitlines()) - 1 or iy == 0 or iy == len(line.strip()) - 1:
                    pass
                else:
                    pass
                locx += 1
            elif char == "1" or char == "2" or char == "3":
                locx += 1
                # Append the row to the matrix
            iy += 1
        ix += 1
        iy = 0
        locy += 1
        locx = 1
        tempmatrix.append(row)
        # save data to txt file
        save_data_to_txt_file(f"{row}\n")
    return tempmatrix


# print(read_url_turn_to_matrix("http://bilgisayar.kocaeli.edu.tr/prolab2/url1.txt"))
# checked


def add_walls_around_the_matrix(matrix):
    """Add walls around the matrix"""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == 0 or i == len(matrix) - 1 or j == 0 or j == len(matrix[i]) - 1:
                matrix[i][j] = 1
    # save data to txt file
    save_data_to_txt_file(
        f"\n2)add_walls_around_the_matrix(matrix) is called with matrix \n")
    save_data_to_txt_file(f"and added walls around the matrix\n")
    return matrix


# print(add_walls_around_the_matrix(read_url_turn_to_matrix("http://bilgisayar.kocaeli.edu.tr/prolab2/url1.txt")))
# checked


def multiply_matrix_with_wall_width(matrix):
    """Multiply the matrix with WALL_WIDTH"""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= WALL_WIDTH
    # save data to txt file
    save_data_to_txt_file(
        f"\n3)multiply_matrix_with_wall_width(matrix) is called with matrix\n")
    save_data_to_txt_file(
        f"and multiplied the matrix with WALL_WIDTH({WALL_WIDTH})\n")
    return matrix


# print(multiply_matrix_with_wall_width(add_walls_around_the_matrix(url_turn_to_matrix("http://bilgisayar.kocaeli.edu.tr/prolab2/url1.txt"))))
# checked


def determine_start_end_points(matrix):
    """Determine the start and end points"""
    # chose a random start point by "0" and locate indexes as locatex and locatey
    start_point = (random.randint(1, len(matrix) - 2),
                   random.randint(1, len(matrix[0]) - 2))
    while matrix[start_point[0]][start_point[1]] != 0:
        start_point = (random.randint(1, len(matrix) - 2),
                       random.randint(1, len(matrix[0]) - 2))
    # chose a random end point by "0" and locate indexes as locatex and locatey
    end_point = (random.randint(1, len(matrix) - 2),
                 random.randint(1, len(matrix[0]) - 2))
    while matrix[end_point[0]][end_point[1]] != 0:
        end_point = (random.randint(1, len(matrix) - 2),
                     random.randint(1, len(matrix[0]) - 2))
    # if start point and end point are the same, chose a new end point
    while start_point == end_point:
        end_point = (random.randint(1, len(matrix) - 2),
                     random.randint(1, len(matrix[0]) - 2))
    # save data to txt file
    save_data_to_txt_file(
        f"\n4)determine_start_end_points(matrix) is called with matrix \n")
    save_data_to_txt_file(
        f"and determined start and end points all by random positions\n")
    save_data_to_txt_file(
        f"start_point = {start_point}\tend_point = {end_point}\n")

    return start_point, end_point


def determine_start_end_points_by_opposite_corners(matrix):
    """Determine the start and end points by opposite corners"""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                start_point = (i, j)
                break
    for i in range(len(matrix) - 1, -1, -1):
        for j in range(len(matrix[i]) - 1, -1, -1):
            if matrix[i][j] == 0:
                end_point = (i, j)
                break
    # save data to txt file
    save_data_to_txt_file(
        f"\n4)determine_start_end_points_by_opposite_corners(matrix) is called with matrix \n")
    save_data_to_txt_file(
        f"and determined start and end points by opposite corners\n")
    save_data_to_txt_file(
        f"start_point = {start_point}\tend_point = {end_point}\n")

    return start_point, end_point


def create_maze_matrix(mazesize):
    # generate a square matrix with random 0s and 1s
    save_data_to_txt_file(
        f"\n5)create_maze_matrix(mazesize) is called with mazesize\n")
    save_data_to_txt_file(
        f"and created a square matrix with random 0s and 1s\n")
    save_data_to_txt_file(f"{mazesize}x{mazesize} matrix: \n")
    matrix = [[0 if random.random() < 0.80 else 1 for j in range(mazesize)]
              for i in range(mazesize)]
    for i in range(mazesize):
        for j in range(mazesize):
            if i == 0 or i == mazesize - 1 or j == 0 or j == mazesize - 1:
                matrix[i][j] = 1
            save_data_to_txt_file(f"{matrix[i][j]}")
        save_data_to_txt_file(f"\n")
    return matrix

# print(create_maze_matrix(10))
# checked


def draw_object(screen, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x*WALL_WIDTH,
                     y*WALL_WIDTH, width, height))
# checked

# locate robot at starting point


def create_pygame_screen():
    """Create the pygame screen"""
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Maze")
    # screen.fill((0, 0, 0))
    save_data_to_txt_file(f"\n6)create_pygame_screen() is called\n")
    save_data_to_txt_file(f"and created the pygame screen\n")
    return screen
# checked


def explore_map(maze, start, end):
    explored = set()
    # Keep track of the current positions in list
    steps = []
    # Keep track of the current positions in set
    save_data_to_txt_file(
        f"\n7)explore_map(maze, start, end) is called with maze, start, end\n")
    save_data_to_txt_file(f"and explored the map\n")

    def explore(row, col):
        if (row, col) in explored or maze[row][col] != 0:
            return
        explored.add((row, col))
        # steps.append((row, col))
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == 0:
                print("Going from ({}, {}) to ({}, {})".format(
                    row, col, new_row, new_col))
                save_data_to_txt_file(
                    f"Going from ({row}, {col}) to ({new_row}, {new_col})\n")
                steps.append((row, col))
                steps.append((new_row, new_col))
                explore(new_row, new_col)
            if (new_row, new_col) == end:
                print("Going from ({}, {}) to ({}, {})".format(
                    row, col, new_row, new_col))
                steps.append((row, col))
                steps.append((new_row, new_col))
                return steps, len(set(steps))

   # explore by robot's position
    explore(start[0], start[1])

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if (row, col) not in explored and maze[row][col] == 0:
                explore(row, col)

    step_count = len(set(steps))
    print("Steps: {}".format(step_count))
    save_data_to_txt_file(f"Steps: {step_count}\n")
    return steps, step_count


def multiply_tuple_list(tuple_list, number):
    """Multiply a tuple list with a number"""
    new_tuple_list = []
    for i in range(len(tuple_list)):
        new_tuple_list.append(
            (tuple_list[i][0]*number, tuple_list[i][1]*number))
    return new_tuple_list


def turn_matrix_to_roads_and_walls(matrix):
    """Turn the matrix to roads and walls"""
    # matrix = multiply_matrix_with_wall_width(matrix)
    roads = []
    walls = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                ro = Road(j, i, 0)
                roads.append(ro)
            else:
                # elif matrix[i][j] == 1 or matrix[i][j] == 2 or matrix[i][j] == 3:
                wa = Wall(j, i, 1)
                walls.append(wa)
    save_data_to_txt_file(
        f"\n8)turn_matrix_to_roads_and_walls(matrix) is called with matrix\n")
    save_data_to_txt_file(f"and turned the matrix to roads and walls\n")
    return roads, walls


def draw_map_by_roads_and_walls(matrix, screen, roads, walls):
    # matrix = multiply_matrix_with_wall_width(matrix)
    screen.fill((0, 0, 0))
    for road in roads:
        draw_object(screen, road.x, road.y, WALL_WIDTH, WALL_WIDTH, road.color)
    for wall in walls:
        draw_object(screen, wall.x, wall.y, WALL_WIDTH, WALL_WIDTH, wall.color)
    save_data_to_txt_file(
        f"\n9)draw_map_by_roads_and_walls(matrix, screen, roads, walls) is called with matrix, screen, roads, walls\n")
    save_data_to_txt_file(f"and drew the map by roads and walls\n")


def draw_start_and_points(matrix, screen, start_point, end_point):
    draw_object(screen, start_point[1], start_point[0],
                WALL_WIDTH, WALL_WIDTH, (0, 255, 0))
    draw_object(screen, end_point[1], end_point[0],
                WALL_WIDTH, WALL_WIDTH, (255, 0, 0))
    save_data_to_txt_file(
        f"\n10)draw_start_and_points(matrix, screen, start_point, end_point) is called with matrix, screen, start_point, end_point\n")
    save_data_to_txt_file(f"and drew the start and points\n")


def control_road_by_location_and_change_road_color(x, y, roads):
    """Control the road by location and change the road color"""

    save_data_to_txt_file(
        f"\n11)control_road_by_location_and_change_road_color(x, y, roads) is called with x, y, roads\n")
    save_data_to_txt_file(
        f"and controlled the road by location and changed the road color\n")
    for road in roads:
        if road.x == x and road.y == y:
            road.visited = True
            road.color = VISITED_ROAD_COLOR
            road.changestatus()
            save_data_to_txt_file(
                f"in position: road ({road.x}, {road.y}) is visited\n")
    return roads


def control_wall_by_location_and_change_wall_color(x, y, walls):
    """Control the wall by location and change the wall color"""
    # Change the color of the wall if there is a wall on the right, left, bottom, or top of the location
    for wall in walls:  # sağında , solunda , altında , üstünde
        if wall.x == x + 1 and wall.y == y or wall.x == x - 1 and wall.y == y or wall.x == x and wall.y == y + 1 or wall.x == x and wall.y == y - 1:
            wall.is_seen = True
            wall.color = SEEN_WALL_COLOR
            save_data_to_txt_file(
                f"in position:  wall ({wall.x}, {wall.y}) is seen\n")
    return walls


def lines_for_game_frame(screen, size):
    """Draw the lines for the game frame"""
    # draw the vertical lines
    for i in range(0, (size+1)*WALL_WIDTH, WALL_WIDTH):
        pygame.draw.line(screen, (220, 220, 220),
                         (i, 0), (i, size*WALL_WIDTH), 1)
    # draw the horizontal lines
    for i in range(0, (size+1)*WALL_WIDTH, WALL_WIDTH):
        pygame.draw.line(screen, (220, 220, 220),
                         (0, i), (size*WALL_WIDTH, i), 1)


def trackers(screen, steps, time):
    """Draw the trackers"""
    # line from (1000, 0) to (1000, 800)
    pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 800), 10)
    # locate label for counting steps
    font = pygame.font.SysFont('arcade', 30)
    text = font.render(f"Steps : {steps}", True, (255, 255, 255))
    screen.blit(text, (1020, 40))
    # locate label for timer (counting seconds)
    font = pygame.font.SysFont('arcade', 30)
    text = font.render(
        f"Time : {time}", True, (255, 255, 255))
    screen.blit(text, (1020, 80))


def add_increase_and_decrease_delay_buttons(screen):
    """Add the increase and decrease delay buttons"""
    # increase delay button
    button1 = Button(x=1020, y=120, width=40, height=30,
                     color=(255, 51, 51), text="-")
    button1.draw(screen)
    # decrease delay button
    button2 = Button(x=1120, y=120, width=40, height=30,
                     color=(51, 255, 51), text="+")
    button2.draw(screen)
    pygame.display.update()
    return button1, button2


def count_visited_road(roads):
    """Count the visited roads"""
    save_data_to_txt_file(
        f"\n12)count_visited_road(roads) is called with roads\n")
    save_data_to_txt_file(f"and counted the visited roads\n")
    count = 0
    for road in roads:
        if road.is_visited:
            count += 1
    save_data_to_txt_file(f"count of visited roads: {count}\n")
    return count


def add_roads_to_shortest_path(maze, start, end, roads):
    """Add the roads to the shortest path"""
    save_data_to_txt_file(
        f"\n13)add_roads_to_shortest_path(maze, start, end, roads) is called with maze, start, end, roads\n")
    save_data_to_txt_file(f"and added the roads to the shortest path\n")
    save_data_to_txt_file(f"shortest path: \n")
    shortest_path = astar(maze, start, end)  # shortest path
    print(shortest_path)
    shortest_path = multiply_tuple_list(shortest_path, WALL_WIDTH)
    print(shortest_path)
    for path in shortest_path:
        for road in roads:
            if road.x*WALL_WIDTH == path[1] and road.y*WALL_WIDTH == path[0]:
                # print("location")
                # print(path[0], path[1], path)
                # print("road")
                # print(road.x, road.y)
                road.color = SHORTEST_PATH_COLOR
                road.is_shortest_path = True
                save_data_to_txt_file(
                    f"({road.x*WALL_WIDTH},{road.y*WALL_WIDTH}) ")
        save_data_to_txt_file(f"\n")
    return roads


def create_data_txt_file():
    """Create the data txt file"""
    with open("data.txt", "w") as file:
        file.write("PROJECT DATA SHEET :")
        file.close()


def save_data_to_txt_file(text):
    """Save the data to the txt file"""
    with open("data.txt", "a") as file:
        file.write(f"{text}")
        file.close()


def button1_clicked(url, window):
    """Button1 clicked"""
    # destroy the window
    window.destroy()
    # create the pygame screen
    screen = create_pygame_screen()
    screen.fill((0, 0, 0))
    # read the url and turn it into a matrix
    matrix = read_url_turn_to_matrix(url)
    rot_matrix = matrix

    # create the pygame screen
    screen = create_pygame_screen()
    screen.fill((0, 0, 0))
    # add walls around the matrix
    # matrix = add_walls_around_the_matrix(matrix)
    # multiply the matrix with WALL_WIDTH
    matrix = multiply_matrix_with_wall_width(matrix)
    # determine the start and end points
    # start_point, end_point = determine_start_end_points(matrix)
    start_point, end_point = determine_start_end_points_by_opposite_corners(
        matrix)
    # draw the walls

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1*20 or matrix[i][j] == 2*20 or matrix[i][j] == 3*20:
                draw_object(screen, j, i, WALL_WIDTH, WALL_WIDTH, WALL_COLOR)
    # draw the roads
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                draw_object(screen, j, i, ROAD_WIDTH, ROAD_WIDTH, ROAD_COLOR)

    lines_for_game_frame(screen, len(matrix))


# _______________________________________________________________________________________

    # draw the start and end points
    draw_start_and_points(matrix, screen, start_point, end_point)

    # locate robot
    robot = Robot(start_point[1], start_point[0], screen=screen)

    # directions
    directions, total_step = explore_map(
        maze=rot_matrix, start=start_point, end=end_point)
    directions = multiply_tuple_list(directions, 20)

    # update the screen
    # pygame.display.update()
    # wait for the user to close the window
    roads, walls = turn_matrix_to_roads_and_walls(matrix)
    steps = 0
    start_time = 0
    current_time = 0
    delay = DELAY
    for dir in directions:
        robot.move_robot(dir[1], dir[0])
        pygame.time.delay(delay)
        draw_map_by_roads_and_walls(
            matrix=matrix, screen=screen, roads=roads, walls=walls)
        draw_start_and_points(matrix, screen, start_point, end_point)

        roads = control_road_by_location_and_change_road_color(
            x=dir[1]/20, y=dir[0]/20, roads=roads)
        walls = control_wall_by_location_and_change_wall_color(
            x=dir[1]/20, y=dir[0]/20, walls=walls)

        lines_for_game_frame(screen, len(matrix))
        steps = count_visited_road(roads=roads)
        current_time = pygame.time.get_ticks() - start_time
        inc_but, dec_but = add_increase_and_decrease_delay_buttons(screen)
        trackers(screen, steps=steps, time=round(current_time/1000))
        # if the robot reach the end point
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if button is clicked
                if inc_but.is_clicked(pygame.mouse.get_pos()):
                    print('increase button clicked')
                    delay += 300
                if dec_but.is_clicked(pygame.mouse.get_pos()):
                    print('decrease button clicked')
                    delay -= 300

        if (dir[1]/20, dir[0]/20) == (end_point[1], end_point[0]):
            trackers(screen, steps=steps, time=round(current_time/1000))
            pygame.time.delay(2000)
            pygame.display.update()
            roads = add_roads_to_shortest_path(
                roads=roads, maze=rot_matrix, start=start_point, end=end_point)

            draw_map_by_roads_and_walls(

                matrix=matrix, screen=screen, roads=roads, walls=walls)
            draw_start_and_points(matrix, screen, start_point, end_point)
            lines_for_game_frame(screen, len(matrix))
            trackers(screen, steps=steps,
                     time=round(current_time/1000 - 2))

            pygame.time.delay(2000)
            break
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        pygame.display.update()


def button2_clicked(mazesize, window):
    """Button2 clicked"""
    # close the window
    window.destroy()
    # create maze by using mazesize
    matrix = create_maze_matrix(mazesize)
    rot_matrix = matrix
    # create the pygame screen
    screen = create_pygame_screen()
    screen.fill((0, 0, 0))
    # add walls around the matrix
    # matrix = add_walls_around_the_matrix(matrix)
    # multiply the matrix with WALL_WIDTH
    matrix = multiply_matrix_with_wall_width(matrix)

    # determine the start and end points
    # start_point, end_point = determine_start_end_points(matrix)
    start_point, end_point = determine_start_end_points_by_opposite_corners(
        matrix)

    # draw the walls

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1*20 or matrix[i][j] == 2*20 or matrix[i][j] == 3*20:
                draw_object(screen, j, i, WALL_WIDTH, WALL_WIDTH, WALL_COLOR)
    # draw the roads
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                draw_object(screen, j, i, ROAD_WIDTH, ROAD_WIDTH, ROAD_COLOR)

    lines_for_game_frame(screen, len(matrix))

# _______________________________________________________________________________________

    # draw the start and end points
    draw_start_and_points(matrix, screen, start_point, end_point)

    # locate robot
    robot = Robot(start_point[1], start_point[0], screen=screen)

    # directions
    directions, total_step = explore_map(
        maze=rot_matrix, start=start_point, end=end_point)
    directions = multiply_tuple_list(directions, 20)

    # update the screen
    # pygame.display.update()
    # wait for the user to close the window
    roads, walls = turn_matrix_to_roads_and_walls(matrix)
    steps = 0
    start_time = 0
    current_time = 0
    delay = DELAY
    for dir in directions:

        robot.move_robot(dir[1], dir[0])
        pygame.time.delay(delay)
        draw_map_by_roads_and_walls(
            matrix=matrix, screen=screen, roads=roads, walls=walls)
        draw_start_and_points(matrix, screen, start_point, end_point)

        roads = control_road_by_location_and_change_road_color(
            x=dir[1]/20, y=dir[0]/20, roads=roads)
        walls = control_wall_by_location_and_change_wall_color(
            x=dir[1]/20, y=dir[0]/20, walls=walls)

        lines_for_game_frame(screen, len(matrix))
        steps = count_visited_road(roads=roads)
        current_time = pygame.time.get_ticks() - start_time
        inc_but, dec_but = add_increase_and_decrease_delay_buttons(screen)
        trackers(screen, steps=steps, time=round(current_time/1000))
        # if the robot reach the end point
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if button is clicked
                if inc_but.is_clicked(pygame.mouse.get_pos()):
                    print('increase button clicked')
                    delay += 100
                if dec_but.is_clicked(pygame.mouse.get_pos()):
                    print('decrease button clicked')
                    delay -= 100

        if (dir[1]/20, dir[0]/20) == (end_point[1], end_point[0]):
            trackers(screen, steps=steps, time=round(current_time/1000))
            pygame.time.delay(2000)
            pygame.display.update()
            roads = add_roads_to_shortest_path(
                roads=roads, maze=rot_matrix, start=start_point, end=end_point)

            draw_map_by_roads_and_walls(

                matrix=matrix, screen=screen, roads=roads, walls=walls)
            draw_start_and_points(matrix, screen, start_point, end_point)
            lines_for_game_frame(screen, len(matrix))
            trackers(screen, steps=steps,
                     time=round(current_time/1000 - 2))

            pygame.time.delay(2000)
            break
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        pygame.display.update()


def create_tkinter_menu():
    """Create the tkinter menu"""
    # make window size
    window = tk.Tk()
    window.title("Maze")
    window.geometry("1200x700")
    # add one label for game title,add two entry boxes and add two buttons for start and exit with grid
    # every cells are should be the same size
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)

    font = ("arcade", 50, "bold")
    # add one label for game title
    label = tk.Label(window, text="Maze", font=font)
    label.grid(row=0, column=0, columnspan=2)

    font = ("arcade", 20, "bold")

    # add two entry boxes
    entry1 = tk.Entry(window, width=35, font=font)
    entry1.grid(row=1, column=0)
    entry2 = tk.Entry(window, width=35, font=font)
    entry2.grid(row=1, column=1)

    # add two buttons for start and exit with grid
    button1 = tk.Button(
        window, text="enter url and start game", width=35, font=font)
    button1.grid(row=2, column=0)
    button2 = tk.Button(
        window, text="enter size of matrix and start game", width=35, font=font)
    button2.grid(row=2, column=1)

    # menu with gaming theme
    window.configure(bg="black", relief="sunken", bd=10, cursor="pirate",
                     highlightcolor="red", highlightbackground="red", highlightthickness=5)
    label.configure(bg="black", fg="white", relief="sunken", bd=10, cursor="pirate", highlightcolor="red", highlightbackground="red",
                    highlightthickness=5, activebackground="red", activeforeground="white", anchor="center", justify="center", padx=2000, pady=10, wraplength=1000)
    entry1.configure(bg="black", fg="white", relief="sunken", bd=10, cursor="pirate", highlightcolor="red", highlightbackground="red",
                     highlightthickness=5, justify="center")
    entry2.configure(bg="black", fg="white", relief="sunken", bd=10, cursor="pirate", highlightcolor="red", highlightbackground="red",
                     highlightthickness=5, justify="center")
    button1.configure(bg="black", fg="white", relief="sunken", bd=10, cursor="pirate", highlightcolor="red", highlightbackground="red", highlightthickness=5,
                      activebackground="red", activeforeground="white", anchor="center", justify="center", padx=10, pady=10, wraplength=1000, command=lambda: button1_clicked(entry1.get(), window=window), takefocus=True)
    button2.configure(bg="black", fg="white", relief="sunken", bd=10, cursor="pirate", highlightcolor="red", highlightbackground="red", highlightthickness=5,
                      activebackground="red", activeforeground="white", anchor="center", justify="center", padx=10, pady=10, wraplength=1000, command=lambda: button2_clicked(int(entry2.get()), window=window), takefocus=True)

    create_data_txt_file()

    # window.mainloop()  # if u want to use return window u should close this line and make mainloop returned variable
    return window


# test create_tkinter_menu method
# menu = create_tkinter_menu()
# menu.mainloop()
