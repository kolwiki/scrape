from bs4 import BeautifulSoup
import urllib2
import re

TESTMODE = 0
TESTURL = "http://kol.coldfront.net/thekolwiki/index.php/Data:Bashful,_the_Reindeer"

class Monster(object):

    def __init__(self, dataTable, id):
        self.id = id
        self.name = dataTable['Name']
        self.hp = dataTable['Hitpoints']
        self.attack = dataTable['Attack power']
        self.defense = dataTable['Defense power']
        self.safeMoxie = dataTable['Moxie for no-hit']
        self.initiative = dataTable['Initiative']
        self.meat = dataTable['Meat gained']
        self.element = dataTable['Elemental alignment']
        self.physicalRes = dataTable['Physical resistance']
        self.iURL = dataTable['Image']
        self.phylum = dataTable['Phylum']
        self.items = dataTable['Items dropped']
        self.location = dataTable['Location encountered']

    def printMonster(self):
        print("Name: " + self.name)
        print("ID: " + str(self.id))
        print("HP: " + self.hp)
        print("Attack: " + self.attack)
        print("Defense: " + self.defense)
        print("Safe moxie: " + self.safeMoxie)
        print("Initiative: " + self.initiative)
        print("Meat: " + self.meat)
        print("Element: " + self.element)
        print("Physical resistance: " + self.physicalRes)
        print("iURL: " + self.iURL)
        print("Phylum: " + self.phylum)
        print("Location: " + self.location)
        print("Items: " + self.items)

def pullData(url):
    dataTable = dict()
    print(url)
    soup =  BeautifulSoup(urllib2.urlopen(url))
    monsterDiv = soup.find("div", { "class" : "mw-content-ltr" })
    monsterLIs = monsterDiv.find_all("li")
    i = 0
    for li in monsterLIs:
        textSplit = li.text.rsplit("-", 1)
        print textSplit
        #print textSplit[0].strip().split(" ")[0]
        if textSplit[0].strip().split(" ")[0] in ['Name', 'Meat', 'Items', 'Location', 'Attack', 
                                                  'Defense', 'Image', 'Hitpoints', 'Phylum']:
            textSplit = li.text.split("-",1)
        dataTable[textSplit[0].strip()] = textSplit[1].strip()

    imageFilename = dataTable["Image"][1:-1].replace('_',' ')
    if imageFilename[0].islower():
        imageFilename = imageFilename.capitalize()
    print imageFilename
    dataTable["Image"] = soup.find("img", { "alt" : imageFilename })['src'] # find correct iURL
    dataTable["Name"] = (re.sub('^an* ', '', dataTable["Name"])) #removing 'a' and 'an' from names
    
    return dataTable

def main():
    monsterList = list()
    monsterURLFile = open('monsterdataurls', 'r')
    id = 100000
    
    if not TESTMODE:
        for line in monsterURLFile:
            monster = Monster(pullData(line),id)
            monsterList.append(monster)
            monster.printMonster()        
            id = id + 1
        monsterURLFile.close()
    else:
        monsterList.append(Monster(pullData(TESTURL),id))

    for monster in monsterList:
            monster.printMonster()

    return monsterList

if __name__ == '__main__':
    main()



