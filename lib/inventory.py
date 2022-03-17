#!/usr/bin/env python3

from cc import turtle

# Drop all items in inventory except for any item found in exceptions.
def drop_all(execptions):

    for slot in range(1, 17):
        turtle.select(slot)
        item = turtle.getItemDetail()
        if item:
            if item["name"] in exceptions:
                continue

        turtle.drop()


def search(search_item):

    for slot in range(1, 17):
        turtle.select(slot)
        item = turtle.getItemDetail()
        if item:
            if item["name"] == search_item:
                return True
        return False


def is_full():
    for i in range(1, 17):
        turtle.select(slot)
        if not turtle.getItemDetail():
            return False
    return True


class inventory:
    items = {}
    current_slot = 0
    position = None

    def __init__(self, position):
        self.position = position

    def is_full(self):
        if self.current_slot > 16:
            for _, count in self.items.values():
                if count < 64:
                    return False
            return True
        return True

    def is_full_item(self, name):
        if self.current_slot > 16:
            if self.items[name][1] == 64:
                return True
        return False

    def add_item(self, name, count):
        if self.is_full_item(name):
            return False

        while count:
            if name in self.items:
                slot_quantity = self.items[name][1]
                to_drop = 64 - slot_quantity
                to_drop = to_drop if to_drop <= count else count
                self.items[name][1] += to_drop
                if self.items[name][1] == 64:
                    self.items[name][0] = self.current_slot
                    self.current_slot += 1
                count -= to_drop
                if self.is_full_item(name):
                    return count == 0
            else:
                self.items[name] = [self.current_slot, 0]
                self.current_slot += 1
        return True
