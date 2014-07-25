import os
import sqlite3
from bs4 import BeautifulSoup

# pages = ['pimpdata.html', 'monkdata.html']
DATA_PATH = 'monsters/data'
DATABASE_NAME = 'test.db'
FIELD_NAMES = {
    'Name': 'Name',
    'Phylum': 'Phylum',
    'Hitpoints': 'Hp',
    'Attack power': 'Att',
    'Defense power': 'Def',
    'Moxie for no-hit' : 'Safe',
    'Initiative': 'Init',
    'Meat gained': 'Meat',
    'Items dropped': 'Drops',
    'Location encountered': 'Locations',
    'Elemental alignment': 'Element',
    'Physical resistance': 'Resistance'
}

data_files = [ f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH,f)) ]

# rebuilding db each time
if os.path.exists(DATABASE_NAME):
    os.remove(DATABASE_NAME)

con = sqlite3.connect(DATABASE_NAME)
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Monsters(Id INT PRIMARY KEY, Name TEXT, Locations TEXT, Drops TEXT, Hp TEXT, Att TEXT, Def TEXT, Safe TEXT, Init TEXT, Resistance TEXT, Meat TEXT, Phylum TEXT, Element TEXT, Description TEXT)")

id = 1000000 - 1

for page in data_files:
    id += 1    

    soup = BeautifulSoup(open(os.path.join(DATA_PATH, page)))

    div = soup.find("div", { "class" : "mw-content-ltr" })

    list_items = div.find_all("li")

    pairs = []

    for li in list_items:
        pairs.append(li.get_text().strip().split(" - "))

    details = {'Id': str(id)} # making it a string for now

    for pair in pairs:
        field_name = FIELD_NAMES.get(pair[0])
        if field_name != None:

            # remove 'a' or 'an' at beginning of name
            if field_name == 'Name':
                if pair[1][:2] == 'a ':
                    pair[1] = pair[1][2:]
                elif pair[1][:3] == 'an ':
                    pair[1] = pair[1][3:]
                else:
                    pair[1] = pair[1][1:]

            details[field_name] = pair[1]

    # print details


    with con:

        fields = ["Id", "Name", "Locations", "Drops", "Hp", "Att", "Def", "Safe", "Init", 
                  "Resistance", "Meat", "Phylum", "Element", "Description"]

        # TODO resistances etc has text 'none', replace with null or something?

        query = ("INSERT INTO Monsters (" + ", ".join(fields) + ") VALUES (")

        for field in fields:
            detail = details.get(field)

            if detail != None:
                if "'" in detail:
                    detail = '"' + detail + '"'
                else:
                    detail = "'" + detail + "'" # TEXT fields must be surrounded by quotes

                query += detail

            else: 
                query += '""'

            query += ", "

        query = query[:-2] + ")"

        # print query
    
        cur.execute(query)

        print "Added entry to " + DATABASE_NAME + " for " + details['Name'] + " (" + details['Id'] + ")"
        
