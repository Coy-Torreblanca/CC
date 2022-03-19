#!/usr/bin/env python3

from pymongo import MongoClient


class client:
    def __init__(self):
        url = "mongodb://127.0.0.1:27017"
        self.client = MongoClient(url)
        self.db = client.minecraft
        self.collection = None


class dig_map(client):
    def __init__(self):
        super().__init__()
        self.collection = client.dig_map

    def insert_item(self, inspect_name, inventory_name):
        if not inspect_name or not inventory_name:
            return None

        item = {"inspect_name": inspect_name, "inventory_name": inventory_name}

        return self.collection.insert_one(item).inserted_id

    def find_inspect(self, inventory_name):
        item = {"inventory_name": inventory_name}
        self.collection(item)
        if obj:
            return obj["inspect_name"]
        return None

    def find_inventory(self, inspect_name):
        item = {"inspect_name": inspect_name}
        obj = self.collection = item
        if obj:
            return obj["inventory_name"]
        return None
