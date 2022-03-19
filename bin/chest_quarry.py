#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")
inv = import_file("/lib/inventory.py")


def error(message):
    print(error)


class chest_quarry:
    def __init__(self):
        self.nav = nav.nav()
        self.chest = self.put_chest()
        self.chests = [self.chest]
        self.inventory = inv.turtleInventory(turtle)  # test - should be 16

    def put_chest(self):
        # 1. check stack functionality by removing argumetn
        if not inv.search("minecraft:chest"):
            error("No chest to place")
            return None

        self.nav.turn_left()
        self.nav.turn_left()

        if turtle.detect():
            turtle.dig()

        if not turtle.place():
            error("chest could not be placed")
            return None

        inventory_size = 27

        if inv.search("minecraft:chest"):
            self.nav.turn_left()
            if turtle.detect():
                turtle.dig()

            if self.nav.forward():
                self.nav.turn_right()
                if turtle.detect():
                    turtle.dig()
                if turtle.place():
                    inventory_size *= 2
                    self.nav.turn_left()
                    self.nav.back()
            self.nav.turn_right()

        inventory = inv.inventory(
            1, self.nav.locate(), self.nav.direction
        )  # test - should be inventory_size
        self.nav.turn_left()
        self.nav.turn_left()

        return inventory

    def dig(self):

        block = turtle.inspect()
        if block:
            self.inventory.print()  # test
            if not self.inventory.dig():
                if self.chest.is_full_item(block["name"]):
                    self.chest = self.put_chest()
                    if not self.chest:
                        print("chest could not be created")
                        return False
                    self.chests = [self.chest] + self.chests
                    # remove turn by editing put_self.chest
                    direction = self.nav.direction
                    self.nav.turn_to(self.chest.direction)
                    for key in list(self.inventory.keys())[:]:
                        self.inventory.drop(key, chest)
                    self.nav.turn_to(direction)

                else:
                    position = self.nav.locate()
                    direction = self.nav.direction
                    if not self.nav.path(self.chest.position):
                        print("chest could not be reached")
                        return False
                    self.nav.turn_to(self.chest.direction)
                    for key in list(self.inventory.keys())[:]:
                        self.inventory.drop(key, chest)
                    if not self.nav.path(position):
                        print("return position could not be reached")
                        return False
                    self.nav.turn_to(direction)
                block = turtle.inspect()
                if block:
                    self.inventory.print()  # test
                    self.inventory.dig()

    def quarry(self, length, width, height):

        if not self.nav.direction_test_pass:
            error("direction test pass failed")
            return False

        if not self.chest:
            print("chest could not be placed")
            return False

        turn = self.nav.turn_left

        for z in range(height):
            for x in range(width):
                for y in range(length - 1):

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


# passing args is not working
args = [6, 6, 6]  # test

if len(args) < 3:
    print("usage: quarry <length> <width> <height>")
else:
    length, width, height = [int(x) for x in args[:3]]
    quarry = chest_quarry()
    quarry.quarry(length, width, height)
