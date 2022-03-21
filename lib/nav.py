#!/usr/bin/env python3

from cc import turtle, import_file, gps

# globals
refuel = import_file("/lib/fuel.py").refuel
(
    direction_map,
    refuel_cost,
    coordinate_cardinal_map,
    cardinal_coordinate_map,
) = import_file("data/nav.py").get_data()


class nav:
    direction = "north"
    direction_test_pass = False

    def __init__(self):
        self.direction_test_pass = self.direction_test()

    def direction_test(self):
        # west is negative x
        # north is negative z
        # xzy
        starting_position = gps.locate()

        if starting_position:

            if self.forward():
                diff = [a - b for a, b in zip(gps.locate(), starting_position)]
                for axis in range(2):
                    if diff[axis] != 0:
                        self.direction = coordinate_cardinal_map[axis][diff[axis]]
                        self.back()
                        return True
                self.back()

            elif self.back():
                self.turn_left()
                self.turn_left()
                diff = [a - b for a, b in zip(gps.locate(), starting_position)]
                for axis in range(2):
                    if diff[axis] != 0:
                        self.direction = coordinate_cardinal_map[axis][diff[axis]]
                        self.back()
                        self.turn_left()
                        self.turn_left()
                        return True
                self.back()
                self.turn_left()
                self.turn_left()
        return False

    def call_move(self, move):

        try:
            if move():
                return True
        # try:
        ## If move failed there is a mob in the way
        # if move == turtle.back and not move():
        # self.turn_left()
        # self.turn_left()
        # move = turtle.forward
        # while not move() and not turtle.detect():
        # turtle.attack()
        # self.turn_left()
        # self.turn_left()
        # else:
        ## Add all directions
        # while not move() and not turtle.detect():
        # if move == turtle.forward:
        # turtle.attack()
        # elif move == turtle.up:
        # turtle.attackUp()
        # elif move == turtle.down():
        # turtle.attackDown()
        # return True

        except BaseException as error:
            refuel()

            try:
                if move():
                    return True
            except:
                return False

    def up(self):
        return self.call_move(turtle.up)

    def down(self):
        return self.call_move(turtle.down)

    def forward(self):
        return self.call_move(turtle.forward)

    def back(self):
        return self.call_move(turtle.back)

    def turn_left(self):
        self.direction = direction_map[self.direction]["left"]
        return turtle.turnLeft()

    def turn_right(self):
        self.direction = direction_map[self.direction]["right"]
        return turtle.turnRight()

    def turn_to(self, to_direction):
        while self.direction != to_direction:
            self.turn_right()
        return True

    def locate(self):
        return [x for x in gps.locate()]

    def move_relative(self, coordinates):
        if not self.direction_test_pass:
            return False

        for axis in range(2):

            if coordinates[axis] != 0:
                movement = coordinates[axis] / abs(coordinates[axis])
                self.turn_to(coordinate_cardinal_map[axis][movement])
                for _ in range(abs(coordinates[axis])):
                    if not self.forward():
                        return False

        move = self.up if coordinates[2] > 0 else self.down
        for _ in range(abs(coordinates[2])):
            if not move():
                return False

        return True

    def move(self, coordinates):
        position = self.locate()
        if position[0]:
            diff_coordinates = [a - b for a, b in zip(coordinates, position)]
            return self.move_relative(diff_coordinates)
        return False

    def path(self, coordinates):
        if not coordinates:
            return True

        if not self.move(coordinates):
            current_position = self.locate()
            for axis in range(2):
                for movement in [1, -1]:
                    starting_position = self.locate()
                    starting_direction = self.locate()
                    self.turn_to(coordinate_cardinal_map[axis][movement])
                    self.forward()
                    if self.move(coordinates):
                        return True
                    if not self.move(starting_position):
                        return False
                    self.turn_to(starting_direction)

            for movement in [self.up, self.down]:
                starting_position = self.locate()
                starting_direction = self.locate()
                movement()
                if self.move(self, coordinates):
                    return True
                if not self.move(self, starting_position):
                    return False
                self.turn_to(starting_direction)

    def get_cardinal_coordinates(self):
        return cardinal_coordinate_map[self.direction]

    def get_opposite_direction(self):
        coordinates = cardinal_coordinate_map[self.direction]
        new_direction_direction = -1 if coordinates["direction"] == 1 else 1
        return coordinate_cardinal_map[coordinates["axis"]][new_direction_direction]
