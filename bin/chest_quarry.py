#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")
inv = import_file("/lib/inventory.py")

# chest: "minecraft:chest"

# passing args is not working
args = [0, 0, 0]


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
        if nav.forward():
            nav.turn_right()
            if turtle.detect():
                turtle.dig()
            turtle.place()
            inventory_size *= 2
            nav.turn_left()
            nav.back()
        nav.turn_right()

    nav.turn_left()
    nav.turn_left()
    return inv.inventory(inventory_size, nav.locate(), nav.direction)


def quarry(length, width, height):

    nav = nav.nav()
    if not nav.direction_test_pass:
        return False

    inventory = inv.inventory(16)
    chest = put_chest(nav)
    chests = [chest]

    if not chest:
        return False

    turn = nav.turn_left

    for z in range(height):
        for x in range(width):
            for y in range(length - 1):

                block = turtle.inspect()
                if block:
                    if not inventory.is_full_item(block["name"]):
                        turtle.dig()
                    else:
                        if chest.is_full_item(block["name"]):
                            chest = put_chest(nav)
                            if not chest:
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
                                return False
                            nav.turn_to(chest.direction)
                            for slot in range(1, 17):
                                turtle.select(slot)
                                name = turtle.getItemDetail()["name"]
                                count = turtle.getItemDetail()["count"]
                                turtle.drop()
                                chest.add_item(name, count)
                            if not nav.path(position):
                                return False
                            nav.turn_to(direction)

                if not nav.forward():
                    return False

            if x != width - 1:

                turn = nav.turn_right if turn == nav.turn_left else nav.turn_left

                turn()

                block = turtle.inspect()
                if block:
                    if not inventory.is_full_item(block["name"]):
                        turtle.dig()
                    else:
                        if chest.is_full_item(block["name"]):
                            chest = put_chest(nav)
                            if not chest:
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
                                return False
                            nav.turn_to(chest.direction)
                            for slot in range(1, 17):
                                turtle.select(slot)
                                name = turtle.getItemDetail()["name"]
                                count = turtle.getItemDetail()["count"]
                                turtle.drop()
                                chest.add_item(name, count)
                            if not nav.path(position):
                                return False
                            nav.turn_to(direction)

                if not nav.forward():
                    return False

                turn()

        if z != height - 1:
            if turtle.detectDown():
                turtle.digDown()

            if not nav.down():
                return False

            turn()
            turn()


if len(args) < 3:
    print("usage: quarry <length> <width> <height>")
else:
    length, width, height = [int(x) for x in args[:3]]
    quarry(length, width, height)
