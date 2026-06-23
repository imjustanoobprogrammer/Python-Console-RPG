import random
import sys

SCENES = ('Forest', 'Mountains', 'Plains', 'Dungeons', 'Temple')
SHOP_ITEMS = ['health potion', 'armor', 'ammo']
ENEMY_DROPS = ['health potion', 'armor', 'ammo', 'coin']
enemies = {
    "Goblin": {"health": (40, 45), "damage": (25, 30), "drop_chance":10},
    "Witch": {"health": (45, 50), "damage": (25, 30), "drop_chance": 10},
    "Wolf": {"health": (35, 40), "damage": (20, 25), "drop_chance": 10},
    "Slime": {"health": (20, 30), "damage": (15, 20), "drop_chance": 10},
    "Minotaur": {"health": (45, 55), "damage": (40, 50), "drop_chance": 15},
    "Spectre": {"health": (45, 55), "damage": (30, 40), "drop_chance": 20},
    "Dragon": {"health": (65, 75), "damage": (50, 65), "drop_chance": 25}
}
weapons = {'pistol': {"damage":(34, 35), "cost": 1},
           'mac10': {"damage":(40, 55), "cost": 1},
           'm16': {"damage":(50, 65), "cost": 2,},
           'bazooka': {"damage":(55, 65), "cost": 3},
           'taser': {"damage":(10, 15), "cost": 1},
           'mortar': {"damage":(60, 75), "cost": 5}
           }
familiars = {'Fox': {'damage': (10, 15), },
             'Spirit': {'damage': (15, 20), },
             'Yokai': {'damage': (20, 25), },
             'Undead': {'damage': (25, 30), }
             }
def new_game_state():
    return {
    "hp":  100,
    "xp" : 0,
    "coins":  10,
    "weapon_ammo" :    {'pistol': 3,
                       'mac10': 3,
                       'm16': 2,
                       'bazooka': 2,
                       'taser': 4,
                       'mortar': 2},
    "weapon_upgrade":  {'pistol': 0,
                      'mac10': 0,
                      'm16': 0,
                      'bazooka': 0,
                      'taser': 0,
                      'mortar': 0},
    "inventory" :{'health potion':1, 'armor':1, 'ammo':1},
    "familiar_state" : False,
    "familiar_hp" : 100,
    "user_familiar" : None
    }

items = {'health potion': {'cap': 100, 'heal':(20,30)}, 'armor': {'cap':200, 'heal':(50,100)},  'ammo':1}

item_cost = {'armor':3, 'health potion':1, 'ammo':{'pistol':1, 'mac10':1, 'm16':2, 'bazooka':2, 'taser':1, 'mortar':2}}

def greetings():
    state = new_game_state()
    input("""
     ===== TEXT RPG =====

     Welcome, adventurer!
     Defeat enemies, collect loot,
     upgrade your weapons,
     and reach 100 XP to win.

     Good luck!
     ====================
     """)
    menu(state)
def menu(state):
    while True:
        print(f"\n---HP: {state['hp']} XP: {state['xp']} COINS: {state['coins']}---")
        print(f"1) Shop\n2) Upgrade\n3) Look for familiar\n4) Fight\n5) Inventory\n6) Quit")
        choose = input("> ")
        if choose == "1":
            state = shop(state)
        elif choose == "2":
            state = upgrade(state)
        elif choose == "3":
            state = familiar(state)
        elif choose == "4":
            state = fight(state)
        elif choose == "5":
            state = user_inventory(state)
        elif choose == "6":
            print("Thanks for playing!")
            sys.exit()
        else:
            print("Choose valid option.")
            continue

def shop(state):
    print(f"\nWelcome to the shop! What do you want to buy? Your coins: {state['coins']}")
    print(SHOP_ITEMS)
    item_to_buy = input("> ").lower()
    if item_to_buy =='ammo':
        what_ammo = input(f"Select what weapon ammo {list(weapons.keys())}: ")
        if what_ammo not in weapons:
            input("Please choose a valid weapon.")
            return state
        if input(f"This ammo costs {item_cost['ammo'][what_ammo]} coin/s, continue? (y/n): ").lower() == 'y':
            if state["coins"] >= item_cost['ammo'][what_ammo]:
                state["coins"] -= item_cost['ammo'][what_ammo]
                state["weapon_ammo"][what_ammo] += 1
                input(f'You successfully purchased 1 ammo for {what_ammo}. Come again!')
            else:
             input("You don't have enough coins.")
        else:
            input("Try buying next time!")
    elif item_to_buy in SHOP_ITEMS:
        if input(f"This item costs {item_cost[item_to_buy]} coins, continue? (y/n): ").lower() == "y":
            if state["coins"] >= item_cost[item_to_buy]:
                state["coins"] -= item_cost[item_to_buy]
                state["inventory"][item_to_buy] += 1
                print(f"You successfully purchased {item_to_buy}. Come again!")
                input("Press enter to continue...")
            else:
                input("You don't have enough coins.")
    else:
        input("Please choose an item from the list.")
    return state
def upgrade(state):
    weapon_to_upgrade = input(f"Please choose a weapon to upgrade.(Your Coins: {state['coins']}) {list(weapons.keys())}: ")
    if weapon_to_upgrade in weapons:
        if input(f"This weapon costs {weapons[weapon_to_upgrade]['cost']} coins to upgrade, continue? (y/n): ").lower() == "y":
            if state["coins"] >= weapons[weapon_to_upgrade]["cost"]:
                state["coins"] -= weapons[weapon_to_upgrade]["cost"]
                state["weapon_upgrade"][weapon_to_upgrade] += random.randint(5, 10)
                input(f"You successfully upgraded {weapon_to_upgrade}.")
            else:
                input("You don't have enough coins.")
        else:
            input("Maybe next time")
    return state
def familiar(state):
    if state["familiar_state"]:
        input("You already have a familiar.")
    elif input(f"Look for familiar for 10 coins? Your coins: {state['coins']} (y/n): ").lower() == "y":
        if state["coins"] >= 10:
            state["coins"] -= 10
            familiar_scene = random.choice(SCENES)
            if random.randint(1, 100) <= 50:
                state["user_familiar"] = random.choice (list(familiars.keys()))
                input(f"You arrived at {familiar_scene}\nYou formed a pact with a {state['user_familiar']}.\nPress any key to continue...")
                state["familiar_state"] = True
            else:
                input(f"You arrived at {familiar_scene} but found nothing...\nPress enter to continue...")
        else:
            input("You don't have enough coins.")
    else:
        input("Maybe next time.")
    return state
def fight(state):
    while state["hp"] > 0 and state["xp"] < 100 and any(value > 0 for value in state["weapon_ammo"].values()):

        enemy = random.choice(list(enemies.keys()))
        enemy_data = enemies[enemy]
        e_hp = random.randint(*enemy_data["health"]) + (state["xp"]//5)
        scene = random.choice(SCENES)

        print(f'\n---HP: {state["hp"]} XP: {state["xp"]}---')
        print(f"You arrived at the {scene}. A {enemy} (HP: {e_hp}) blocks your path!")
        decision = input("Fight or run? (f/r): ").lower()
        if decision == "f":
            while e_hp > 0:



                print(f"\n{state['weapon_ammo']}")
                print(f"\nChoose your weapon from the list.")
                weapon = input("> ").lower()

                if weapon not in weapons:
                    print("Please choose a weapon from the list.")
                    continue
                if state["weapon_ammo"][weapon] <= 0:
                    print(f"You are out of {weapon} ammo.")
                    continue

                weapon_data = weapons[weapon]

                weapon_damage = random.randint(*weapon_data["damage"]) + (state["weapon_upgrade"][weapon])
                e_dmg = random.randint(*enemy_data["damage"]) + (state["xp"] // 5)

                state["weapon_ammo"][weapon] -= 1
                state["weapon_ammo"][weapon] = max(0, state["weapon_ammo"][weapon])
                e_hp -= weapon_damage
                ehp = max(0, e_hp)
                input(f"-> You hit the {enemy} using {weapon} for {weapon_damage} damage! ({enemy} HP: {ehp})")
                if e_hp <= 0:
                    break

                if state["familiar_state"]:
                    familiar_data = familiars[state["user_familiar"]]
                    familiar_dmg = random.randint(*familiar_data["damage"])
                    e_hp -= familiar_dmg
                    ehp = max(0, e_hp)
                    input(f'-> Your familiar ({state["user_familiar"]}) dealt {familiar_dmg} damage to the {enemy}! ({enemy} HP: {ehp})')
                    edmg_familiar = e_dmg // 5
                    state["familiar_hp"] -= edmg_familiar
                    state["familiar_hp"] = max(0, state["familiar_hp"])
                    if e_hp <= 0:
                        break
                    input(f"-> The {enemy} dealt {edmg_familiar} damage to your familiar. ({state['user_familiar']} HP: {state['familiar_hp']}) ")
                    if state["familiar_hp"] <= 0:
                        state["familiar_state"] = False
                        state["user_familiar"] = None
                        state["familiar_hp"] = 100
                        input("Your familiar died, my condolences.")
                if e_hp > 0:
                    state["hp"] -= e_dmg
                    state["hp"] = max(0, state["hp"])
                    input(f"-> The {enemy} deals {e_dmg} damage to you! (Your HP: {state['hp']})")

                if state["hp"] <= 0:
                    print("\n*** YOU DIED ***")
                    print(f"Final Score: {state['xp']}")
                    if input("You lost, play again? (y/n): ").lower() == "y":
                        greetings()
                    else:
                        print('Thanks for playing!')
                        sys.exit()

                if state["xp"] >= 100:
                    print("\n*** YOU WIN! ***")
                    print(f"Final score: {state['xp']}")
                    if input("Play again? (y/n): ").lower() == "y":
                        greetings()
                    else:
                        print("Thanks for playing!")
                        sys.exit()
                if all(value <= 0 for value in state["weapon_ammo"].values()):
                    input("You ran out of weapon ammo.")
                    break
            if e_hp <= 0:
                reward = max(5, random.randint(15, 20) - (state["xp"] // 5))
                state["xp"] += reward
                state["xp"] = min(100, state["xp"])
                comp_choice = random.choice(ENEMY_DROPS)
                input(f"\nVictory! You defeated the {enemy} and gained {reward} XP.")
                if  random.randint(1, 100) <= 50 + enemies[enemy]["drop_chance"]:
                    if comp_choice == 'coin':
                        coins_reward = random.randint(2, 6)
                        state["coins"] += coins_reward
                        input(f"The {enemy} dropped {coins_reward} coins")
                    else:
                        state["inventory"][comp_choice] += 1
                        input(f"The {enemy} dropped the {comp_choice} loot!")


        elif decision == "r":
            input("\nYou safely escaped back to the trail!")
            break
        else:
            input("Invalid choice! The enemy stares at you awkwardly.")
            continue

    if all(value <= 0 for value in state["weapon_ammo"].values()):
        input("You are out of weapon ammo. Resupply first.")
    return state

def user_inventory(state):
    print(f"\n---HP: {state['hp']} XP: {state['xp']}---")
    print(f"Available items: {state['inventory']}")
    item_to_use = input("Which one do you want to use?: ").lower()
    if item_to_use in state["inventory"]:
        if state["inventory"][item_to_use] > 0:
            if item_to_use == "ammo":
                    print(f"Select what weapon you want to use the ammo to. {list(weapons.keys())}")
                    use_ammo_for = input("> ").lower()
                    if use_ammo_for in list(weapons.keys()):
                        state["weapon_ammo"][use_ammo_for] += 1
                        state["inventory"][item_to_use] -= 1
                        state["inventory"][item_to_use] = max(0, state["inventory"][item_to_use])
                        input(f"You added 1 ammo to {use_ammo_for}.")
                    else:
                        input("Select which weapon you want to use the ammo to.")
            else:
                hp_cap = items[item_to_use]['cap']
                if state["hp"] >= hp_cap:
                    print("Your hp is already full.")
                else:
                    state["hp"] += random.randint(*items[item_to_use]['heal'])
                    state["hp"] = min(hp_cap, state["hp"])
                    state["inventory"][item_to_use] -= 1
                    input(f"You successfully used {item_to_use}.")
        else:
            input(f"You are out of {item_to_use} from your inventory.")
    else:
        input(f"You don't have {item_to_use} in your inventory.")
    return state
greetings()
