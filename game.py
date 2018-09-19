import copy
import random
import time

from Gear import *
from Mobs import *
from Events import *

score_lost_to_death = 3

yes_list = ["yes", "yeah", "sure", "why not", "y", ""]


def global_luck():
    return random.randint(1, 10)


def clean_armor(armor):
    return {k.rstrip(':'): v
            for k, v in armor.items() if k in {"Name:", "Attack:", "Defense:", "Type:"}}

class Player:

    score = 0
    kill_count = 0

    equipped_armor = {
        "Head Protection:": clean_armor(armor_head_rusty_cap),
        "Chest Protection:": clean_armor(armor_chest_rusty_mail),
        "Legs Protection:": clean_armor(armor_legs_rash_leggings),
    }

    HP = 20
    MP = 10
    gold = 0

    potions = {"Potions: ": [potion_hp["Name:"]]}

    def __init__(self, equipped_weapon = DEFAULT_WEAPON, equipped_armor = equipped_armor):
        self.name = "Cavalex"
        self.location = 0
        self.base_attack = 1
        self.base_defense = 0
        self.equipped_weapon = copy.deepcopy(equipped_weapon)
        self.equipped_armor = copy.deepcopy(equipped_armor)


    @property
    def ATTACK(self):
        return self.base_attack + self.equipped_weapon[add_attack]

    @property
    def ui_gold(self):
        return {"Gold: ": self.gold}

    @property
    def ui_equipped_weapon(self):
        return {"Equipped Weapon: {}".format(clean_armor(self.equipped_weapon)): ""}

    @property
    def inv(self):
        return [
            self.equipped_armor,
            self.ui_equipped_weapon,
            self.potions,
            self.ui_gold,
        ]

    def set_score(self):
        self.score += self.kill_count

    def status(self):
        print("Name: {}".format(self.name))
        print("HP: {}".format(self.HP))
        print("MP: {}".format(self.MP))
        print("Attack: {}".format(self.ATTACK))
        print("Defense: {}".format(player_defense_points()))

    def see_inventory(self):
        for element in self.inv:
            for k, v in element.items():
                if isinstance(v, list):
                    print(k, ' '.join(v))
                else:
                    print(k, v)

    COMMANDS = {  # I will add more as I improve the game
        "f": "fight",
        "r": "run",
        "s": "see stats",
        "i": "see inventory",
        "p": "to drink a potion"
    }


def armor_defense_points():
    return sum(value["Defense"] for key, value in player.equipped_armor.items())


def player_defense_points():
    return armor_defense_points() + player.base_defense + player.equipped_weapon[add_defense]


def add_gold(amount):
    player.gold += amount


# Adding to inventory:
def new_potion_to_inv(potion):
    player.potions["Potions: "].append(potion["Name:"])


def equip_weapon(new_weapon_code):
    eq_val = input(
        "Do you want to equip this weapon? ->( {} )<-\nNote that your current weapon ( {} ) will be discarded.\n-->".format(
            new_weapon_code["Name:"], player.equipped_weapon))
    if eq_val.lower() in yes_list:
        player.equipped_weapon = new_weapon_code
        print("Successfully equipped the {}.".format(new_weapon_code["Name:"]))
        print("The weapon you had was discarded.\n")
        time.sleep(0.5)
    else:
        print("The new weapon was discarded.")
        time.sleep(0.5)


def equip_armor(new_armor_code):
    if new_armor_code["Type:"] == "Head":
        eq_val = input(
            "Do you want to equip this armor in the {} slot? ->( {} )<-\nNote that your current armor, {} will be discarded.\n[y/n]-->".format(
                new_armor_code["Type:"], new_armor_code["Name:"], player.equipped_armor["Head Protection:"]))
        if eq_val.lower() in yes_list:
            player.equipped_armor["Head Protection:"] = clean_armor(new_armor_code)
            print("The armor you had was discarded.")
        else:
            print("The new armor was discarded.")
    if new_armor_code["Type:"] == "Chest":
        eq_val = input(
            "Do you want to equip this armor in the {} slot? ->( {} )<-\nNote that your current armor, {} will be discarded.\n[y/n]-->".format(
                new_armor_code["Type:"], new_armor_code["Name:"], player.equipped_armor["Chest Protection:"]))
        if eq_val.lower() in yes_list:
            player.equipped_armor["Chest Protection:"] = clean_armor(new_armor_code)
            print("The armor you had was discarded.")
        else:
            print("The new armor was discarded.")
    if new_armor_code["Type:"] == "Legs":
        eq_val = input(
            "Do you want to equip this armor in the {} slot? ->( {} )<-\nNote that your current armor, {} will be discarded.\n[y/n]-->".format(
                new_armor_code["Type:"], new_armor_code["Name:"], player.equipped_armor["Legs Protection:"]))
        if eq_val.lower() in yes_list:
            player.equipped_armor["Legs Protection:"] = clean_armor(new_armor_code)
            print("The armor you had was discarded.")
        else:
            print("The new armor was discarded.")


# Creating the player:
player = Player()


def commands():
    for command, action in player.COMMANDS.items():
        print('Press \"{}\" to {}'.format(command, action))


def print_quitting():
    print("Quitting...")
    time.sleep(1)


def quitting():
    player.set_score()
    print("\nGame Over! You ran back!")
    print("Your score is {}".format(player.score))
    print("You killed {} monsters.".format(player.kill_count))
    print_quitting()


def main():

    def mm_map():

        print("#####This is a game called \"Infinite Tower Climber Text RPG\" or simply \"InfiToClimber\" made by Cavalex.#####")
        print("### Credits to ShadowRanger for helping me code the player's inventory and functions related to it.")
        print("->Play --Press \"p\" or \"play\" to play")
        print("->Help --Press \"h\" or \"help\" for help")
        print("->Quit --Press \"q\" or \"quit\" to quit")
        ss = input("")
        if ss.lower() == "p" or ss.lower() == "play":
            print()
            main_loop()
        if ss.lower() == "h" or ss.lower() == "help":

            def help():
                print("\nIn this game you are an adventurer that's exploring a tower that has infinite height.")
                print("You will find monsters, and for each monster you kill you get 1 score.")
                print("Each \"attack round\" is the equivalent to 2 attacks,")
                print("and at the end of each attack round you can run and the game is over.")
                print("To calculate your damage, simply do Your Attack - Enemy's Defense, and vice-versa.")
                print("You also have 10% chance of dodging their attacks, and they yours!")
                print("If you die, you will loose {} points of score.".format(score_lost_to_death))
                print("As you kill monsters, you gain gold, weapons and armor")
                print("that will make you stronger in the long run.")
            help()
            print()
            mm_map()
        if ss.lower() == "q" or ss.lower() == "quit":
            print_quitting()
            exit()
        print("Invalid Input! Try again.")
        mm_map()
    mm_map()


def monster_encounter():
    global player_input
    if player.location == 1:
        print("Right at the entrance of the tower you spot something!")
        print("As an adventurer, you decide to go check it!...")
    if player.location < 10:
        mob = random.choice(ENEMIES_0_10)
    if 10 <= player.location < 20:
        mob = random.choice(ENEMIES_10_20)
    if player.location >= 20:
        mob = random.choice(ENEMIES_20_30)
    mob.HP = mob.MAXHEALTH
    print("You found a monster! It's {}!".format(mob.type))
    print("What do you want to do? ")
    commands()
    player_input = input("--> ")

    def wrong_command():
        global player_input
        while player_input not in player.COMMANDS:
            print("Invalid Input!")
            commands()
            player_input = input("--> ")
            while player_input == "s":
                print("\nThese are your stats:")
                player.status()
                print("\nWhat do you want to do now?")
                commands()
                player_input = input("--> ")
            while player_input == "i":
                print("\nYour inventory:")
                player.see_inventory()
                time.sleep(0.1)
                print("\nWhat do you want to do now?")
                commands()
                player_input = input("--> ")
            if player_input == "r":
                print()
                quitting()
                exit()
    while player_input != "f":
        while player_input == "s":
            print("\nThese are your stats:")
            player.status()
            print("\nWhat do you want to do now?")
            commands()
            player_input = input("--> ")
        wrong_command()
        while player_input == "i":
            print("\nYour inventory:")
            player.see_inventory()
            print("\nWhat do you want to do now?")
            commands()
            player_input = input("--> ")
        wrong_command()
        while player_input == "p":
            drink_potion()
            print("\nWhat do you want to do now?")
            commands()
            player_input = input("--> ")
        wrong_command()
        if player_input == "r":
            print()
            quitting()
            exit()
    if player_input == "f":
        print("\nYou decided to attack the monster:")
        print("Enemy's Type: {}".format(mob.name))
        print("Enemy's HP: {}/{}".format(mob.HP, mob.MAXHEALTH))
        print("Enemy's Attack: {}".format(mob.ATTACK))
        print("Enemy's Defense: {}".format(mob.DEFENSE))
        attack_tick = 0

        def attack():
            global charged_strike
            mob_dodged = False
            global_luck()
            if global_luck() == 1:
                mob_dodged = True
                print("Your Attack was dodged!")
            if not mob_dodged:
                damage = player.ATTACK - mob.DEFENSE
                if charged_strike:
                    damage += 1
                mob.HP -= damage
                if charged_strike:
                    print("Your Charged Strike has inflicted {} damage.".format(damage))
                else:
                    print("Your attack has inflicted {} damage.".format(damage))
            if mob.HP <= 0:
                print("You killed the {}. Press \"Enter\" to continue.".format(mob.name))
                player.kill_count += 1
                input("\n")
            else:
                if mob_dodged:
                    print("The {} still has {} HP.".format(mob.name, mob.HP))
                if not mob_dodged:
                    print("The {} now has {} HP.".format(mob.name, mob.HP))
                player_dodged = False
                global_luck()
                if global_luck() == 1:
                    player_dodged = True
                    print("You dodged the {} Attack!".format(mob.name))
                if not player_dodged:
                    global damage_received
                    damage_received = mob.ATTACK - player_defense_points()
                    if damage_received < 0:
                        damage_received = 0
                    player.HP -= damage_received
                if damage_received == 0 and not player_dodged:
                    print("You were able to block the monster's attack.")
                    print("You still have {} HP.".format(player.HP))
                if damage_received > 0 and not player_dodged:
                    print("The {} inflicted you {} damage.".format(mob.name, damage_received))
                print("You have {} HP.".format(player.HP))
        while True:
            global charged_strike
            charged_strike = False
            time.sleep(2)
            print("\nDo you want to use a charged strike for 1 MP that will add more 1 damage to your next attack?")
            ss = input("[y/n]-->")
            if ss.lower() in yes_list and player.MP > 0:
                charged_strike = True
                player.MP -= 1
            else:
                pass
            print("Attack Number {}:".format(attack_tick + 1))
            attack()
            attack_tick += 1
            if mob.HP <= 0:
                break
            if player.HP <= 0:
                player.set_score()
                player.score -= score_lost_to_death
                print("Game Over! You died!")
                print("Your score is {}".format(player.score))
                print("You killed {} monster(s).".format(player.kill_count))
                print_quitting()
                exit()
            if attack_tick % 2 == 0:
                time.sleep(0.5)
                print("\nDo you wish to run and loose the game now without loosing 2 score points?")
                print("Press anything to continue")
                run = input("Press \"r\" to run\n-->")
                if run.lower() == "r":
                    quitting()
                    exit()
                else:
                    continue
    if player_input == "r":
        print()
        quitting()
        exit()

def get_events():

    event_getter = random.randint(1, 10)
    if event_getter <= 3:
        event = random.choice(EVENTS)
        event()


def get_armor():
    armor_prob = random.randint(1, 5)
    if armor_prob == 1:
        print("\nYour inventory:")
        player.see_inventory()
        new_armor = random.choice(ARMOR)
        print("\nWhile climbing to the next floor you found a piece of armor on the ground.")
        print("The item is: {} and can be equipped in the {} Armor Slot.".format(clean_armor(new_armor), new_armor["Type:"]))
        equip_armor(new_armor)


def get_weapon():
    weapon_prob = random.randint(1, 5)
    if weapon_prob == 1:
        print("\nYour inventory:")
        player.see_inventory()
        new_weapon = random.choice(WEAPONS)
        print("\nWhile climbing to the next floor you found a weapon on the ground.")
        print("The item is: {} and can be equipped in exchange for your current weapon.".format(new_weapon))
        equip_weapon(new_weapon)


def drink_potion():
    print("\nThese are your potions:")
    print(player.potions)
    potion_input = input("To drink a potion write its name here: -->")
    if potion_input.lower() == "hp potion" or potion_input.lower() == "hp":
        if potion_hp["Name:"] in player.potions["Potions: "]:
            print("It will add {} HP and is going to be discarded, are you sure?".format(potion_hp[add_HP]))
            sure = input("[y/n]-->")
            if sure.lower() in yes_list:
                player.potions["Potions: "].remove(potion_hp["Name:"])
                player.HP += potion_hp[add_HP]
    if potion_input.lower() == "mp potion" or potion_input.lower() == "mp":
        if potion_mp["Name:"] in player.potions["Potions: "]:
            print("It will add {} MP and is going to be discarded, are you sure?".format(potion_mp[add_MP]))
            sure = input("[y/n]-->")
            if sure.lower() in yes_list:
                player.potions["Potions: "].remove(potion_mp["Name:"])
                player.MP += potion_mp[add_MP]


# Game Loop
def main_loop():
    while player.HP > 0:
        while player.location == 0:
            player.name = input("What's your name, adventurer? ")
            print("You are {}, an adventurer exploring a tower that reaches up to the sky!".format(player.name))
            time.sleep(0.3)
            print("You decide to investigate it with hopes of coming back with great tales and fortunes!")
            time.sleep(0.3)
            print("The game will begin, to continue press \"Enter\", or anything else.")
            beg = input("--> ")
            player.location += 1
        print()
        monster_encounter()

        gold_variable = random.randint(5, 25)
        add_gold(gold_variable)
        print("The monster dropped {} gold.".format(gold_variable))

        if player.HP <= 0:
            player.set_score()
            player.score -= score_lost_to_death
            print("Game Over! You died!")
            print("Your score is {}".format(player.score))
            print("You killed {} monster(s).".format(player.kill_count))
            print_quitting()
            exit()

        print("\nYou decided to continue your journey inside the dungeon...")
        get_events()
        get_armor()
        get_weapon()

        print("\n###################################################")
        print("\nYou recovered 1 HP by going to the next level.")
        player.HP += 1
        player.location += 1
        print("You are now at the dungeon's level {}.".format(player.location))
        print("\nThese are your stats:")
        player.status()
        time.sleep(2)


if __name__ == "__main__":
    main()
