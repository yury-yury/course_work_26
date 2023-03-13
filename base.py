from typing import Optional

from unit import PlayerUnit, EnemyUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """
    The Arena class implements the interaction of all game objects, and contains the basic logic.
    When initializing the class object, it determines the initial values of the arguments,
    does not accept any parameters.
    """
    STAMINA_PER_ROUND: float = 1
    player: PlayerUnit = ...
    enemy: EnemyUnit = ...
    game_is_running: bool = False
    battle_resault: Optional[str] = None

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit):
        """
        The start_game function defines a method of the Arena class, when called, it takes as arguments
        a player and an opponent in the form of objects of classes inherited from the abstract BaseUnit class.
        When called, it assigns the attributes "player" and "opponent" to the instance of the class,
        and also sets True for the "has the game started" property.
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """
        The _check_players_hp function defines a protected method of the Arena class, does not accept
        arguments when called. Checks the hp attribute values of the player and the opponent.
        Based on the results of the check, it returns None if both values are greater than zero,
        otherwise it determines the outcome of the battle and calls the _end_game method.
        """
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_resault = 'Ничья'
        elif self.player.hp <= 0:
            self.battle_resault = 'Игрок проиграл битву'
        else:
            self.battle_resault = 'Игрок выиграл битву'
        self._end_game()

    def _stamina_regeneration(self):
        """
        The _stamina_regeneration function defines a protected method of the Arena class, does not accept
        arguments when called. Increases the values of stamina attributes of player and opponent objects.
        Checks that the values do not exceed the maximum value.
        """
        units = (self.player, self.enemy)
        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        """
        The next_turn function defines a method of the Arena class, does not accept arguments when called.
        It is called when the player performs some action, Checks the value returned by the _check_players_hp method,
        if the method returned the result, it returns it, Otherwise it calls the _stamina_regeneration method,
        and then enemy.hit with passing to it as an argument an instance of the player to perform a response move.
        """
        if self.game_is_running:
            self._stamina_regeneration()
            result = self.enemy.hit(self.player)

            res = self._check_players_hp()
            if res is not None:
                return res

            return result

    def _end_game(self) -> str:
        """
        The _end_game function defines a protected method of the Arena class, does not accept arguments when called.
        Cleans singleton, stops the game and returns the result of the battle.
        """
        self._instances: dict = {}
        self.game_is_running = False
        return self.battle_resault

    def player_hit(self) -> str:
        """
        The player_hit function defines a method of the Arena class, does not accept arguments when called.
        Retrieves the result of the player.hit function, starts the next move and returns
        the result of the player's action.
        """
        result = self.player.hit(self.enemy)

        res = self._check_players_hp()
        if res is not None:
            return res

        turn_result = self.next_turn()

        return f'{result}<br>{turn_result}'

    def player_use_skill(self) -> str:
        """
        The player_use_skill function defines a method of the Arena class, does not accept arguments when called.
        Retrieves the result of the player.use_skill function, starts the next move and returns
        the result of the player's action.
        """
        result = self.player.use_skill(self.enemy)

        res = self._check_players_hp()
        if res is not None:
            return res

        turn_result = self.next_turn()

        return f'{result}<br>{turn_result}'
