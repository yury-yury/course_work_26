from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    "id": 1,
    "name": "топорик",
    "min_damage": 2.5,
    "max_damage": 4.1,
    "stamina_per_hit": 2
    pass


@dataclass
class Weapon:
    pass

    @property
    def damage(self):
        pass


@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    pass


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        # TODO возвращает объект оружия по имени
        pass

    def get_armor(self, armor_name) -> Armor:
        # TODO возвращает объект брони по имени
        pass

    def get_weapons_names(self) -> list:
        # TODO возвращаем список с оружием
        pass

    def get_armors_names(self) -> list:
        # TODO возвращаем список с броней
        pass

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        with open("./data/equipment.json", 'r', encoding='utf-8') as equipment_file:
            data = json.load(equipment_file)
        return data

        # equipment_schema = marshmallow_dataclass.class_schema( ... )
        # try:
        #     return equipment_schema().load(data)
        # except marshmallow.exceptions.ValidationError:
        #     raise ValueError

q = Equipment()
print(q.equipment)