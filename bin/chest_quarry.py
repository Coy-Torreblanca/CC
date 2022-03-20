#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")
inv = import_file("/lib/inventory.py")
chests = import_file("/data/mongo_client.py")
refuel = import_file("/lib/fuel.py").refuel


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

        if turtle.detect():
            self.inventory.dig()

        if not self.inventory.place("minecraft:chest"):
            print("chest could not be placed")
            return None

        inventory_size = 27

        if self.inventory.search("minecraft:chest"):
            self.nav.turn_left()
            if turtle.detect():
                turtle.dig()

            if self.nav.forward():
                self.nav.turn_right()
                if turtle.detect():
                    self.inventory.dig()
                if self.inventory.place("minecraft:chest"):
                    inventory_size *= 2
                    self.nav.turn_left()
                    self.nav.back()
            self.nav.turn_right()

        inventory = inv.inventory(
            1, self.nav.locate(), self.nav.direction
        )  # test - should be inventory_size
        self.db.insert(self.nav.locate(), self.nav.direction, job)

        self.nav.turn_left()
        self.nav.turn_left()

        return inventory

    def dig(self):

        block = turtle.inspect()
        if block:
            self.inventory.print()  # test
            if not self.inventory.dig():
                if self.chest.is_full_item(block["name"]):
                    self.chest = self.put_chest(self.job)
                    if not self.chest:
                        print("chest could not be created")
                        return False
                    # remove turn by editing put_self.chest
                    direction = self.nav.direction
                    self.nav.turn_to(self.chest.direction)
                    refuel()
                    for key in list(self.inventory.items.keys())[:]:
                        if key != "minecraft:chest":
                            self.inventory.drop(key, self.chest)
                    self.nav.turn_to(direction)

                else:
                    position = self.nav.locate()
                    direction = self.nav.direction
                    if not self.nav.path(self.chest.position):
                        print("chest could not be reached")
                        return False
                    self.nav.turn_to(self.chest.direction)
                    refuel()
                    for key in list(self.inventory.items.keys())[:]:
                        if key != "minecraft:chest":
                            self.inventory.drop(key, self.chest)
                    if not self.nav.path(position):
                        print("return position could not be reached")
                        return False
                    self.nav.turn_to(direction)
                block = turtle.inspect()
                if block:
                    self.inventory.print()  # test
                    self.inventory.dig()

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
                        self.dig()
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
                        self.dig()

                    if not self.nav.forward():
                        print("could not move forward *?*")
                        return False

                    turn()

            if z != height - 1:
                if turtle.detectDown():  # replace with dig function
                    turtle.digDown()

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
