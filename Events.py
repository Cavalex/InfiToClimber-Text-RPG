from game import *
from Gear import *
from Mobs import *


### Funtions Needed for some events:

def quitting_event():
    player.set_score()
    player.score -= score_lost_to_death
    player.score -= 1 # From the greed.
    print("\nGame Over! You died of greed!")
    print("Your score is {}".format(player.score))
    print("You killed {} monsters.".format(player.kill_count))
    print_quitting()

def trap_chest_encounter_event():
    global player_input

    mob = TrapChest()
    mob.HP = mob.MAXHEALTH
    print("The chest was a monster! It's {}!".format(mob.type))
    print("What do you want to do? ")
    commands()
    player_input = input("--> ")

    tried_to_run = False

    def wrong_command():
        global player_input
        global tried_to_run

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
            while player_input == "r":
                if not tried_to_run:
                    print()
                    print("As you were trying to run the door suddenly closed")
                    print("And the chest jumped at you from behind and hit you! It won't let you run!")
                    print("You lost 3 HP.")
                    time.sleep(0.1)
                    player.HP -= 3
                    print("\nWhat do you want to do now?")
                    commands()
                    player_input = input("--> ")
                    tried_to_run = True
                else:
                    print()
                    print("You can't run!")
                    print("\nWhat do you want to do now?")
                    commands()
                    player_input = input("--> ")
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
        while player_input == "r":
            if not tried_to_run:
                print()
                print("As you were trying to run the door suddenly closed")
                print("And the chest jumped at you from behind and hit you! It won't let you run!")
                print("You lost 3 HP.")
                player.HP -= 3
                print("\nWhat do you want to do now?")
                commands()
                player_input = input("--> ")
                tried_to_run = True
            else:
                print()
                print("You can't run!")
                print("\nWhat do you want to do now?")
                commands()
                player_input = input("--> ")
        wrong_command()
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
        print("As you were trying to run the door suddenly closed and the")
        print("chest critically injured you from behind, knocking you unconscious.")
        print("1 additional point will be subtracted from your score for dying of greed.")
        quitting_event()
        exit()


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
        print("Helloo agaaaain, {} the Adventurerrrrrr.".format(player.name))
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
    print("After killing that monster you felt dizzy, but before you realized")
    print("your wounds were lightly healed and you feel like new again!")
    print("You gained 3 HP and 1 MP.")
    player.HP += 3
    player.MP += 1


def event_fountain():
    rrr = random.randint(1, 2)
    print("As you were climbing the floor number {},".format(player.location))
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
    print("As you approached the next floor you saw a open door on your side")
    print("with a yellow light coming out of it.")
    m = input("Do you want to check it?")
    if m.lower() in yes_list:
        if rrr == 1:
            print("You found a room full of treasure with a huge chest in the middle.")
            print("You decide to check it...")
            trap_chest_encounter_event()
        if rrr == 2:
            print("You found a room full of treasure with a huge chest in the middle.")
            print("You decide to check it...")
            print("You received 100 gold.")
            player.gold += 100
    else:
        print("You left the suspicious room alone and continued your journey.")


def event_skeleton_weapon():
    rrr = random.randint(1, 3)
    print("As you approached the next floor you saw a open door on your side")
    print("and you got a glimpse of what looked like a dead skeleton on the ground")
    print("with a golden weapon on the hand.")
    m = input("Do you want to check it?\n[y/n]-->")
    if m.lower() in yes_list:
        print("The skeleton was dead as expected and")
        if rrr == 1:
            print("the weapon he was carrying was a {}".format(weapon_sword_enchanted_gold))
            player.see_inventory()
            equip_weapon(weapon_sword_enchanted_gold)
        if rrr > 1:
            print("the weapon he was carrying was a {}".format(weapon_sword_gold))
            player.see_inventory()
            equip_weapon(weapon_sword_gold)
    else:
        print("You left the room and continued your journey.")


def event_random_merchant():
    global merchant_found
    merchant_found = False
    if 100 <= player.gold < 140 and not merchant_found:
        merchant_found = True
        print("As you approached the next floor you heard a voice in front of")
        print("you coming from a weird defenseless spirit:")
        print("\"Hey there stranger! I love gold and you look like you have a bunch of it there...")
        print("do you mind if we did a quick trade?\"")
        c = input("\nWill you accept the spirit's offer?\n[y/n]-->")
        if c.lower() in yes_list:
            print("\"Nice...Good...Take a look at this and buy it!... I mean..., analyse it, and tell me what you think...\"")
            print("\nYour inventory:")
            player.see_inventory()
            print("\nHis item:".format(weapon_sword_strongly_enchanted_iron))
            print("\n\"Do you want to buy it stranger? I can sell the weapon to you for 100 coins...\"")
            d = input("-->")
            if d.lower() in yes_list:
                equip_weapon(weapon_sword_strongly_enchanted_iron)
                player.gold -= 100
                print("After you gave him the money, the spirit quickly disappeared.")
            else:
                print("AAAAHHH...( he screamed ) that... that's a shame.")
                print("He quickly vanished into the walls.")
        else:
            print("AAAAHHH...( he screamed ) that... that's a shame.")
            print("You didn't even saw the weapon... oh well...")
            print("He quickly vanished into the walls.")
    if player.gold >= 140 and not merchant_found:
        merchant_found = True
        print("As you approached the next floor you heard a voice in front of")
        print("you coming from a weird defenseless spirit:")
        print("\"Hey there stranger! I love gold and you look like you have a bunch of it there...")
        print("do you mind if we did a quick trade?\"")
        c = input("\nWill you accept the spirit's offer?\n[y/n]-->")
        if c.lower() in yes_list:
            print("\"Nice...Good...Take a look at this and buy it!... I mean..., analyse it, and tell me what you think...\"")
            print("\nYour inventory:")
            player.see_inventory()
            print("\nHis item:".format(weapon_sword_strongly_enchanted_iron))
            print("\n\"Do you want to buy it stranger? I can sell the weapon to you for 140 coins...\"")
            d = input("-->")
            if d.lower() in yes_list:
                equip_weapon(weapon_sword_strongly_enchanted_iron)
                player.gold -= 140
                print("After you gave him the money, the spirit quickly disappeared.")
            else:
                print("AAAAHHH...( he screamed ) that... that's a shame.")
                print("He quickly vanished into the walls.")
        else:
            print("AAAAHHH...( he screamed ) that... that's a shame.")
            print("You didn't even saw the weapon... oh well...")
            print("He quickly vanished into the walls.")
    if merchant_found:
        print("As you were advancing in the dungeon you saw a familiar spirit.")
        print("He quickly ignored you when he noticed you and disappeared into the walls.")


def event_wall_arrow():
    print("As you were advancing in the dungeon you suddenly stepped in a pressure plate")
    print("that released a arrow that hit you in the leg.")
    print("You lost 2 HP.")
    player.HP -= 2


def event_angel_blessing():
    print("You suddenly see a bright light above you, and as you prepare your weapon")
    print("your wounds suddenly heal and you feel restored, an angel was above you")
    print("and blessed you for some reason after disappearing.")
    print("You gained 2 HP and 1 MP.")
    player.HP += 2
    player.MP += 1


def event_above_arrow():
    print("As you were advancing in the dungeon you suddenly stepped in a pressure plate")
    print("that released a arrow that hit you in the arm.")
    print("You lost 2 HP.")
    player.HP -= 2


def event_dead_armor():

    global found_armor
    global dead_armor_tick

    found_armor = False
    dead_armor_tick = 0

    if dead_armor_tick == 0:
        print("As you were climbing the stairs to the next level you saw a human")
        print("body in the ground with a weird armor on hit.")
        m = input("Do you want to check it?\n[y/n]-->")
        if m.lower() in yes_list:
            dead_armor_tick += 1
            found_armor = True
            print("You found a very good armor in a good condition due to the fact")
            print("that it was enchanted. It's a {}".format(armor_chest_dead_man_breastplate))
            print("\nYour inventory:")
            player.see_inventory()
            equip_armor(armor_chest_dead_man_breastplate)
        else:
            dead_armor_tick += 1
            print("You left him alone and resumed your journey.")
    if dead_armor_tick == 1 and not found_armor:
        print("As you were climbing the stairs to the next level you saw the same human")
        print("body in the ground with a weird armor on him again,")
        print("almost like if he was teleported to this floor.")
        m = input("Do you want to check it?\n[y/n]-->")
        if m.lower() in yes_list:
            dead_armor_tick += 1
            found_armor = True
            print("You found a very good armor in a good condition due to the fact")
            print("that it was enchanted. It's a {}".format(armor_chest_dead_man_breastplate))
            print("\nYour inventory:")
            player.see_inventory()
            equip_armor(armor_chest_dead_man_breastplate)
        else:
            dead_armor_tick += 1
            print("You left him alone and resumed your journey.")
    if dead_armor_tick > 1 and not found_armor:
        print("As you were climbing the stairs to the next level you saw again the same human")
        print("body in the ground with a weird armor on him again,")
        print("but this time it looked like it had a evil aura around it.")
        m = input("Do you want to check it?\n[y/n]-->")
        if m.lower() in yes_list:
            dead_armor_tick += 1
            found_armor = True
            print("Apparently it was't nothing bad, and ")
            print("you found a very good armor in a good condition due to the fact")
            print("that it was enchanted. It's a {}".format(armor_chest_dead_man_breastplate))
            print("\nYour inventory:")
            player.see_inventory()
            equip_armor(armor_chest_dead_man_breastplate)
        else:
            dead_armor_tick += 1
            print("You left him alone and resumed your journey.")
    if found_armor:
        print("As you were climbing the stairs to the next level you saw the same human")
        print("body in the ground almost like if he was teleported to this floor.")
        print("He has nothing to check on him more, so you continue your journey.")


EVENTS = [event_shop, event_get_hp, event_fountain, event_chest, trap_chest_encounter_event, event_skeleton_weapon,
          event_random_merchant, event_wall_arrow, event_angel_blessing, event_above_arrow, event_dead_armor]
