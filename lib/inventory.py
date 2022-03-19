#!/usr/bin/env python3

from cc import turtle, fs, import_file

mongo = import_file("/data/mongo_client.py")

# TODO: add drop
# grass -> dirt problem
# inspect to dig dictionary

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


def error(message):
    print(message)


class inventory:
    items = {}
    current_slot = 1
    max_storage = 0
    position = None
    direction = None

    def __init__(self, max_storage=16, position=None, direction=None):
        self.position = position
        self.direction = direction
        self.max_storage = max_storage

    def is_full(self):
        if self.current_slot >= self.max_storage:
            for _, count in self.items.values():
                if count < 64:
                    return False
            return True
        return False

    def is_full_item(self, name):
        if self.current_slot >= self.max_storage:
            if name in self.items:
                return self.items[name][1] == 64
            return True
        return False

    def add_item(self, name, count=1):

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

                self.current_slot += 1
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

    def print(self):

        with fs.open("inventory_print", "w") as f:

            f.writeLine("current_slot: " + str(self.current_slot))
            for name in self.items:

                slot, count = self.items[name]
                f.writeLine(name + " " + str(slot) + " " + str(count))


class turtleInventory(inventory):
    def __init__(self, turtle, position, direction):

        super().__init__(16, position, direction)
        self.turtle = turtle
        self.db = mongo.dig_map()

    def search(self, item_name):
        for slot in range(self.max_storage, 0, -1):
            item = self.turtle.getItemDetail(slot)
            if item_name == item["name"]:
                return slot
        return None

    # Assume that there are no empty slots in between occupied slots.
    # Assume that stacks are full as possible
    def check_turtle_inventory(self):

        self.items = {}
        self.current_slot = 1

        for slot in range(1, 17):

            self.turtle.select(slot)
            item = self.turtle.getItemDetail()

            if item:

                name = item["name"]
                count = item["count"]

                if not self.add_item(name, count):

                    error("adding item to inventory failed")
                    return False
            else:

                return True

    def dig(self):

        block = self.turtle.inspect()

        if not block:

            return False

        inventory_name = self.db.find_inventory(block["name"])

        if inventory_name:

            return self.add_item(inventory_name)

        if self.is_full():

            return False

        self.turtle.dig()

        self.turtle.select(self.current_slot)

        item = self.turtle.getItemDetail()

        if not item:

            error("Item selected should exist")
            return False

        self.db.find_inventory(
            {"inspect_name": inventory_name, "inventory_name": item["name"]}
        )

        if not self.add_item(item["name"]):

            error("Adding item should succeed")
            return False

        return True

    def drop(self, item_name, count=(self.max_storage * 64)):

        while count:

            item = self.items[item_name]

            if item not in self.items[item_name]:
                return True

            # Get slot of item to drop
            drop_slot = item[0]
            # Calculate number to drop from this slot
            drop_count = item[1] if item[1] < count else count

            # Drop Item
            self.turtle.select(drop_slot)
            self.turtle.drop(drop_count)
            count -= drop_count

            # Update inventory so there are no empty slots between full ones
            if self.current_slot - 1 == drop_slot:
                self.current_slot = drop_slot
            else:
                self.turtle.select(self.current_slot - 1)
                self.turtle.transferTo(drop_slot)
                self.current_slot -= 1

            # Update inventory dictionary
            slot = self.search(item_name)
            if not slot:
                del self.items[item_name]
                return True
            else:
                item = turtle.getItemDetail(slot)
                self.items[item_name] = [slot, item["count"]]

            if not count:
                return True
            # if item current slot is empty,
            # go to current  slot - 1
            # move items from there to emptyd slot
            # update item dictionary
            # current slot -= 1
