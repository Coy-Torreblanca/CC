#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py").nav()
inv = import_file("/lib/inventory.py")


def error(message):
    print(error)


class chest_quarry:
    def put_chest(self):
        # 1. check stack functionality by removing argumetn
        if not inv.search("minecraft:chest"):
            error("No chest to place")
            return False

        self.nav.turn_left()
        self.nav.turn_left()

        if turtle.detect():
            turtle.dig()

        if not turtle.place():
            error("chest could not be placed")
            return False

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

        self.inventory = inv.inventory(
            1, self.nav.locate(), nav.direction
        )  # test - should be inventory_size
        self.nav.turn_left()
        self.nav.turn_left()

        return True

    def dig(self):

        block = turtle.inspect()
        if block:
            self.inventory.print()  # test
            if not self.inventory.is_full_item(block["name"]):
                turtle.dig()
                self.inventory.add_item(block["name"], 1)
            else:
                if self.chest.is_full_item(block["name"]):
                    self.chest = self.put_chest(self.nav)
                    if not self.chest:
                        print("self.chest could not be created")
                        return False
                    self.chests = self.chest + self.chests
                    # remove turn by editing put_self.chest
                    direction = self.nav.direction
                    self.nav.turn_to(self.chest.direction)
                    for slot in range(1, 17):
                        # TEST dont drop test
                        turtle.select(slot)
                        item = turtle.getItemDetail()
                        if not item:
                            continue
                        name = turtle.getItemDetail()["name"]
                        count = turtle.getItemDetail()["count"]
                        turtle.drop()
                        # personal invenotry not upd ated
                        self.chest.add_item(name, count)
                    self.nav.turn_to(direction)

                else:
                    position = self.nav.locate()
                    direction = self.nav.direction
                    if not self.nav.path(self.chest.position):
                        print("chest could not be reached")
                        return False
                    self.nav.turn_to(self.chest.direction)
                    for slot in range(1, 17):
                        turtle.select(slot)
                        item = turtle.getItemDetail()
                        if not item:
                            continue
                        name = turtle.getItemDetail()["name"]
                        count = turtle.getItemDetail()["count"]
                        turtle.drop()  # you don't drop from inv
                        self.chest.add_item(name, count)
                    if not self.nav.path(position):
                        print("return position could not be reached")
                        return False
                    self.nav.turn_to(direction)
                block = turtle.inspect()
                if block:
                    self.inventory.print()  # test
                    if not self.inventory.is_full_item(block["name"]):
                        turtle.dig()
                        self.inventory.add_item(block["name"], 1)
                    else:
                        error("self.inventory full *?*")
                        return False

    def quarry(self, length, width, height):

        if not nav.direction_test_pass:
            error("direction test pass failed")
            return False

        self.inventory = inv.inventory(1)  # test - should be 16
        self.chest = put_chest(nav)
        self.chests = [chest]

        if not self.chest:
            print("chest could not be placed")
            return False

        turn = nav.turn_left

        for z in range(height):
            for x in range(width):
                for y in range(length - 1):

                    dig()
                    if not nav.forward():
                        print("cannot move forward *?*")
                        return False

                if x != width - 1:

                    turn = nav.turn_right if turn == nav.turn_left else nav.turn_left

                    turn()

                    dig()

                    if not nav.forward():
                        print("could not move forward *?*")
                        return False

                    turn()

            if z != height - 1:
                if turtle.detectDown():  # replace with dig function
                    turtle.digDown()

                if not nav.down():
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
