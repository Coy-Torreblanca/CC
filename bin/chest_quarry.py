#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")
inv = import_file("/lib/inventory.py")
refuel = import_file("/lib/fuel.py").refuel
move_to_inspect, move_to_dig = import_file("/data/movement.py").get_data()
data = import_file("/data/mongo_client.py")
cm = import_file("/lib/chest_management.py")


# passing args is not working
args = [64, 64, 64]  # test


class chest_quarry:
    def __init__(self):
        self.nav = nav.nav()
        self.inventory = inv.turtleInventory(turtle)  # test - should be 16
        self.db = data.dig_map()
        self.job = "chest_quarry_" + str(self.nav.locate())
        self.chest_management = cm.chest_management(
            self.job, self.nav, self.inventory, turtle
        )

        self.nav.turn_to(self.nav.get_opposite_direction())
        chest = self.chest_management.put_chest(self, False)
        self.chest_management.chest = chest
        self.nav.turn_to(self.nav.get_opposite_direction())

    def dig(self, turtle_direction):

        block = move_to_inspect[turtle_direction]()
        if block:
            self.inventory.print()  # test
            if not self.inventory.dig(turtle_direction):

                inventory_name = self.db.find_inventory(block["name"])
                inventory_name = inventory_name or block["name"]

                new_cardinal = nav.get_opposite_direction()

                cardinal_directions = nav.get_cardinal_directions()
                axis = cardinal_directions["axis"]
                direction = cardinal_directions["direction"]
                new_direction = -1 if direction == 1 else direction
                new_location = nav.locate()
                location[axis] += new_direction

                if not self.chest_management.drop_into_chest(
                    new_direction,
                    location,
                    inventory_name,
                    False,
                    {"minecraft:chest": "None"},
                ):
                    return False

                block = move_to_inspect[turtle_direction]()
                if block:
                    self.inventory.print()  # test
                    return self.inventory.dig(turtle_direction)
        return True

    def quarry(self, length, width, height):

        print("beg. quarrying...")
        if not self.nav.direction_test_pass:
            print("direction test pass failed")
            return False

        if not self.chest_management.chest:
            print("chest could not be placed")
            return False

        print("turning")
        turn = self.nav.turn_left

        for z in range(height):
            for x in range(width):
                for y in range(length - 1):

                    print("detecting")
                    while turtle.detect():
                        print("beg. quarrying dig")
                        if not self.dig(turtle.forward):
                            print("could not dig")
                            return False
                    if not self.nav.forward():
                        print("cannot move forward *?*")
                        return False

                if x != width - 1:

                    turn = (
                        self.nav.turn_right
                        if turn == self.nav.turn_left
                        else self.nav.turn_left
                    )

                    turn()

                    while turtle.detect():
                        if not self.dig(turtle.forward):
                            print("could not dig")
                            return False

                    if not self.nav.forward():
                        print("could not move forward *?*")
                        return False

                    turn()

            if z != height - 1:
                while turtle.detectDown():  # replace with dig function
                    if not self.dig(turtle.down):
                        print("could not dig")
                        return False
                if not self.nav.down():
                    print("could not move down")
                    return False

                turn()
                turn()
        return True


if len(args) < 3:
    print("usage: quarry <length> <width> <height>")
else:
    length, width, height = [int(x) for x in args[:3]]
    quarry = chest_quarry()
    quarry.quarry(length, width, height)
