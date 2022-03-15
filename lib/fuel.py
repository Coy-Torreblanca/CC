#!/usr/bin/env python3
from cc import turtle

fuel = {"minecraft:coal": 80, "minecraft:coal_block": 800}


def refuel():

    current_fuel_level = turtle.getFuelLevel()
    max_fuel_level = turtle.getFuelLimit()

    turtle.select(1)

    for slot in range(1, 17):

        turtle.select(slot)

        item = turtle.getItemDetail(slot)
        if item:
            item_name = item["name"]
        else:
            continue

        if item_name in fuel:

            item_count = turtle.getItemCount(slot)
            items_to_max_refuel = (max_fuel_level - current_fuel_level) / fuel[
                item_name
            ]
            refuel_count = (
                item_count if item_count < items_to_max_refuel else items_to_max_refuel
            )

            turtle.refuel(refuel_count)

            current_fuel_level += fuel[item_name] * refuel_count

            if current_fuel_level == max_fuel_level:
                break
