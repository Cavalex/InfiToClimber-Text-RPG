import random

class GenMob:
    type = ""
    MAXHEALTH = 0
    ATTACK = 0
    DEFENSE = 0
    HP = MAXHEALTH

    def status(self):
        print("Monster: {}".format(self.type))
        print("HP: {}/{}".format(self.HP, self.MAXHEALTH))
        print("Attack: {}".format(self.ATTACK))
        print("Defense: {}".format(self.DEFENSE))

### Event Mobs:

class TrapChest(GenMob):
    name = "Trap Chest"
    type = "a Trap Chest"
    MAXHEALTH = 8
    ATTACK = 2.5
    DEFENSE = 2
    HP = MAXHEALTH


### Mobs:

class Skeleton(GenMob):
    name = "Skeleton"
    type = "a Skeleton"
    MAXHEALTH = 4
    ATTACK = 2
    DEFENSE = 0.5
    HP = MAXHEALTH

class GiantSlime(GenMob):
    name = "Giant Slime"
    type = "a Giant Slime"
    MAXHEALTH = 6
    ATTACK = 2
    DEFENSE = 0.5
    HP = MAXHEALTH

class Goblin(GenMob):
    name = "Goblin"
    type = "a Goblin"
    MAXHEALTH = 4
    ATTACK = 2
    DEFENSE = 1
    HP = MAXHEALTH

class UndeadWolf(GenMob):
    name = "Undead Wolf"
    type = "an Undead Wolf"
    MAXHEALTH = 4
    ATTACK = 1.5
    DEFENSE = 1
    HP = MAXHEALTH

class Zombie(GenMob):
    name = "Zombie"
    type = "a Zombie"
    MAXHEALTH = 5
    ATTACK = 2
    DEFENSE = 1
    HP = MAXHEALTH

####
class PoisonousSlime(GenMob):
    name = "Poisonous Slime"
    type = "a Poisonous Slime"
    MAXHEALTH = 3
    ATTACK = 2.5
    DEFENSE = 0.5
    HP = MAXHEALTH

class Orc(GenMob):
    name = "Orc"
    type = "an Orc"
    MAXHEALTH = 6
    ATTACK = 3
    DEFENSE = 1
    HP = MAXHEALTH
#

class HobGoblin(GenMob):
    name = "Hobgoblin"
    type = "a Hobgoblin"
    MAXHEALTH = 8
    ATTACK = 3
    DEFENSE = 1.5
    HP = MAXHEALTH

class EnchantedSkeleton(GenMob):
    name = "Enchanted Skeleton"
    type = "an Enchanted Skeleton"
    MAXHEALTH = 6
    ATTACK = 2.5
    DEFENSE = 2
    HP = MAXHEALTH

class HighOrc(GenMob):
    name = "High Orc"
    type = "a High Orc"
    MAXHEALTH = 8
    ATTACK = 4
    DEFENSE = 1.5
    HP = MAXHEALTH

###
class RedcapGoblin(GenMob):
    name = "Redcap Goblin"
    type = "a Redcap Goblin"
    MAXHEALTH = 9
    ATTACK = 4
    DEFENSE = 1.5
    HP = MAXHEALTH

class MagicSpirit(GenMob):
    rr = random.randint(1, 4)
    if rr == 1:
        type = "a Water Spirit"
        name = "Water Spirit"
    if rr == 2:
        type = "a Fire Spirit"
        name = "Fire Spirit"
    if rr == 3:
        type = "a Wind Spirit"
        name = "Wind Spirit"
    if rr == 4:
        type = "an Earth Spirit"
        name = "Earth Spirit"
    MAXHEALTH = 4
    ATTACK = 6
    DEFENSE = 1
    HP = MAXHEALTH
#
class EvolvedHighOrc(GenMob):
    name = "Evolved High Orc"
    type = "a Evolved High Orc"
    MAXHEALTH = 9
    ATTACK = 4
    DEFENSE = 2
    HP = MAXHEALTH

class Elemental(GenMob):
    rr = random.randint(1, 4)
    if rr == 1:
        type = "a Water Elemental"
        name = "Water Elemental"
    if rr == 2:
        type = "a Fire Elemental"
        name = "Fire Elemental"
    if rr == 3:
        type = "a Wind Elemental"
        name = "Wind Elemental"
    if rr == 4:
        type = "an Earth Elemental"
        name = "Earth Elemental"
    MAXHEALTH = 5
    ATTACK = 6
    DEFENSE = 1.5
    HP = MAXHEALTH

class HiglyEnchantedSkeleton(GenMob):
    name = "Highly Enchanted Skeleton"
    type = "an Highly Enchanted Skeleton"
    MAXHEALTH = 7
    ATTACK = 3
    DEFENSE = 2.5
    HP = MAXHEALTH

class Golem(GenMob):
    rr = random.randint(1, 2)
    if rr == 1:
        type = "a Earth Golem"
        name = "Earth Golem"
    if rr == 2:
        type = "a Iron Golem"
        name = "Iron Golem"
    MAXHEALTH = 10
    ATTACK = 3
    DEFENSE = 2.5
    HP = MAXHEALTH

class GiantPoisonousSlime(GenMob):
    name = "Giant Poisonous Slime"
    type = "a Giant Poisonous Slime"
    MAXHEALTH = 3.5
    ATTACK = 6
    DEFENSE = 1
    HP = MAXHEALTH


ENEMIES_0_10 = [Goblin, UndeadWolf, Zombie, Skeleton, GiantSlime, Orc, PoisonousSlime]

ENEMIES_10_20 = [PoisonousSlime, Orc, HobGoblin, HighOrc, EnchantedSkeleton, MagicSpirit, RedcapGoblin]

ENEMIES_20_30 = [RedcapGoblin, MagicSpirit, EvolvedHighOrc, Elemental, Elemental, HiglyEnchantedSkeleton, Golem, GiantPoisonousSlime]
# 2x Elementals. I like them lol.
