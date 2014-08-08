import os
import sqlite3
import pullMonsterData

DATABASE_NAME = "test.db"

# 'main' method
def createTable(thingList):
#    __createDatabase()
    __writeTable(thingList)

# creates db file if it doesn't already exist
def __createDatabase():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)

# writes table by calling appropriate method for table type
def __writeTable(thingList):
    if type(thingList[0]).__name__ == 'Monster':
        __writeMonsterTable(thingList)
    elif type(thingList[0]).__name__ == 'Item':
        __writeItemTable()
    elif type(thingList[0]).__name__ == 'Zone':
        __writeZoneTable()
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
        cur.execute("CREATE TABLE Monsters(id INT PRIMARY KEY, name TEXT, hp INT, att INT, def INT, sm INT, init INT, ml INT, res TEXT, meat REAL, phylum TEXT, element TEXT, description TEXT)")

        # # add monsters to table
        # for monster in thingList:
        #     query = "INSERT INTO Monsters(id, name, hp, att, def, sm, init, ml, res, meat, phylum, element, description) VALUES(" \
        #             "'" + str (monster.id) + "', " \
        #             "'" +  monster.name + "', " \
        #             "'" + str (monster.hp) + "', " \
        #             "'" + str (monster.attack) + "', " \
        #             "'" + str (monster.defense) + "', " \
        #             "'" + str (monster.safeMoxie) + "', " \
        #             "'" + str (monster.initiative) + "', " \
        #             "'" + str (monster.attack) + "', " \
        #             "'" + monster.element + "', " \
        #             "'" + str (monster.meat) + "', " \
        #             "'" + monster.phylum + "', " \
        #             "'" + monster.element + "', " \
        #             "'" + monster.name + "')"
        
        for monster in thingList:
            query = 'INSERT INTO Monsters(id, name, hp, att, def, sm, init, ml, res, meat, phylum, element, description) VALUES(' \
                    '"' + str (monster.id) + '", ' \
                    '"' +  monster.name + '", ' \
                    '"' + str (monster.hp) + '", ' \
                    '"' + str (monster.attack) + '", ' \
                    '"' + str (monster.defense) + '", ' \
                    '"' + str (monster.safeMoxie) + '", ' \
                    '"' + str (monster.initiative) + '", ' \
                    '"' + str (monster.attack) + '", ' \
                    '"' + monster.element + '", ' \
                    '"' + str (monster.meat) + '", ' \
                    '"' + monster.phylum + '", ' \
                    '"' + monster.element + '", ' \
                    '"' + monster.name + '")'
        
            print query
            cur.execute(query)

def __writeItemTable():
    pass

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
