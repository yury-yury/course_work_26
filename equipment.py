from dataclasses import dataclass
from typing import Optional, List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    """
    The Armor class is a dataclass that defines the type and value of all armor attributes.
    """
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    """
    The Weapon class is a dataclass that defines the type and value of all attributes of a character's weapon.
    """
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        """
        The damage function implements the property method of the Weapon class, does not accept arguments,
        when called, returns a random weapon damage value from a specified range, rounded to one decimal place.
        """
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    """
    The Equipment Data class is a data class that defines the list and type of attributes of its instance.
    Used to load data.
    """
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    """
    The Equipment class is designed to load and form objects of armor and weapons used by the characters of the game.
    Contains all the necessary methods.
    """
    def __init__(self):
        """
        The "__init__" method is called when initializing the class object and generates the class attribute
        by calling the data loading method from an external file.
        """
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        """
        The get_weapon function defines a method of the Equipment class, takes the name of the weapon
        as a string as an argument, and returns the requested type of weapon as an instance of the Weapon class.
        """
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name: str) -> Armor:
        """
        The get_armor function defines a method of the Equipment class, takes as an argument the name of the armor
        as a string and returns the requested type of armor as an instance of the Armor class.
        """
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor

    def get_weapons_names(self) -> List[str]:
        """
        The get_weapons_names function defines a method of the Equipment class, does not accept arguments,
        and when called generates and returns the names of all available weapons, in the form of a list of strings.
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> List[str]:
        """
        The get_armors_names function defines a method of the Equipment class, does not accept arguments,
        and when called generates and returns the names of all available types of armor,
        in the form of a list of strings.
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """
        The _get_equipment_data function defines a protected method of the Equipment class, does not accept arguments,
        and when called loads data from an external file, forms an object of the EquipmentData class.
        """
        with open("./data/equipment.json", 'r', encoding='utf-8') as equipment_file:
            data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
