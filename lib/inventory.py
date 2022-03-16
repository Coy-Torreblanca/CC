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
