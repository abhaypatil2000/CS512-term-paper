"""
1 for GBF search
2 for A*
3 for A* with 2 cordinating players
4 for A* with 4 cordinating players
5 prediction involved with the simple A*
"""

from random import choice, random
from time import sleep
from turtle import *
from freegames import floor, vector
# vector is nothing but pair<int, int> in c++

from math import sqrt
from heapq import heapify, heappush, heappop
from random import uniform
from map import *

import copy


def square(x, y):
    """
    Draw blue square using path turtle at (x, y).

    Blue square drawn above white pellet to hide it.
    """
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return tile index, from the grid cordinates"""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if cordinate point is valid in tiles"""
    index = offset(point)
    if tiles[index] == 0:
        return False

    index = offset(point + 19)  # adds to both the cordinates
    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draws the initial map using path turtle"""
    bgcolor('orange')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def heuristic(position):
    """heuristic cost to go from ghost 'position' to 'pacman' cordinates"""
    return sqrt((position.x - pacman.x)**2 + (position.y - pacman.y)**2)  # euclidean
    # return abs(position.x - pacman.x) + abs(position.y - pacman.y)  # manhattan


def pathCost(point, direction):
    """returns the cost for travelling from ghost 'point' to 'pacman' cordinates"""
    global ghost_rank  # this is used to know the rank of the ghost for which direction is being found
    # global prev_path_penalty  # this is a dictionary used to keep track of the previous ghost's paths for cordinated A* and penalty associated with it
    global curr_path_penalty
    # global best_path
    # map from (i, j) cordinates => to penalty cost for g(x)
    global tiles
    if version == 1:  # Greedy best first
        return heuristic(point + direction)
    elif version == 2:  # A* search
        visited = set()
        options = [
            vector(step_size, 0),
            vector(-step_size, 0),
            vector(0, step_size),
            vector(0, -step_size),
        ]

        heap = []
        heappush(
            heap,
            (
                1 + heuristic(point + direction),  # f(x) = g(x) + h(x)
                1,  # g(x)
                uniform(0, 1),  # for tie breaker as the next two arguements don't support < or <= comparators
                point + direction,  # new position
                direction,  # previous step
            ),
        )
        visited.add((point.x, point.y))

        while len(heap) != 0:
            tope = heappop(heap)

            g_x = tope[1]
            curr_pos = tope[3]
            prev_step = tope[4]

            if (curr_pos.x, curr_pos.y) in visited:
                continue
            visited.add((curr_pos.x, curr_pos.y))

            if curr_pos == pacman:
                return g_x

            for currCourse in options:
                if currCourse + prev_step != vector(0, 0):  # pacman is not allowed to take a u-turn
                    if (valid(curr_pos + currCourse)):
                        heappush(
                            heap,
                            (
                                g_x + 1 + heuristic(curr_pos + currCourse),
                                g_x + 1,
                                uniform(0, 1),
                                curr_pos + currCourse,
                                currCourse,
                            ),
                        )

    elif version == 3:  # A* with two players coordinating
        # 0 and 1 are cordinating
        # 2 and 3 are independent

        if ghost_rank == 2 or ghost_rank == 3:  # the uncordinated ghosts
            visited = set()
            options = [
                vector(step_size, 0),
                vector(-step_size, 0),
                vector(0, step_size),
                vector(0, -step_size),
            ]

            heap = []
            heappush(
                heap,
                (
                    1 + heuristic(point + direction),  # f(x) = g(x) + h(x)
                    1,  # g(x)
                    uniform(0, 1),  # for tie breaker as the next two arguements don't support < or <= comparators
                    point + direction,  # new position
                    direction,  # previous step
                ),
            )
            visited.add((point.x, point.y))

            while len(heap) != 0:
                tope = heappop(heap)

                g_x = tope[1]
                curr_pos = tope[3]
                prev_step = tope[4]

                if (curr_pos.x, curr_pos.y) in visited:
                    continue
                visited.add((curr_pos.x, curr_pos.y))

                if curr_pos == pacman:
                    return g_x

                for currCourse in options:
                    if currCourse + prev_step != vector(0, 0):  # pacman is not allowed to take a u-turn
                        if (valid(curr_pos + currCourse)):
                            heappush(
                                heap,
                                (
                                    g_x + 1 + heuristic(curr_pos + currCourse),
                                    g_x + 1,
                                    uniform(0, 1),
                                    curr_pos + currCourse,
                                    currCourse,
                                ),
                            )

        elif ghost_rank == 0:  # leader ghost
            visited = set()
            options = [
                vector(step_size, 0),
                vector(-step_size, 0),
                vector(0, step_size),
                vector(0, -step_size),
            ]

            heap = []
            heappush(
                heap,
                (
                    1 + heuristic(point + direction),  # f(x) = g(x) + h(x)
                    1,  # g(x)
                    uniform(0, 1),  # for tie breaker as the next two arguements don't support < or <= comparators
                    point + direction,  # new position
                    direction,  # previous step
                ),
            )
            prev = {}  # the previous nodes for a path (to find the path in A* search)
            visited.add((point.x, point.y))
            prev[(point.x, point.y)] = -1

            while len(heap) != 0:
                tope = heappop(heap)

                g_x = tope[1]
                curr_pos = tope[3]
                prev_step = tope[4]

                if (curr_pos.x, curr_pos.y) in visited:
                    continue
                visited.add((curr_pos.x, curr_pos.y))

                prev[(curr_pos.x, curr_pos.y)] = (curr_pos.x - prev_step.x, curr_pos.y - prev_step.y)

                if curr_pos == pacman:
                    # now reconstruct the path and assign penalty to each node
                    curr_pos = (curr_pos.x, curr_pos.y)
                    curr = prev[curr_pos]
                    curr_penalty = intersection_penalty

                    while curr != -1:
                        if curr in curr_path_penalty.keys():
                            curr_path_penalty[curr] += curr_penalty
                        else:
                            curr_path_penalty[curr] = curr_penalty
                        curr_penalty *= decay_factor
                        curr = prev[curr]
                    return g_x

                for currCourse in options:
                    if currCourse + prev_step != vector(0, 0):  # pacman is not allowed to take a u-turn
                        if (valid(curr_pos + currCourse)):
                            heappush(
                                heap,
                                (
                                    g_x + 1 + heuristic(curr_pos + currCourse),
                                    g_x + 1,
                                    uniform(0, 1),
                                    curr_pos + currCourse,
                                    currCourse,
                                ),
                            )

        elif ghost_rank == 1:  # the follower ghost
            visited = set()  # marks the visited nodes
            options = [
                vector(step_size, 0),
                vector(-step_size, 0),
                vector(0, step_size),
                vector(0, -step_size),
            ]

            heap = []
            local_penalty = 0
            if (point.x + direction.x, point.y + direction.y) in curr_path_penalty.keys():
                local_penalty = curr_path_penalty[(point.x + direction.x, point.y + direction.y)]
            heappush(
                heap,
                (
                    1 + local_penalty + heuristic(point + direction),  # f(x) = g(x) + h(x)
                    1 + local_penalty,  # g(x)
                    uniform(0, 1),  # for tie breaker as the next two arguements don't support < or <= comparators
                    point + direction,  # new position
                    direction,  # previous step
                ),
            )
            visited.add((point.x, point.y))

            while len(heap) != 0:
                tope = heappop(heap)
                g_x = tope[1]
                curr_pos = tope[3]
                prev_step = tope[4]

                if (curr_pos.x, curr_pos.y) in visited:
                    continue
                visited.add((curr_pos.x, curr_pos.y))

                if curr_pos == pacman:
                    return g_x

                for currCourse in options:
                    if currCourse + prev_step != vector(0, 0):  # pacman is not allowed to take a u-turn
                        if (valid(curr_pos + currCourse)):
                            local_penalty = 0
                            if (curr_pos.x + currCourse.x, curr_pos.y + currCourse.y) in curr_path_penalty.keys():
                                local_penalty = curr_path_penalty[(curr_pos.x + currCourse.x, curr_pos.y + currCourse.y)]
                            heappush(
                                heap,
                                (
                                    g_x + 1 + local_penalty + heuristic(curr_pos + currCourse),
                                    g_x + 1 + local_penalty,
                                    uniform(0, 1),
                                    curr_pos + currCourse,
                                    currCourse,
                                ),
                            )

    elif version == 4:  # A* with 4 cordinating
        visited = set()
        options = [
            vector(step_size, 0),
            vector(-step_size, 0),
            vector(0, step_size),
            vector(0, -step_size),
        ]

        heap = []
        local_penalty = 0
        if (point.x + direction.x, point.y + direction.y) in curr_path_penalty.keys():
            local_penalty = curr_path_penalty[(point.x + direction.x, point.y + direction.y)]
        heappush(
            heap,
            (
                1 + local_penalty + heuristic(point + direction),  # f(x) = g(x) + h(x)
                1 + local_penalty,  # g(x)
                uniform(0, 1),  # for tie breaker as the next two arguements don't support < or <= comparators
                point + direction,  # new position
                direction,  # previous step
            ),
        )
        prev = {}  # the previous nodes for a path (to find the path in A* search)
        visited.add((point.x, point.y))
        prev[(point.x, point.y)] = -1

        while len(heap) != 0:
            tope = heappop(heap)

            g_x = tope[1]
            curr_pos = tope[3]
            prev_step = tope[4]

            if (curr_pos.x, curr_pos.y) in visited:
                continue
            visited.add((curr_pos.x, curr_pos.y))

            prev[(curr_pos.x, curr_pos.y)] = (curr_pos.x - prev_step.x, curr_pos.y - prev_step.y)

            if curr_pos == pacman:
                # now reconstruct the path and assign penalty to each node
                curr_pos = (curr_pos.x, curr_pos.y)
                curr = prev[curr_pos]
                curr_penalty = intersection_penalty

                while curr != -1:
                    if curr in curr_path_penalty.keys():
                        curr_path_penalty[curr] += curr_penalty
                    else:
                        curr_path_penalty[curr] = curr_penalty
                    curr_penalty *= decay_factor
                    curr = prev[curr]
                return g_x

            for currCourse in options:
                if currCourse + prev_step != vector(0, 0):  # pacman is not allowed to take a u-turn
                    if (valid(curr_pos + currCourse)):
                        local_penalty = 0
                        if (curr_pos.x + currCourse.x, curr_pos.y + currCourse.y) in curr_path_penalty.keys():
                            local_penalty = curr_path_penalty[(curr_pos.x + currCourse.x, curr_pos.y + currCourse.y)]
                        heappush(
                            heap,
                            (
                                g_x + 1 + local_penalty + heuristic(curr_pos + currCourse),
                                g_x + 1 + local_penalty,
                                uniform(0, 1),
                                curr_pos + currCourse,
                                currCourse,
                            ),
                        )

    elif version == 5:  # prediction involved with the simple A*
        visited = set()
        options = [
            vector(step_size, 0),
            vector(-step_size, 0),
            vector(0, step_size),
            vector(0, -step_size),
        ]

        heap = []
        local_discount = 0
        if tiles[offset(point + direction)] == 1:
            local_discount = 1 * discount
        heappush(
            heap,
            (
                1 - local_discount + (1 - discount) * heuristic(point + direction),  # f(x) = g(x) + h(x)
                1 - local_discount,  # g(x)
                uniform(0, 1),  # for tie breaker as the next two arguements don't support < or <= comparators
                point + direction,  # new position
                direction,  # previous step
            ),
        )
        visited.add((point.x, point.y))

        while len(heap) != 0:
            tope = heappop(heap)

            g_x = tope[1]
            curr_pos = tope[3]
            prev_step = tope[4]

            if (curr_pos.x, curr_pos.y) in visited:
                continue
            visited.add((curr_pos.x, curr_pos.y))

            if curr_pos == pacman:
                return g_x

            for currCourse in options:
                if currCourse + prev_step != vector(0, 0):  # pacman is not allowed to take a u-turn
                    if (valid(curr_pos + currCourse)):
                        local_discount = 0
                        if tiles[offset(point + direction)] == 1:
                            local_discount = 1 * discount
                        heappush(
                            heap,
                            (
                                g_x + 1 - discount + (1 - discount) * heuristic(curr_pos + currCourse),
                                g_x + 1 - discount,
                                uniform(0, 1),
                                curr_pos + currCourse,
                                currCourse,
                            ),
                        )


def move():
    """Move pacman and all ghosts using this function"""
    global timeout
    global mid_time
    global end_time
    global ghost_rank
    global prev_path_penalty  # map from (i, j) cordinated => to penalty cost for g(x)
    global curr_path_penalty
    global best_path_penalty
    global end_score
    writer.undo()
    writer.write(state['score'])

    clear()  # this will clear the previous pacman and ghosts positions from the screen

    if valid(pacman + aim):  # if the new position is a valid one then move to that position
        pacman.move(aim)

    index = offset(pacman)  # the tile number of the pacman

    if tiles[index] == 1:  # if tile had food
        tiles[index] = 2  # consume the food
        state['score'] += 1  # increase the score
        if state['score'] == end_score:
            print("GAME COMPLETE")
            return
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)  # now draw blue tile to hide the food particle

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')  # plot the pacman on the screen
    if timeout <= mid_time and want_timeout:
        for point, course in ghosts:
            if valid(point + course):  # if ghost can move in this direction then move there
                point.move(course)
            else:  # else chose a new direction
                options = [
                    vector(step_size, 0),
                    vector(-step_size, 0),
                    vector(0, step_size),
                    vector(0, -step_size),
                ]
                plan = choice(options)
                course.x = plan.x
                course.y = plan.y

            up()
            goto(point.x + 10, point.y + 10)
            dot(20, 'green')  # plot the ghost on the screen

        update()
    else:
        options = [
            vector(step_size, 0),
            vector(-step_size, 0),
            vector(0, step_size),
            vector(0, -step_size),
        ]

        avoid_pos = set()  # set containing the tile index of the previous pacmans which are to be avoided but not really forbidden
        ghost_rank = 0  # this is used to know the rank of the ghost for which direction is being found
        prev_path_penalty = {}  # this is a dictionary used to keep track of the previous ghost's paths for cordinated A* and penalty associated with it
        curr_path_penalty = {}  # temporary variable for prev_path_penalty
        best_path_penalty = {}  # temporary variable for prev_path_penalty
        for point, course in ghosts:
            leastPathCost = float('inf')
            plan = vector(0, 0)
            for currCourse in options:
                curr_path_penalty = copy.deepcopy(prev_path_penalty)
                if currCourse + course != vector(0, 0):  # pacman is not allowed to take a u-turn
                    if (valid(point + currCourse)):
                        next_pos = offset(point + currCourse)
                        currPathCost = pathCost(point, currCourse)  # last step is also necessary to prevent going back to the previous position

                        if next_pos in avoid_pos:
                            currPathCost += overlap_cost
                        if currPathCost is None:
                            if leastPathCost == float('inf'):
                                best_path_penalty = curr_path_penalty
                                leastPathCost = currPathCost
                                plan = currCourse
                        elif (currPathCost < leastPathCost):
                            best_path_penalty = curr_path_penalty
                            leastPathCost = currPathCost
                            plan = currCourse

            course.x = plan.x
            course.y = plan.y

            prev_path_penalty = best_path_penalty

            point.move(course)
            avoid_pos.add(offset(point))

            up()
            goto(point.x + 10, point.y + 10)
            if ghost_rank == 0:
                dot(20, 'saddle brown')
                pass
            elif ghost_rank == 1:
                dot(20, 'peru')
                pass
            elif ghost_rank == 2:
                dot(20, 'tan')
                pass
            elif ghost_rank == 3:
                dot(20, 'wheat')
                pass
            else:
                raise ()

            ghost_rank += 1

        avoid_pos.clear()
        update()

        for point, course in ghosts:
            if abs(pacman - point) < 20:  # the pacman is killed # gameover
                return

    timeout += 1
    timeout %= end_time
    ontimer(move, interval)  # this is used to create an infinite loop


def change(x, y):  # this will be called asyncronously
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


if __name__ == "__main__":
    global version
    global mid_time
    global end_time

    # Game parameters
    step_size = 10
    interval = 150  # pause in nano seconds between two frames

    # Agent parameters
    timeout = 0  # needed for switching between safe mode and attack mode of ghost
    mid_time = 15  # from [0, mid_time) scatter and [mid_time, end_time) attack mode
    end_time = 50
    want_timeout = True
    overlap_cost = 100  # cost when two ghosts are overlapping (at the same position)
    decay_factor = 0.7  # the intersection in cordinated A* decays with this factor
    intersection_penalty = 100  # the intersection penalty in case of cordinated A*
    discount = 0.9  # 1 * discount is the g(x) for a route with food particle

    print("1 for GBF search")
    print("2 for A*")
    print("3 for A* with 2 cordinating players")
    print("4 for A* with 4 cordinating players")
    print("5 prediction involved with the simple A*")
    version = int(input())

    state = {'score': 0}  # game's score
    path = Turtle(visible=False)  # needed for blue sqaures drawing
    writer = Turtle(visible=False)  # handles the score board

    aim = vector(0, 0)  # direction in which pacman wishes to go
    pacman = vector(0, 0)  # current position of the pacman

    # list for ghosts along with their starting positions and their initial directions
    ghosts = [
        [vector(-180, 160), vector(step_size, 0)],  # top left ghost
        [vector(-180, -160), vector(0, step_size)],  # botton left ghost
        [vector(100, 160), vector(0, -step_size)],  # top right ghost
        [vector(100, -160), vector(-step_size, 0)],  # botton right ghost
    ]

    # non functional setup
    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    writer.goto(160, 160)
    writer.color('white')
    writer.write(state['score'])
    listen()
    onkey(lambda: change(step_size, 0), 'Right')  # this will be called asyncronously
    onkey(lambda: change(-step_size, 0), 'Left')  # this will be called asyncronously
    onkey(lambda: change(0, step_size), 'Up')  # this will be called asyncronously
    onkey(lambda: change(0, -step_size), 'Down')  # this will be called asyncronously
    world()
    move()  # actual game starts here
    done()