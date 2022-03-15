#!/usr/bin/env python3

from cc import turtle, import_file, gps


class nav:
    # globals
    fuel_cost = {"move": 1}
    refuel = import_file("/lib/fuel/fuel.py").refuel
    direction = "north"
    direction_map = {
        "north": {"right": "west", "left": "east"},
        "west": {"right": "south", "left": "north"},
        "south": {"right": "east", "left": "west"},
        "east": {"right": "north", "left": "south"},
    }

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
        return call_move(turtle.up)

    def down(self):
        return call_move(turtle.down)

    def forward(self):
        return call_move(turtle.forward)

    def back(self):
        return call_move(turtle.back)

    def turn_left(self):
        self.direction = self.direction_map[self.direction]["left"]
        return turtle.turnLeft()

    def turn_right(self):
        self.direction = self.direction_map[self.direction]["right"]
        return turtle.turnRight()

    def turn_to(to_direction):
        while self.direction != to_direction:
            self.turn_right()
        return True

    def locate(self):
        return gps.locate()
