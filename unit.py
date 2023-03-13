from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional, Union


class BaseUnit(ABC):
    """
    The BaseUnit class is an abstract class defining the fields and methods of the game character,
    inherited from the ABC class of the abc library.
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        The __init__ function defines the method of the Unit class and generates the initial values of the fields
        of the instance of the class using the properties of the UnitClass class. Accepts as arguments the names
        of the character, in the form of a string, and an object of the UnitClass class.
        """
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Weapon = ...
        self.armor: Armor = ...
        self._is_skill_used: bool = False

    @property
    def health_points(self) -> float:
        """
        The health_points function defines the property method of the Unit class and allows you to get the value
        of the hp field of an instance of the class. Does not accept additional arguments, returns the value
        of the hp field in the form of float.
        """
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        """
        The stamina_points function defines the property method of the Unit class and allows you to get the value
        of the stamina field of an instance of the class. Does not accept additional arguments, returns the value
        of the stamina field in the form of float.
        """
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        """
        The equip_weapon function defines a method of the Unit class and allows you to assign a value to the weapon
        field of an instance of the class. Takes as an additional argument an object of the Weapon class, returns
        the result of executing the function as a string.
        """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        """
        The equip_armor function defines a method of the Unit class and allows you to assign the value of the armor
        field to an instance of the class. Takes an object of the Armor class as an additional argument, returns
        the result of executing the function as a string.
        """
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        """
        The _count_damage function defines a protected method of the Unit class. Accepts as an additional argument
        an instance of a player or opponent. It contains the logic of calculating the player's damage, taking into
        account the use of target armor, as well as a decrease in the attacker's stamina when hitting and a decrease
        in the defender's stamina when using armor. Returns the value of the damage done as a float.
        """
        self.stamina -= self.weapon.stamina_per_hit
        damage = self.weapon.damage * self.unit_class.attack
        if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor
        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: float):
        """
        The get_damage function defines a method of the Unit class. Takes the damage inflicted
        as an additional argument. Reduces health by the amount of damage inflicted.
        """
        if damage > 0:
            self.hp -= damage

    @abstractmethod
    def hit(self, target: Union[PlayerUnit, EnemyUnit]):
        """
        The hit function defines an abstract method of the Unit class, which must be redefined in child classes.
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        The use_skill function defines a method of the Unit class that implements the use of the skill.
        As an additional argument, it takes the opponent's object on which the skill is applied. If the skill
        was used earlier, it returns a message in the form of a string, otherwise it calls the use function
        of applying the skill and returns a string characterizing the performance
        of the skill returned by this function.
        """
        if self._is_skill_used:
            return 'Навык уже был использован'
        res = self.unit_class.skill.use(user=self, target=target)
        self._is_skill_used = True
        return res



class PlayerUnit(BaseUnit):
    """
    The PlayerUnit class represents the player class, inherited from the abstract BaseUnit class.
    The abstract method of the parent class is redefined in the class.
    """
    def hit(self, target: BaseUnit) -> str:
        """
        The hit function overrides the abstract method of the parent abstract class, represents the function
        of hitting the player, takes the opponent's object as an additional argument. Checks the sufficiency
        of the player's stamina to strike, calls the damage calculation function. Returns the result
        of the function execution as a string.
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает " \
                   f"{target.armor.name} соперника и наносит {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но " \
                   f"{target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):
    """
    The Enemy Unit class represents an enemy class inherited from the abstract BaseUnit class.
    The abstract method of the parent class is redefined in the class.
    """
    def hit(self, target: BaseUnit) -> str:
        """
        The hit function overrides the abstract method of the parent abstract class, represents the function
        of hitting the opponent, takes the player's object as an additional argument. Contains the logic
        of determining the possibility of using the opponent's skill. Checks the sufficiency of the player's
        stamina to strike, calls the damage calculation function. Returns the result of the function execution
        as a string.
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(1, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает " \
                   f"ваш(у) {target.armor.name} и наносит {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит вам удар, но " \
                   f"{target.armor.name} его останавливает."
