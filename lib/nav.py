#!/usr/bin/env python3

from cc import turtle, import_file, gps

# globals
refuel = import_file("/lib/fuel.py").refuel
direction_map, refuel_cost, coordinate_cardinal_map = import_file(
    "data/nav.py"
).get_data()


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

        if starting_position[0]:

            if self.forward():
                diff = [a - b for a, b in zip(gps.locate(), starting_position)]
                for axis in range(2):
                    if diff[axis] != 0:
                        self.direction = coordinate_cardinal_map[axis][diff[axis]]
                        self.back()
                        return True
            self.back()
            return False

    def call_move(self, move):

        try:
            move()

        except BaseException as error:
            if error == "Out of fuel":
                refuel.refuel()

            try:
                if not move():
                    return False
            except:
                return False

        return True

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
        return gps.locate()

    def move_relative(self, coordinates):
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
        position = gps.locate()
        if position[0]:
            diff_coordinates = [a - b for a, b in zip(coordinates, position)]
            return self.move_relative(diff_coordinates)
        return False
