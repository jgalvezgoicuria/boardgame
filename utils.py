import numpy as np

from parameters import UNIT_TYPE_CODE

class War_map:
    def __init__(self, dimensions=[5, 5]):
        self.dimensions = dimensions
        self.tiles = np.zeros(dimensions)

    def remove_unit(self, unit):
        self.tiles[unit.position["y"], unit.position["x"]] = 0
    
    def set_unit(self, unit):
        self.tiles[unit.position["y"], unit.position["x"]] = int(str(unit.team) + str(unit.id))

    def check_ocupation(self, x, y):
        print(x)
        print(y)
        if self.tiles[y, x] == 0:
            return False
        else:
            return True
        
    def show_map(self):
        print(self.tiles)

class Unit:
    def __init__(self, id, team, type,
                 hit_points = 50,
                 movement = 1,
                 position={'x': 0, 'y':0}, 
                 attack_type={'damage': 10,'distance': 1}):
        self.id = id
        self.team = team
        self.type = type
        self.hit_points = hit_points
        self.movement = movement
        self.position = position.copy()
        self.attack_type = attack_type.copy()

    def set_x(self, x):
        self.position['x'] = x

    def set_y(self, y):
        self.position['y'] = y

    def attack(self, target, map):
        # Check if out of range:
        y_len = abs(self.position['y'] - target.position['y'])
        x_len = abs(self.position['x'] - target.position['x'])

        if y_len > self.attack_type["distance"] or x_len > self.attack_type["distance"]:
            print('Target out of range.')
            return 0
        
        # Do damage:
        target.hit_points -= self.attack_type["damage"]
        print('You hit!', 'And do ', self.attack_type["damage"], 'damage.')
        print('The target left with',  target.hit_points, 'hit_points')

        # check if unit defeated:
        if target.hit_points <= 0:
            print('Unit defeated')
            map.remove_unit(target)
            return target.id
        else:
            return 0
        
    def move(self, direction, map):

        # Calculate new positon:
        new_position = self.position.copy()

        if direction == 'up':
            new_position['y'] -= self.movement
        elif direction == 'down':
            new_position['y'] += self.movement
        elif direction == 'left':
            new_position['x'] -= self.movement
        elif direction == 'right':
            new_position['x'] += self.movement
        else:
            print('The wrong direction have been insert. Unit not move.')
            return -1

        # Check if the new position is empty:
        try:
            if map.check_ocupation(new_position['x'], new_position['y']):
                print("You can't move there.")
                return 0
            else:
                map.remove_unit(self)
                self.position = new_position
                map.set_unit(self)
        except:
            print("You can't move there.")
            return 0


def search_unit(team, unit_id):
    for unit in team:
        if unit.id == int(unit_id):
            return unit       
    return 0


def start():
    # create map
    war_map = War_map()

    # create units and assing position
    unit_id = 0
    team_1 = []

    team_1 = [Unit(unit_id, 1, unit_type, 
                   movement=UNIT_TYPE_CODE[unit_type]["movement"], 
                   attack_type=UNIT_TYPE_CODE[unit_type]["attack_type"]) for unit_id, unit_type in enumerate(UNIT_TYPE_CODE)]

    # for unit_type in UNIT_TYPE_CODE:
    #     team_1.append(Unit(unit_id, 1, unit_type, 
    #                        movement=UNIT_TYPE_CODE[unit_type]["movement"], 
    #                        attack_type=UNIT_TYPE_CODE[unit_type]["attack_type"]))
    #     unit_id += 1

    [team_1[i].set_y(i) for i in range(len(team_1))]
    for u in team_1:
        war_map.set_unit(u) 

    # for place, unit in enumerate(team_1):
    #     unit.position["y"] = place
    #     print(unit.position)
    #     war_map.set_unit(unit)

    team_2 = []

    team_2 = [Unit(unit_id + 3, 2, unit_type, 
                    movement=UNIT_TYPE_CODE[unit_type]["movement"], 
                    attack_type=UNIT_TYPE_CODE[unit_type]["attack_type"]) for unit_id, unit_type in enumerate(UNIT_TYPE_CODE)]
    
    [team_2[i].set_y(i) for i in range(len(team_2))]
    [team_2[i].set_x(war_map.tiles.shape[1] - 1) for i in range(len(team_2))]
    for u in team_2:
        war_map.set_unit(u) 
    
    # for unit_type in UNIT_TYPE_CODE:
    #     team_2.append(Unit(unit_id, 2, unit_type, 
    #                        movement=UNIT_TYPE_CODE[unit_type]["movement"], 
    #                        attack_type=UNIT_TYPE_CODE[unit_type]["attack_type"]))
    #     unit_id +=1

    # for place, unit in enumerate(team_2):
    #     unit.position["y"] = place
    #     unit.position["x"] = war_map.tiles.shape[1] - 1
    #     war_map.set_unit(unit)

    return team_1, team_2, war_map
