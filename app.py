from typing import Type, Optional
from flask import Flask, render_template, request, redirect, url_for, Response

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import PlayerUnit, EnemyUnit, BaseUnit


app: Flask = Flask(__name__)

heroes: dict[str, Optional[PlayerUnit, EnemyUnit]] = {"player": ..., "enemy": ...}

arena: Arena =  Arena()


@app.route("/")
def menu_page() -> str:
    """
    The view processes GET requests at the address '/' and loads the main menu of the application.
    """
    return render_template('index.html')


@app.route("/fight/")
def start_fight() -> str:
    """
    The view processes GET requests at "/fight/", executes the start_game function, and passes an instance
    of the arena class the necessary arguments.
    """
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)

@app.route("/fight/hit")
def hit() -> str:
    """
    The view processes GET requests at the address "/fight/hit", represents a strike button, updates
    the fight screen (strike) (template fight.html ), if the game is running, the player.hit() method
    of the arena class instance is called, if the game is not running, it skips the method triggering
    (just render the template with the current data)
    """
    if arena.game_is_running:
        result = arena.player_hit()
    if not arena.game_is_running:
        result = arena.battle_resault
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill() -> str:
    """
    The view processes GET requests at the address "/fight/use-skill", represents a skill use button,
    updates the battle screen (striking) (template fight.html ), if the game is running,
    the player.hit() method of the arena class instance is called, if the game is not running,
    it skips the method triggering (just render template with current data)
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
    if not arena.game_is_running:
        result = arena.battle_resault
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn() -> str:
    """
    The view processes GET requests at the address "/fight/pass-turn", represents the skip move button,
    updates the fight screen (template fight.html ), if the game is going on - calls the next move function
    (arena.next_turn()), if the game is not going on - skips triggering the method (just render
    the template with the current data).
    """
    if arena.game_is_running:
        result = arena.next_turn()
    if not arena.game_is_running:
        result = arena.battle_resault
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight() -> str:
    """
    The view processes GET requests at the address "/fight/end-fight", represents the end game button,
    navigates to the main menu.
    """
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero() -> Optional[str, Response]:
    """
    The view processes GET and POST requests at the address "/fight/choose-hero", is a form of selecting
    a character class and its equipment, with a POST request, data is stored and the transition
    to the choose enemy endpoint is carried out.
    """
    if request.method == 'GET':
        header = 'Выберите героя'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player.equip_armor(Equipment().get_armor(armor_name))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy() -> Optional[str, Response]:
    """
    The view processes GET and POST requests at the address "/fight/choose-enimy", is a form of selecting
    a character class and its equipment, with a POST request, data is stored and the transition
    to the start fight endpoint is carried out.
    """
    if request.method == 'GET':
        header = 'Выберите соперника'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.equip_armor(Equipment().get_armor(armor_name))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run(debug=True)
