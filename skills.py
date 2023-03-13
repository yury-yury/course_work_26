from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit

class Skill(ABC):
    """
    The Skill class is an abstract class inherited from the ABC class of the abc library and defines the attributes
    and methods necessary for all classes inherited from it.
    """
    user: BaseUnit = ...
    target: BaseUnit = ...

    @property
    @abstractmethod
    def name(self):
        """
        The name function defines an abstract property method of the class and must be redefined
        in all inherited classes.
        """
        pass

    @property
    @abstractmethod
    def stamina(self):
        """
        The stamina function defines an abstract property method of the class and must be redefined
        in all inherited classes.
        """
        pass

    @property
    @abstractmethod
    def damage(self):
        """
        The damage function defines an abstract property method of the class and must be redefined
        in all inherited classes.
        """
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        """
        The skill_effect function defines an abstract method of the class and must be redefined
        in all inherited classes.
        """
        pass

    def _is_stamina_enough(self) -> bool:
        """
        The _is_stamina_enough function defines a protected method of the class, does not accept arguments,
        compares the available stamina of the character with the required amount for the use of the skill.
        Returns True if stamina is sufficient, otherwise False.
        """
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        The use function defines the class method, takes as arguments the player character and the opponent character
        in the form of objects of the corresponding classes, compares the available endurance of the character
        with the required amount for the use of the skill, by calling the protected method _is_stamina_enough.
        If the value is sufficient, it applies the skill, otherwise it returns a string with a message.
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    """
    The FuryPunch class inherits from the abstract Skill class and contains overrides of the abstract fields
    and methods of the parent class.
    """
    name = 'Свирепый пинок'
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        """
        The skill_effect function overrides the method of the parent abstract class Skill. Does not accept arguments.
        Produces a decrease in the player's stamina and a decrease in the opponent's health after applying the skill.
        Returns the result as a string.
        """
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'

class HardShot(Skill):
    """
    The HardShot class inherits from the abstract Skill class and contains overrides of the abstract fields
    and methods of the parent class.
    """
    name = 'Мощный укол'
    stamina = 5
    damage = 15

    def skill_effect(self) -> str:
        """
        The skill_effect function overrides the method of the parent abstract class Skill. Does not accept arguments.
        Produces a decrease in the player's stamina and a decrease in the opponent's health after applying the skill.
        Returns the result as a string.
        """
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'
