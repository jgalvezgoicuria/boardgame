import numpy as np

from parameters import UNIT_TYPE_CODE

class map:
    def __init__(self, dimensions=[5, 5]):
        self.dimensions = dimensions
        self.tiles = np.zeros(dimensions)

    def remove_unit(self, unit):
        self.tiles[unit.position.x, unit.position.y] = 0
    
    def set_unit(self, unit):
        self.tiles[unit.position.x, unit.position.y] = int(str(unit.team) + str(unit.id))

    def check_ocupation(self, x, y):
        if self.tiles[x, y] == 0:
            return False
        else:
            return True

class unit:
    def __init__(self, id, team, 
                 hit_points = 50,
                 movement = 1,
                 position={'x': 0, 'y':0}, 
                 attack_type={'damage': 10,'distance': 1}):
        self.id = id
        self.team = team
        self.hit_points = hit_points
        self.movement = movement
        self.position = position
        self.attack_type = attack_type

    def attack(self, target, map):
        # Check if out of range:
        y_len = abs(self.position.y - target.position.y)
        x_len = abs(self.position.x - target.position.x)

        if y_len > self.attack_type.distance or x_len > self.attack_type.distance:
            print('Target out of range.')
            return 0
        
        # Do damage:
        target.hit_points -= self.attack_type.damage
        print('You hit!', 'And do ', self.attack_type.damage, 'damage.')
        print('The target left with',  target.hit_points, 'hit_points')

        # check if unit defeated:
        if target.hit_points <= 0:
            print('Unit defeated')
            map.remove_unit(target)
            return target.id
        else:
            return 0
        
    def movem(self, direction, map):

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


def create_unit(type, team, id):
    # unit_features = ['id', 'team', 'type', 'position', 'hit_points', 'movement', 'attack']
    
    unit = {}
    unit['id'] = id
    unit['type'] = type
    unit['team'] = team
    unit['position'] = {'x': 0, 'y':0}
    unit['hit_points'] = 50
    if unit['type'] == 'infantry':
        unit['movement'] = 1
        unit['attack'] = {
            'damage': 10,
            'distance': 1
        }
    elif unit['type'] == 'archery':
        unit['movement'] = 1
        unit['attack'] = {
            'damage': 10,
            'distance': 3
        }
    elif unit['type'] == 'cavalry':
        unit['movement'] = 3
        unit['attack'] = {
            'damage': 10,
            'distance': 1
        }        
    else:
        print('The wrong type of unit have been insert. Unit not generated.')
        return -1
    
    return unit


def search_unit(team, unit_id):
    for unit in team:
        if unit['id'] == int(unit_id):
            return unit       
    return 0


def show_map(map):
    for line in map:
        print(line)


def start(map):
    # create units and assing position
    team_1 = []
    for unit_type in UNIT_TYPE_CODE:
        team_1.append(create_unit(unit_type, '1', int('1' + UNIT_TYPE_CODE[unit_type])))

    for place, unit in enumerate(team_1):
        unit['position']['y'] = place
        map[unit['position']['y']][unit['position']['x']] = int(unit['team'] + UNIT_TYPE_CODE[unit['type']])

    team_2 = []
    for unit_type in UNIT_TYPE_CODE:
        team_2.append(create_unit(unit_type, '2', int('2' + UNIT_TYPE_CODE[unit_type])))

    for place, unit in enumerate(team_2):
        unit['position']['y'] = place + 2
        unit['position']['x'] = 4
        map[unit['position']['y']][unit['position']['x']] = int(unit['team'] + UNIT_TYPE_CODE[unit['type']])

    return team_1, team_2, map
