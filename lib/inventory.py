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
    max_storage = 16
    position = None

    def __init__(self, position, max_storage):
        self.position = position
        self.max_storage = max_storage if max_storage else self.max_storage

    def is_full(self):
        if self.current_slot > self.max_storage:
            for _, count in self.items.values():
                if count < 64:
                    return False
            return True
        return False

    def is_full_item(self, name):
        if self.current_slot > self.max_storage:
            if name in self.items:
                return self.items[name][1] == 64
            return True
        return False

    def add_item(self, name, count):
        if self.is_full_item(name):
            return False

        if name not in self.items:
            self.items[name] = [self.current_slot, 0]
            self.current_slot += 1

        while count:
            if self.is_full_item(name):
                return False

            # If item slot has no space, update item storage
            if self.items[name][1] == 64:
                self.items[name] = [self.current_slot, 0]
                self.current_slot += 1

            # Quanity of item in item's slot
            slot_quantity = self.items[name][1]

            # Quantity we can drop in slot
            to_drop = 64 - slot_quantity  # Max quantity
            to_drop = to_drop if to_drop <= count else count

            # Drop to_drop into slot
            self.items[name][1] += to_drop
            count -= to_drop

        return True
