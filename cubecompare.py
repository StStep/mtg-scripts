## Take a CubeTutor csv and compare it to a Decked Builder collection
## Create a Decked Builder collection of the missing cards

import io
import scrython
import time
import csv
import shelve

class DeckedBuildCollEntry:
    def __init__(self, id, r, f):
        self.id = id
        self.r = r
        self.f = f

def compare_collection(in_collection, cube, out_collection):
    collentries = read_collection(in_collection)
    cubelist = get_cube_list(cube)

    # Load cache
    refids = shelve.open('refids')
    refprice = shelve.open('refprice')

    # Request Data
    missingentries = []
    missingcost = 0
    for c in cubelist:
        # Load missing values
        if not c in refids or not c in refprice:
            time.sleep(0.05)
            (refprice[c], refids[c]) = get_possible_mutliverse_ids(c)
        have = False
        for i in refids[c]:
            if i in collentries:
                have = True
                break;
        if not have:
            missingentries.append(DeckedBuildCollEntry(refids[c][0], 1, 0))
            missingcost += float(refprice[c])

    # Save cache
    refids.close()
    print("Missing {} cards with estimate cost of {:0.2f} dollars".format(len(missingentries), missingcost))

    write_collection(out_collection, missingentries)

# Using name, return list of all printed Multiverse IDs
# and cheapest price
def get_possible_mutliverse_ids(name):
    search = scrython.cards.Search(q='!"'+name+'" game:paper', unique='prints', order='usd', dir='asc')
    if search.total_cards() > len(search.data()):
        print('Warning: Only looking at 1 page when more exist')

    ret = []
    price = None
    # Prepend Multiverse ID used for price, otherwise append
    for i in range(len(search.data())):
        if price == None and 'usd' in search.data()[i]:
            price = search.data()[i]['usd']
            ret = search.data()[i]['multiverse_ids'] + ret
        else:
            ret.extend(search.data()[i]['multiverse_ids'])
    return (price, ret)

# Read in Decked Builder collection
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
                    ret[id] = DeckedBuildCollEntry(id, reg, foil)
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

# Get cube list from CubeTutor CSV export
def get_cube_list(path):
    ret = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ret.append(row[0])
    return ret

# Write out as Decked Builder collection
def write_collection(path, collentries):
    f = io.open(path, 'w', newline='\n')
    f.write(u'doc:\n- version: 1\n- items:\n')
    for c in collentries:
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
