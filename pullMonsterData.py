from bs4 import BeautifulSoup
import urllib2
import re
import os.path

TESTMODE = 0
TESTURL = "http://kol.coldfront.net/thekolwiki/index.php/Data:1335_HaXx0r"

class Monster(object):

    def __init__(self, dataTable, id):

        if dataTable == None:
            print 'dataTable is None'

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
        self.description = dataTable['Description']

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
        print("Description: " + self.description)

def pullData(url):
    dataTable = dict()
    print(url)

    try:
        soup =  BeautifulSoup(urllib2.urlopen(url))
        monsterDiv = soup.find("div", { "class" : "mw-content-ltr" })
        monsterLIs = monsterDiv.find_all("li")
        i = 0
        for li in monsterLIs:
            textSplit = li.text.encode('utf8').rsplit("-", 1)
            if textSplit[0].strip().split(" ")[0] in ['Name', 'Meat', 'Items', 'Location', 'Attack', 
                                                      'Defense', 'Image', 'Hitpoints', 'Phylum']:
                textSplit = li.text.encode('utf8').split("-",1)
            dataTable[textSplit[0].strip()] = textSplit[1].strip().replace('"',"'")

        imageFilename = dataTable["Image"][1:-1].replace('_',' ')
        if imageFilename[0].islower():
            imageFilename = imageFilename.capitalize()
        dataTable["Image"] = soup.find("img", { "alt" : imageFilename })['src'] # find correct iURL
        dataTable["Name"] = (re.sub('^an* ', '', dataTable["Name"])) #removing 'a' and 'an' from names

        # get description
        monsterUrl = url[:url.index('Data:')] + url[url.index('Data:') + 5:]   
        soup = BeautifulSoup(urllib2.urlopen(monsterUrl))
        fightingText = soup.find(text = re.compile("You're fighting"))
        if fightingText != None:
            description = fightingText.next.next.text.encode('utf8').replace('"',"'")
            if description[len(description)-1] == '\n':
                description = description[:-1]
            dataTable["Description"] = description
        else:
            f = open('desc_log', 'a')
            f.write(monsterUrl)
            f.close()
            dataTable["Description"] = ''

    except Exception as e: # TODO make for only urllib2 exception?
        print '* Exception *'
        f = open('desc_log', 'ab')
        f.write('EXCEPTION ' + e.__class__.__name__ + ': ' + url)
        return None

    return dataTable
           
def main():
    monsterList = list()
    monsterURLFile = open('monsterdataurls', 'r')
    id = 100000
    
    if not TESTMODE:
        for line in monsterURLFile:
            #monster = Monster(pullData(line),id)
            monsterData = pullData(line)            
            if monsterData != None:
                monster = Monster(monsterData, id)
                monsterList.append(monster) 
                monster.printMonster()        
            id = id + 1
        monsterURLFile.close()
    else:
        monsterData = pullData(TESTURL)
        if monsterData != None:
            monster = Monster(monsterData, id)
            monsterList.append(monster)
            monster.printMonster()

    #    for monster in monsterList:
    #        monster.printMonster()

    return monsterList

if __name__ == '__main__':
    main()



