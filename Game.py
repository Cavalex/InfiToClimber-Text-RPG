import copy
import random
import time

from Gear import *
from Mobs import *

score_lost_to_death = 3

yes_list = ["yes", "yeah", "sure", "why not", "y", ""]
yes_list_without_enter = ["yes", "yeah", "sure", "why not", "y"]


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
        "p": "drink a potion"
    }


def armor_defense_points():
    return round(sum(value["Defense"] for key, value in player.equipped_armor.items()), 3)


def player_defense_points():
    return round(armor_defense_points() + player.base_defense + player.equipped_weapon[add_defense], 3)


def add_gold(amount):
    player.gold += amount


# Adding to inventory:
def new_potion_to_inv(potion):
    player.potions["Potions: "].append(potion["Name:"])


def equip_weapon(new_weapon_code):
    eq_val = input(
        "Do you want to equip this weapon? ->( {} )<-\nNote that your current weapon ( {} ) will be discarded.\n[y/n]-->".format(
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


fight_beginning = 0


def monster_encounter():
    global player_input
    global mob
    global fight_beginning
    if fight_beginning == 0:
        if player.location == 1:
            print("Right at the entrance of the tower you spot something!")
            print("As an adventurer, you decide to go check it!...")
        if player.location <= 15:
            mob = random.choice(ENEMIES_0_15)
        if 15 < player.location <= 30:
            mob = random.choice(ENEMIES_15_30)
        if 30 < player.location:
            mob = random.choice(ENEMIES_30_45)
        mob.HP = mob.MAXHEALTH
        print("You found a monster! It's {}!".format(mob.type))
        fight_beginning += 1

    print("What do you want to do? ")
    commands()
    player_input = input("--> ")

    if player_input == "s":
        print("\nThese are your stats:")
        player.status()
        print()
        monster_encounter()
    elif player_input == "i":
        print("\nYour inventory:")
        player.see_inventory()
        print()
        monster_encounter()
    elif player_input == "p":
        drink_potion()
        monster_encounter()
    elif player_input == "r":
        print()
        quitting()
        exit()
    elif player_input == "f":
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
                global player_dodged

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
                    player.HP -= round(damage_received, 3)
                    if damage_received == 0 and not player_dodged:
                        print("You were able to block the monster's attack.")
                        print("You still have {} HP.".format(player.HP))
                    if damage_received > 0 and not player_dodged:
                        print("The {} inflicted you {} damage.".format(mob.name, damage_received))
                    print("You have {} HP.".format(player.HP))
        # attack loop
        while True:
            global charged_strike
            charged_strike = False
            time.sleep(2)
            print("\nDo you want to use a charged strike for 1 MP that will add more 1 damage to your next attack?")
            ss = input("[y/n or enter]-->")
            if ss.lower() in yes_list_without_enter and player.MP > 0:
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
    else:
        print("Wrong Command! Try again.")
        monster_encounter()

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
        if player.location <= 15:
            new_armor = random.choice(ARMOR_0_15)
        if 15 < player.location:
            new_armor = random.choice(ARMOR_15_30)
        print("\nWhile climbing to the next floor you found a piece of armor on the ground.")
        print("The item is: {} and can be equipped in the {} Armor Slot.".format(clean_armor(new_armor), new_armor["Type:"]))
        equip_armor(new_armor)


def get_weapon():
    weapon_prob = random.randint(1, 5)
    if weapon_prob == 1:
        print("\nYour inventory:")
        player.see_inventory()
        if player.location <= 15:
            new_weapon = random.choice(WEAPONS_0_15)
        if 15 < player.location:
            new_weapon = random.choice(WEAPONS_15_30)
        print("\nWhile climbing to the next floor you found a weapon on the ground.")
        print("The item is: {} and can be equipped in exchange for your current weapon.".format(new_weapon))
        equip_weapon(new_weapon)


def drink_potion():
    print("\nThese are your potions:")
    print(player.potions)
    potion_input = input("To drink a potion write its name here, to quit press Enter: -->")
    if potion_input.lower() == "hp potion" or potion_input.lower() == "hp":
        if potion_hp["Name:"] in player.potions["Potions: "]:
            print("It will add {} HP and is going to be discarded, are you sure?".format(potion_hp[add_HP]))
            sure = input("[y/n]-->")
            if sure.lower() in yes_list:
                player.potions["Potions: "].remove(potion_hp["Name:"])
                player.HP += potion_hp[add_HP]
    elif potion_input.lower() == "mp potion" or potion_input.lower() == "mp":
        if potion_mp["Name:"] in player.potions["Potions: "]:
            print("It will add {} MP and is going to be discarded, are you sure?".format(potion_mp[add_MP]))
            sure = input("[y/n]-->")
            if sure.lower() in yes_list:
                player.potions["Potions: "].remove(potion_mp["Name:"])
                player.MP += potion_mp[add_MP]




################################################################ Events.

# The events don't work on a separate file so i decided to put them on here.

#########


### Funtions Needed for some events:


def quitting_event(a = None):
    if a == "rr":
        player.set_score()
        player.score -= score_lost_to_death
        player.score -= 2
        print()
        print("You decided to run from the monster and as you did that")
        print("He attacked you from the back, hitting your head and making you unconscious")
        print("You lost 2 additional score points from being greedy.")
        print("Your score is {}".format(player.score))
        print("You killed {} monster(s).".format(player.kill_count))
        print_quitting()
        exit()
    else:
        player.set_score()
        player.score -= score_lost_to_death
        player.score -= 2
        print()
        print("Game Over! You died of greed! As such you will loose 2 additional score points")
        print("besides the ones you would lose to death.")
        print("Your score is {}".format(player.score))
        print("You killed {} monster(s).".format(player.kill_count))
        print_quitting()
        exit()


def trap_chest_encounter_event():
    global player_input
    global mob
    global fight_beginning

    if fight_beginning == 0:
        mob = TrapChest()
        mob.HP = mob.MAXHEALTH
        print("The chest was a trap! It's {}!".format(mob.type))
        fight_beginning += 1

    print("What do you want to do? ")
    commands()
    player_input = input("--> ")

    if player_input == "s":
        print("\nThese are your stats:")
        player.status()
        print()
        trap_chest_encounter_event()
    elif player_input == "i":
        print("\nYour inventory:")
        player.see_inventory()
        print()
        trap_chest_encounter_event()
    elif player_input == "p":
        drink_potion()
        trap_chest_encounter_event()
    elif player_input == "r":
        print()
        quitting_event("rr")
        exit()
    elif player_input == "f":
        print("\nYou decided to attack the Trap Chest:")
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
                global player_dodged

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
                    player.HP -= round(damage_received, 3)
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
            ss = input("[y/n or enter]-->")
            if ss.lower() in yes_list_without_enter and player.MP > 0:
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
                quitting_event()
            if attack_tick % 2 == 0:
                time.sleep(0.5)
                print("\nYou can't run!")
                print("Press anything to continue")
                continue
    else:
        print("Wrong Command! Try again.")
        trap_chest_encounter_event()




### Events:

def event_shop():

    global deleted_shop

    shop_tick = 0
    deleted_shop = False

    global one_bought
    global two_bought
    global three_bought
    global four_bought
    global five_bought

    one_bought = False
    two_bought = False
    three_bought = False
    four_bought = False
    five_bought = False

    def shop():

        print("\nYour inventory:")
        player.see_inventory()

        while True:

            global one_bought
            global two_bought
            global three_bought
            global four_bought
            global five_bought

            print("\n### Weapons ###")
            if not one_bought:
                print("#1 - 60 gold - {}".format(weapon_sword_bronze))
            if not two_bought:
                print("#2 - 60 gold - {}".format(weapon_axe_bronze))
            if not three_bought:
                print("#3 - 100 gold - {}".format(weapon_longsword_iron))
            print("\n### Potions ###")
            if not four_bought:
                print("#4 - 120 gold - {}".format(potion_hp))
            if not five_bought:
                print("#4 - 120 gold - {}".format(potion_mp))
            buy = str(input("\nDo you want to buy something? \nPress [1/2/3/4/5] to buy the item.\nPress \"q\" or \"quit\" to quit.\n-->"))
            if buy == "1":
                if player.gold >= 60:
                    one_bought = True
                    equip_weapon(weapon_sword_bronze)
                    player.gold -= 60
                    print("Your gold: {}".format(player.gold))
                else:
                    print("Not enough money.")
                    continue
            if buy == "2":
                if player.gold >= 60:
                    two_bought = True
                    equip_weapon(weapon_axe_bronze)
                    player.gold -= 60
                    print("Your gold: {}".format(player.gold))
                else:
                    print("Not enough money.")
                    continue
            if buy == "3":
                if player.gold >= 100:
                    three_bought = True
                    equip_weapon(weapon_longsword_iron)
                    player.gold -= 100
                    print("Your gold: {}".format(player.gold))
                else:
                    print("Not enough money.")
                    continue
            if buy == "4":
                if player.gold >= 120:
                    four_bought = True
                    new_potion_to_inv(potion_hp)
                    player.gold -= 120
                    print("Your gold: {}".format(player.gold))
                else:
                    print("Not enough money.")
                    continue
            if buy == "5":
                if player.gold >= 120:
                    five_bought = True
                    new_potion_to_inv(potion_mp)
                    player.gold -= 120
                    print("Your gold: {}".format(player.gold))
                else:
                    print("Not enough money.")
                    continue
            if buy.lower() == "quit" or buy.lower() == "q":
                break
            if buy != "quit" or buy != "q" or buy != "1" or buy != "2" or buy != "3":
                print("Invalid Input! Try again.")

    if shop_tick == 0:
        print("\nAs you were almost approaching the next floor you found a strange spirit that looked very passive and intelligent.")
        time.sleep(1)
        print("It didn't attack you, so as you looked away from it you felt a weird sensation on your back")
        time.sleep(1)
        print("and suddenly you heard a voice:")
        time.sleep(1)
        print("Heyyyyyy~ {}, IIIII knowww you are adventuuuuring in this toweeeer".format(player.name))
        time.sleep(1)
        print("I haveeeee interessssting items for youuuuuuu~, do you waaaanna check them out?")
        first_shop_input = input("[y/n]-->")
        if first_shop_input.lower() in yes_list:
            shop()
            shop_tick += 1
        else:
            print("That's a shameeee, don't blame meeeeee for wwwhat happens neeeeeeexttt...")
            deleted_shop = True
    if shop_tick > 1:
        print("\nHelloo agaaaain, {} the Adventurerrrrrr.".format(player.name))
        print("Do youuuuuu wannaa buy somethingggg?")
        shop()
        second_shop_input = input("[y/n]-->")
        if second_shop_input.lower() in yes_list:
            shop()
            shop_tick += 1
        else:
            print("That's a shameeee, don't blame meeeeee for wwwhat happens neeeeeeexttt...")
            deleted_shop = True


def event_get_hp():
    print("\nAfter killing that monster you felt dizzy, but before you realized")
    print("your wounds were lightly healed and you feel like new again!")
    print("You gained 3 HP and 1 MP.")
    player.HP += 3
    player.MP += 1


def event_fountain():
    rrr = random.randint(1, 2)
    print("\nAs you were climbing the floor number {},".format(player.location))
    print("you saw a door with a bright light, and curious")
    print("you decided to see what's going on there.")
    print("\nYou saw a huge fountain that with a reddish water")
    print("equal to the one inside your HP Potion.")
    print("Since you had a free bottle with you, you decided to drink")
    print("a bit of it and fill your bottle with it...")
    if rrr == 1:
        print("You gained a HP Potion and 1 HP.")
        player.HP += 1
        new_potion_to_inv(potion_hp)
    if rrr == 2:
        print("The water was poisonous and you quickly threw away your bottle!")
        print("You lost 3 HP.")
        player.HP -= 3


def event_chest():
    rrr = random.randint(1, 2)
    print("\nAs you approached the next floor you saw a open door on your side")
    print("with a yellow light coming out of it.")
    m = input("Do you want to check it?")
    if m.lower() in yes_list:
        if rrr == 1:
            print()
            print("You found a room full of treasure with a huge chest in the middle.")
            print("You decide to check it...")
            time.sleep(2)
            trap_chest_encounter_event()
        if rrr == 2:
            print()
            print("You found a room full of treasure with a huge chest in the middle.")
            print("You decide to check it...")
            time.sleep(2)
            print("You received 100 gold.")
            player.gold += 100
    else:
        print("You left the suspicious room alone and continued your journey.")


def event_skeleton_weapon():
    rrr = random.randint(1, 3)
    print("\nAs you approached the next floor you saw a open door on your side")
    print("and you got a glimpse of what looked like a dead skeleton on the ground")
    print("with a golden weapon on the hand.")
    m = input("Do you want to check it?\n[y/n]-->")
    if m.lower() in yes_list:
        print("The skeleton was dead as expected and")
        if rrr == 1:
            print("the weapon he was carrying was a {}".format(weapon_sword_enchanted_gold))
            print("\nYour inventory:")
            player.see_inventory()
            equip_weapon(weapon_sword_enchanted_gold)
        if rrr > 1:
            print("the weapon he was carrying was a {}".format(weapon_sword_gold))
            player.see_inventory()
            equip_weapon(weapon_sword_gold)
    else:
        print("You left the room and continued your journey.")


merchant_found = False


def event_random_merchant():
    global merchant_found
    if merchant_found:
        print("\nAs you were advancing in the dungeon you saw a familiar spirit.")
        print("He quickly ignored you when he noticed you and disappeared into the walls.")

    if player.location <= 30:
        if 100 <= player.gold < 140 and not merchant_found:
            merchant_found = True
            print("\nAs you approached the next floor you heard a voice in front of")
            print("you coming from a weird defenseless spirit:")
            print("\"Hey there stranger! I love gold and you look like you have a bunch of it there...")
            print("do you mind if we did a quick trade?\"")
            c = input("\nWill you accept the spirit's offer?\n[y/n]-->")
            if c.lower() in yes_list:
                print("\"Nice...Good...Take a look at this and buy it!... I mean..., analyse it, and tell me what you think...\"")
                print("\nYour inventory:")
                player.see_inventory()
                print("\nHis item: {}".format(weapon_sword_strongly_enchanted_iron))
                print("\n\"Do you want to buy it stranger? I can sell the weapon to you for 100 coins...\"")
                d = input("[y/n]-->")
                if d.lower() in yes_list:
                    equip_weapon(weapon_sword_strongly_enchanted_iron)
                    player.gold -= 100
                    print("\nAfter you gave him the money, the spirit quickly disappeared.")
                else:
                    print("\nAAAAHHH...( he screamed ) that... that's a shame.")
                    print("He quickly vanished into the walls.")
            else:
                print("\nAAAAHHH...( he screamed ) that... that's a shame.")
                print("You didn't even saw the weapon... oh well...")
                print("He quickly vanished into the walls.")
        if player.gold >= 140 and not merchant_found:
            merchant_found = True
            print("\nAs you approached the next floor you heard a voice in front of")
            print("you coming from a weird defenseless spirit:")
            print("\"Hey there stranger! I love gold and you look like you have a bunch of it there...")
            print("do you mind if we did a quick trade?\"")
            c = input("\nWill you accept the spirit's offer?\n[y/n]-->")
            if c.lower() in yes_list:
                print("\"Nice...Good...Take a look at this and buy it!... I mean..., analyse it, and tell me what you think...\"")
                print("\nYour inventory:")
                player.see_inventory()
                print("\nHis item: {}".format(weapon_sword_strongly_enchanted_iron))
                print("\n\"Do you want to buy it stranger? I can sell the weapon to you for 140 coins...\"")
                d = input("{y/n]-->")
                if d.lower() in yes_list:
                    equip_weapon(weapon_sword_strongly_enchanted_iron)
                    player.gold -= 140
                    print("\nAfter you gave him the money, the spirit quickly disappeared.")
                else:
                    print("\nAAAAHHH...( he screamed ) that... that's a shame.")
                    print("He quickly vanished into the walls.")
            else:
                print("\nAAAAHHH...( he screamed ) that... that's a shame.")
                print("You didn't even saw the weapon... oh well...")
                print("He quickly vanished into the walls.")
    else:
        if 250 <= player.gold < 350 and not merchant_found:
            merchant_found = True
            print("\nAs you approached the next floor you heard a voice in front of")
            print("you coming from a weird defenseless spirit:")
            print("\"Hey there stranger! I love gold and you look like you have a bunch of it there...")
            print("do you mind if we did a quick trade?\"")
            c = input("\nWill you accept the spirit's offer?\n[y/n]-->")
            if c.lower() in yes_list:
                print("\"Nice...Good...Take a look at this and buy it!... I mean..., analyse it, and tell me what you think...\"")
                print("\nYour inventory:")
                player.see_inventory()
                print("\nHis item:".format(weapon_special_indented_ruby_axe))
                print("\n\"Do you want to buy it stranger? I can sell the weapon to you for 100 coins...\"")
                d = input("-->")
                if d.lower() in yes_list:
                    equip_weapon(weapon_special_indented_ruby_axe)
                    player.gold -= 100
                    print("After you gave him the money, the spirit quickly disappeared.")
                else:
                    print("AAAAHHH...( he screamed ) that... that's a shame.")
                    print("He quickly vanished into the walls.")
            else:
                print("AAAAHHH...( he screamed ) that... that's a shame.")
                print("You didn't even saw the weapon... oh well...")
                print("He quickly vanished into the walls.")
        if player.gold >= 350 and not merchant_found:
            merchant_found = True
            print("\nAs you approached the next floor you heard a voice in front of")
            print("you coming from a weird defenseless spirit:")
            print("\"Hey there stranger! I love gold and you look like you have a bunch of it there...")
            print("do you mind if we did a quick trade?\"")
            c = input("\nWill you accept the spirit's offer?\n[y/n]-->")
            if c.lower() in yes_list:
                print("\"Nice...Good...Take a look at this and buy it!... I mean..., analyse it, and tell me what you think...\"")
                print("\nYour inventory:")
                player.see_inventory()
                print("\nHis item:".format(weapon_special_indented_ruby_axe))
                print("\n\"Do you want to buy it stranger? I can sell the weapon to you for 140 coins...\"")
                d = input("-->")
                if d.lower() in yes_list:
                    equip_weapon(weapon_special_indented_ruby_axe)
                    player.gold -= 140
                    print("After you gave him the money, the spirit quickly disappeared.")
                else:
                    print("AAAAHHH...( he screamed ) that... that's a shame.")
                    print("He quickly vanished into the walls.")
            else:
                print("AAAAHHH...( he screamed ) that... that's a shame.")
                print("You didn't even saw the weapon... oh well...")
                print("He quickly vanished into the walls.")


def event_wall_arrow():
    print("\nAs you were advancing in the dungeon you suddenly stepped in a pressure plate")
    print("that released a arrow that hit you in the leg.")
    print("You lost 2 HP.")
    player.HP -= 2


def event_angel_blessing():
    print("\nYou suddenly see a bright light above you, and as you prepare your weapon")
    print("your wounds suddenly heal and you feel restored, an angel was above you")
    print("and blessed you for some reason after disappearing.")
    print("You gained 2 HP and 1 MP.")
    player.HP += 2
    player.MP += 1


def event_above_arrow():
    print("\nAs you were advancing in the dungeon you suddenly stepped in a pressure plate")
    print("that released a arrow that hit you in the arm.")
    print("You lost 2 HP.")
    player.HP -= 2


found_armor = False
dead_armor_tick = 0


def event_dead_armor():

    global found_armor
    global dead_armor_tick

    #found_armor = False
    #dead_armor_tick = 0

    if found_armor:
        print("\nAs you were climbing the stairs to the next level you saw the same human")
        print("body in the ground almost like if he was teleported to this floor.")
        print("He has nothing to check on him more, so you continue your journey.")

    if dead_armor_tick == 0:
        print("\nAs you were climbing the stairs to the next level you saw a human")
        print("body in the ground with a weird armor on hit.")
        m = input("Do you want to check it?\n[y/n]-->")
        if m.lower() in yes_list:
            found_armor = True
            print("You found a very good armor in a good condition due to the fact")
            print("that it was enchanted. It's a {}".format(armor_chest_dead_man_breastplate))
            print("\nYour inventory:")
            player.see_inventory()
            equip_armor(armor_chest_dead_man_breastplate)
        else:
            print("You left him alone and resumed your journey.")
    if dead_armor_tick == 1 and not found_armor:
        print("\nAs you were climbing the stairs to the next level you saw the same human")
        print("body in the ground with a weird armor on him again,")
        print("almost like if he was teleported to this floor.")
        m = input("Do you want to check it?\n[y/n]-->")
        if m.lower() in yes_list:
            found_armor = True
            print("You found a very good armor in a good condition due to the fact")
            print("that it was enchanted. It's a {}".format(armor_chest_dead_man_breastplate))
            print("\nYour inventory:")
            player.see_inventory()
            equip_armor(armor_chest_dead_man_breastplate)
        else:
            print("You left him alone and resumed your journey.")
    if dead_armor_tick > 1 and not found_armor:
        print("\nAs you were climbing the stairs to the next level you saw again the same human")
        print("body in the ground with a weird armor on him again,")
        print("but this time it looked like it had a evil aura around it.")
        m = input("Do you want to check it?\n[y/n]-->")
        if m.lower() in yes_list:
            found_armor = True
            print("Apparently it was't nothing bad, and ")
            print("you found a very good armor in a good condition due to the fact")
            print("that it was enchanted. It's a {}".format(armor_chest_dead_man_breastplate))
            print("\nYour inventory:")
            player.see_inventory()
            equip_armor(armor_chest_dead_man_breastplate)
        else:
            print("You left him alone and resumed your journey.")

    dead_armor_tick += 1


EVENTS = [event_shop, event_get_hp, event_fountain, event_chest, event_skeleton_weapon,
          event_random_merchant, event_wall_arrow, event_angel_blessing, event_above_arrow, event_dead_armor]


############################


# Game Loop
def main_loop():
    global fight_beginning
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

        fight_beginning = 0
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

        fight_beginning = 0
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
