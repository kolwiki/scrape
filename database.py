import os
import sqlite3

DATABASE_NAME = "test.db"

# 'main' method
def createTable(thingList):
    __createDatabase()
    __writeTable(thingList)

# creates db file if it doesn't already exist
def __createDatabase():
    if not os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)

# writes table by calling appropriate method for table type
def __writeTable(thingList):
    if type(thingList[0]) is Monster:
        __writeMonsterTable()
##    elif type(thingList[0]) is Item:
##        __writeItemTable()
##    elif type(thingList[0]) is Zone:
##        __writeZoneTable()
##    elif type(thingList[0]) is Class: # might cause trouble?
##        __writeClassTable()
##    elif type(thingList[0]) is Skill:
##        __writeSkillTable()
##    elif type(thingList[0]) is Familiar:
##        __writeFamiliarTable()
##    elif type(thingList[0]) is Location:
##        __writeLocationTable()
    else:
        raise TypeError('Unexpected list object, type: ' + type(thingList[0]))

def __writeMonsterTable():
    con = sqlite3.connect(DATABASE_NAME)

    with con:
        cur = con.cursor()

        # create monster table, deleting previous version if it exists
        cur.execute("DROP TABLE IF EXISTS Monsters")
        cur.execute("CREATE TABLE Monsters(id INT PRIMARY KEY, name TEXT, hp INT, att INT, def INT, sm INT, init INT, ml INT, res TEXT, meat REAL, phylum TEXT, element TEXT, description TEXT")

        # add monsters to table
        for monster in thingList:
            query = "INSERT INTO Monsters(id, name, hp, att, def, sm, init, ml, res, meat, phylum, element, description) VALUES(" \
                    "'" + str (monster.id) + "', " \
                    "'" +  monster.name + "', " \
                    "'" + str (monster.hp) + "', " \
                    "'" + str (monster.attack) + "', " \
                    "'" + str (monster.defense) + "', " \
                    "'" + str (monster.safeMoxie) + "', " \
                    "'" + str (monster.initiative) + "', " \
                    "'" + str (monster.attack) + "', " \
                    "'" + monster.element + "', " \
                    "'" + str (monster.meat) + "', " \
                    "'" + monster.phylum + "', " \
                    "'" + monster.element + "', " \
                    "'" + monster.name + "')"

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
