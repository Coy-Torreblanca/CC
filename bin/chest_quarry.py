#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py").nav()
inv = import_file("/lib/inventory.py")

# chest: "minecraft:chest"

# passing args is not working
args = [6, 6, 6]  # test


def put_chest(nav):
    if not inv.search("minecraft:chest"):
        return None

    nav.turn_left()
    nav.turn_left()

    if turtle.detect():
        turtle.dig()

    turtle.place()

    inventory_size = 27

    if inv.search("minecraft:chest"):
        nav.turn_left()
        if turtle.detect():
            turtle.dig()

        if nav.forward():
            nav.turn_right()
            if turtle.detect():
                turtle.dig()
            turtle.place()
            inventory_size *= 2
            nav.turn_left()
            nav.back()
        nav.turn_right()

    return inv.inventory(
        1, nav.locate(), nav.direction
    )  # test - should be inventory_size
    nav.turn_left()
    nav.turn_left()


def error(message):
    print(error)


def quarry(length, width, height):

    if not nav.direction_test_pass:
        error("direction test pass failed")
        return False

    inventory = inv.inventory(1)  # test - should be 16
    chest = put_chest(nav)
    chests = [chest]

    if not chest:
        print("chest could not be placed")
        return False

    turn = nav.turn_left

    for z in range(height):
        for x in range(width):
            for y in range(length - 1):
                block = turtle.inspect()
                if block:
                    inventory.print()  # test
                    if not inventory.is_full_item(block["name"]):
                        turtle.dig()
                        inventory.add_item(block["name"], 1)
                    else:
                        if chest.is_full_item(block["name"]):
                            chest = put_chest(nav)
                            if not chest:
                                print("chest could not be created")
                                return False
                            chests = chest + chests
                            # remove turn by editing put_chest
                            direction = nav.direction
                            nav.turn_to(chest.direction)
                            for slot in range(1, 17):
                                # TEST dont drop test
                                turtle.select(slot)
                                item = turtle.getItemDetail()
                                if not item:
                                    continue
                                name = turtle.getItemDetail()["name"]
                                count = turtle.getItemDetail()["count"]
                                turtle.drop()
                                chest.add_item(name, count)
                            nav.turn_to(direction)

                        else:
                            position = nav.locate()
                            direction = nav.direction
                            if not nav.path(chest.position):
                                print("chest could not be reached")
                                return False
                            nav.turn_to(chest.direction)
                            for slot in range(1, 17):
                                turtle.select(slot)
                                item = turtle.getItemDetail()
                                if not item:
                                    continue
                                name = turtle.getItemDetail()["name"]
                                count = turtle.getItemDetail()["count"]
                                turtle.drop()
                                chest.add_item(name, count)
                            if not nav.path(position):
                                print("return position could not be reached")
                                return False
                            nav.turn_to(direction)

                if not nav.forward():
                    print("cannot move forward *?*")
                    return False

            if x != width - 1:

                turn = nav.turn_right if turn == nav.turn_left else nav.turn_left

                turn()

                block = turtle.inspect()
                if block:
                    # debug
                    inventory.print()
                    if not inventory.is_full_item(block["name"]):
                        turtle.dig()
                        inventory.add_item(block["name"], 1)
                    else:
                        if chest.is_full_item(block["name"]):
                            chest = put_chest(nav)
                            if not chest:
                                print("could not place chest")
                                return False
                            chests = chest + chests
                            # remove turn by editing put_chest
                            direction = nav.direction
                            nav.turn_to(chest.direction)
                            for slot in range(1, 17):
                                turtle.select(slot)
                                name = turtle.getItemDetail()["name"]
                                count = turtle.getItemDetail()["count"]
                                turtle.drop()
                                chest.add_item(name, count)
                            nav.turn_to(direction)

                        else:
                            position = nav.locate()
                            direction = nav.direction
                            if not nav.path(chest.position):
                                print("could not path to chest")
                                return False
                            nav.turn_to(chest.direction)
                            for slot in range(1, 17):
                                turtle.select(slot)
                                name = turtle.getItemDetail()["name"]
                                count = turtle.getItemDetail()["count"]
                                turtle.drop()
                                chest.add_item(name, count)
                            if not nav.path(position):
                                print("could not move back to position")
                                return False
                            nav.turn_to(direction)

                if not nav.forward():
                    print("could not move forward *?*")
                    return False

                turn()

        if z != height - 1:
            if turtle.detectDown():
                turtle.digDown()

            if not nav.down():
                print("could not move down")
                return False

            turn()
            turn()
    return True


if len(args) < 3:
    print("usage: quarry <length> <width> <height>")
else:
    length, width, height = [int(x) for x in args[:3]]
    quarry(length, width, height)
