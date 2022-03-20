#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")
inv = import_file("/lib/inventory.py")
chests = import_file("/data/mongo_client.py")
refuel = import_file("/lib/fuel.py").refuel
move_to_inspect, move_to_dig = import_file("/data/movement.py").get_data()


# passing args is not working
args = [64, 64, 64]  # test


class chest_quarry:
    def __init__(self):
        self.nav = nav.nav()
        self.inventory = inv.turtleInventory(turtle)  # test - should be 16
        self.db = chests.chests()
        self.job = "chest_quarry_" + str(self.nav.locate())
        self.chest = self.put_chest(self.job)

    def put_chest(self, job):
        self.nav.turn_left()
        self.nav.turn_left()

        block = turtle.inspect()
        if block:
            if self.inventory.is_full_item(block["name"]):
                turtle.dig()
            else:
                self.inventory.dig(turtle.forward)

        if not self.inventory.place("minecraft:chest"):
            print("chest could not be placed")
            return None

        inventory = inv.inventory(
            1, self.nav.locate(), self.nav.direction
        )  # test - should be inventory_size
        self.db.insert(self.nav.locate(), self.nav.direction, job)

        self.nav.turn_left()
        self.nav.turn_left()

        return inventory

    def dig(self, turtle_direction):

        block = move_to_inspect[turtle_direction]()
        if block:
            self.inventory.print()  # test
            if not self.inventory.dig(turtle_direction):
                if self.chest.is_full_item(block["name"]):
                    print("creating new chest")
                    self.chest = self.put_chest(self.job)
                    if not self.chest:
                        print("chest could not be created")
                        return False
                    # remove turn by editing put_self.chest
                    direction = self.nav.direction
                    self.nav.turn_to(self.chest.direction)
                    refuel()
                    print("dropping")
                    for key in list(self.inventory.items.keys())[:]:
                        if key != "minecraft:chest":
                            self.inventory.drop(key, self.chest)
                    self.nav.turn_to(direction)
                    print("returning to original position")

                else:
                    print("going back to chest")
                    position = self.nav.locate()
                    direction = self.nav.direction
                    if not self.nav.path(self.chest.position):
                        print("chest could not be reached")
                        return False
                    self.nav.turn_to(self.chest.direction)
                    refuel()
                    print("dropping")
                    for key in list(self.inventory.items.keys())[:]:
                        if key != "minecraft:chest":
                            self.inventory.drop(key, self.chest)
                    if not self.nav.path(position):
                        print("return position could not be reached")
                        return False
                    self.nav.turn_to(direction)
                    print("returned to original position")
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

        if not self.chest:
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
