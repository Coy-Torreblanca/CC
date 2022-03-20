#!/usr/bin/env python3

from cc import import_file

inv = import_file("/lib/inventory.py")
nav = import_file("lib/nav.py")
chests = import_file("/data/mongo_client.py")
move_to_inspect, move_to_dig = import_file("/data/movement.py").get_data()


class chest_management:
    def __init__(self, job, nav, inventory, turtle):
        self.nav = nav
        self.db = chests.chests()
        self.job = job + "_" + str(self.nav.locate())
        self.chest = None
        self.inventory = inventory
        self.turtle = turtle

    def put_chest(self, double):

        if self.turtle.detect():
            self.inventory.dig()

        if not self.inventory.place("minecraft:chest"):
            print("chest could not be placed")
            return None

        inventory_size = 27

        if double:

            if self.inventory.search("minecraft:chest"):
                self.nav.turn_left()
                if self.turtle.detect():
                    self.turtle.dig()

                if self.nav.forward():
                    self.nav.turn_right()
                    if self.turtle.detect():
                        self.inventory.dig()
                    if self.inventory.place("minecraft:chest"):
                        inventory_size *= 2
                    self.nav.turn_left()
                    self.nav.back()
                self.nav.turn_right()

        inventory = inv.inventory(
            inventory_size, self.nav.locate(), self.nav.direction
        )  # test - should be inventory_size
        self.db.insert(self.nav.locate(), self.nav.direction, self.job)

        return inventory

    def drop_into_chest(
        self, new_chest_direction, new_chest_location, item_name, double, drop_exception
    ):
        starting_position = self.nav.locate()
        starting_direction = self.nav.direction

        if self.chest and self.chest.is_full_item(item_name):
            if not self.nav.path(new_chest_location):
                print("could not path to new chest location")
                return False

            self.nav.turn_to(new_chest_direction)
            new_chest = self.put_chest(double)
            if not new_chest:
                print("count not create new chest")
                return False

            self.chest = new_chest

        else:
            if not self.nav.path(self.chest.position):
                print("could not path to old chest")
                return False
            self.nav.turn_to(self.chest.direction)

        for item_name in list(self.inventory.items.keys())[:]:
            if item_name not in drop_exception:
                self.inventory.drop(item_name, self.chest)

        if not self.nav.path(starting_position):
            return False
        self.nav.turn_to(starting_direction)
        return True
