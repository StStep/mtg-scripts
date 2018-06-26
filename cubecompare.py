## Take a CubeTutor csv and compare it to a Decked Builder collection
## Create a Decked Builder collection of the missing cards

import io

class Card:
    def __init__(self, id, r, f):
        self.id = id
        self.r = r
        self.f = f

def compare_collection(in_collection, cube, out_collection):
    cards = read_collection(in_collection)
    cubelist = get_cube_list(cube)

    missing = []
    for c in cubelist:
        pass

    write_collection(out_collection, missing)

def read_collection(path):
    ret = {}
    with open(path) as f:
        id = 0
        reg = 0
        foil = 0
        for line in f:
            sline = line[6:]
            if sline.startswith('id:'):
                if id != 0:
                    ret[id] = Card(id, reg, foil)
                    id = 0
                    reg = 0
                    foil = 0
                id = int(sline[4:])
            elif sline.startswith('r:'):
                reg = int(sline[3:])
            elif sline.startswith('f:'):
                foil = int(sline[3:])
            else:
                pass
    return ret

def get_cube_list(path):
    ret = []
    with open(path) as f:
        for line in f:
            ret.append(line.split(',')[0][1:-1])
    return ret

def write_collection(path, cards):
    f = io.open(path, 'w', newline='\n')
    f.write(u'doc:\n- version: 1\n- items:\n')
    for c in cards:
        if c.r <= 0 and c.f <= 0:
            continue

        f.write(u'  - - id: {}\n'.format(c.id))
        if c.r > 0:
            f.write(u'    - r: {}\n'.format(c.r))
        if c.f > 0:
            f.write(u'    - f: {}\n'.format(c.f))
    f.close()

if __name__ == '__main__':
    compare_collection('./StephensCollection.coll2', './cardkingdom_starter_cube_version_4.csv', './OutCollection.coll')
