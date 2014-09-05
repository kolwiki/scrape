import os
import pullItemData
import pullMonsterData
import sqlite3

DATABASE_NAME = "test.db"

# 'main' method
def createTable(thingList):
    __createDatabase()
    __createAndroidMetadataTable()
    __createTable(thingList)

# creates db file if it doesn't already exist
def __createDatabase():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)

# creates required Android metadata table
def __createAndroidMetadataTable():
    con = sqlite3.connect(DATABASE_NAME)

    with con:
        cur = con.cursor()

        # id table, deleting previous version if it exists
        cur.execute('DROP TABLE IF EXISTS android_metadata')
        cur.execute('CREATE TABLE "android_metadata" ("locale" TEXT DEFAULT \'en_US\')')
        cur.execute('INSERT INTO "android_metadata" VALUES (\'en_US\')')

# create table by calling appropriate method for table type
def __createTable(thingList):
    if type(thingList[0]).__name__ == 'Monster':
        __writeMonsterTable(thingList)
    elif type(thingList[0]).__name__ == 'Item':
        __writeItemTable(thingList)
    elif type(thingList[0]).__name__ == 'Zone':
        __writeZoneTable(thingList)
    elif type(thingList[0]).__name__ == 'Class': # might cause trouble'?
        __writeClassTable()
    elif type(thingList[0]).__name__ == 'Skill':
        __writeSkillTable()
    elif type(thingList[0]).__name__ == 'Familiar':
        __writeFamiliarTable()
    elif type(thingList[0]).__name__ == 'Location':
        __writeLocationTable()
    else:
        raise TypeError('Unexpected list object, type: ' + str(type(thingList[0])))

def __writeMonsterTable(thingList):

    con = sqlite3.connect(DATABASE_NAME)

    with con:
        cur = con.cursor()

        # create monster table, deleting previous version if it exists
        cur.execute("DROP TABLE IF EXISTS Monsters")
        cur.execute("CREATE TABLE Monsters(_id INT PRIMARY KEY, name TEXT, descr TEXT, hp INT, att INT, def INT, sm INT, init INT, ml INT, res TEXT, meat REAL, phylum TEXT, element TEXT, url TEXT, location TEXT, items TEXT)")

        for monster in thingList:
            query = 'INSERT INTO Monsters(_id, name, descr, hp, att, def, sm, init, ml, res, meat, phylum, element, url, location, items) VALUES(' \
                    '"' + str (monster.id) + '", ' \
                    '"' + monster.name + '", ' \
                    '"' + monster.description + '", ' \
                    '"' + str (monster.hp) + '", ' \
                    '"' + str (monster.attack) + '", ' \
                    '"' + str (monster.defense) + '", ' \
                    '"' + str (monster.safeMoxie) + '", ' \
                    '"' + str (monster.initiative) + '", ' \
                    '"' + str (monster.attack) + '", ' \
                    '"' + monster.physicalRes + '", ' \
                    '"' + str (monster.meat) + '", ' \
                    '"' + monster.phylum + '", ' \
                    '"' + monster.element + '", ' \
                    '"' + monster.iURL + '", ' \
                    '"' + monster.location + '", ' \
                    '"' + monster.items + '")'
        
            print query
            cur.execute(query)

def __writeItemTable(thingList):

    con = sqlite3.connect(DATABASE_NAME)

    with con:
        cur = con.cursor()

        # create item table, deleting previous version if it exists
        cur.execute('DROP TABLE IF EXISTS Items')
        cur.execute('CREATE TABLE Items(_id INT PRIMARY KEY, name TEXT, type TEXT, descr TEXT, sellPrice INT, tradable TEXT, discardable TEXT, questItem TEXT, location TEXT, requirement TEXT, power INT, size INT, adventures INT, ' \
                    'stats TEXT, enchantment TEXT, duration TEXT, quality TEXT)')

        for item in thingList:
            query = 'INSERT INTO Items(_id, name, type, descr, sellPrice, tradable, discardable, questItem, location, requirement, power, size, adventures, stats, enchantment, duration, quality ) VALUES(' \
                    '"' + str (item.id) + '", ' \
                    '"' + item.name + '", ' \
                    '"' + item.itemType + '", ' \
                    '"' + item.description + '", ' \
                    '"' + str (item.sellPrice) + '", ' \
                    '"' + str (item.tradable) + '", ' \
                    '"' + str (item.discardable) + '", ' \
                    '"' + str (item.questItem) + '", ' \
                    '"' + item.location + '", ' \
                    '"' + item.requirement + '", ' \
                    '"' + str (item.power) + '", ' \
                    '"' + str (item.size) + '", ' \
                    '"' + item.adventures + '", ' \
                    '"' + item.stats + '", ' \
                    '"' + item.enchantment + '", ' \
                    '"' + str (item.duration) + '", ' \
                    '"' + item.quality + '")'
        
            print query
            cur.execute(query)

def __writeZoneTable():
    pass

def __writeClassTable():
    pass

def __writeSkillTable():
    pass

def __writeFamiliarTable():
    pass

def __writeLocationTable():
    pass
