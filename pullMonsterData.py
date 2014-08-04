from bs4 import BeautifulSoup
import urllib2
import re

TESTURL = "http://kol.coldfront.net/thekolwiki/index.php/Data:1335_HaXx0r"

class Monster:
    def __init__(self, dataTable, id):
        self.name = dataTable[0]
        self.phylum = dataTable[1]
        self.iURL = dataTable[2]
        self.hp = dataTable[3]
        self.attack = dataTable[4]
        self.defense = dataTable[5]
        self.safeMoxie = dataTable[6]
        self.initiative = dataTable[7]
        self.meat = dataTable[8]
        self.element = dataTable[9]
        self.id = "1"+ str(id)

    def printMonster(self):
        print("\n\n")
        print("Name: " + self.name)
        print("ID: " + self.id)
        print("HP: " + self.hp)
        print("Attack: " + self.attack)
        print("Defense: " + self.defense)
        print("Safe moxie: " + self.safeMoxie)
        print("Initiative: " + self.initiative)
        print("Meat: " + self.meat)
        print("Element: " + self.element)
        print("iURL: " + self.iURL)
        print("Phylum: " + self.phylum)

def pullData(url):
    dataTable = list()
    print(url)
    soup =  BeautifulSoup(urllib2.urlopen(url))
    monsterDiv = soup.find("div", { "class" : "mw-content-ltr" })
    monsterLIs = monsterDiv.find_all("li")
    i = 0
    for li in monsterLIs:
        if (i == 0) or (i==2) or (i>2 and i<9) or (i==14): #Fields to be included
            thisLI = li.text.rsplit("-",1)
            thisLI = str(thisLI[1]).strip()
            dataTable.append(thisLI)
        if (i==9): #Cleaning up meat
            thisLI = li.text.split("=",1)
            thisLI = str(thisLI[0]).strip()
            thisLI = thisLI[thisLI.find("-")+2:len(thisLI)]
            dataTable.append(thisLI)
        i = i + 1
    dataTable[0] = (re.sub('^an* ', '', dataTable[0])) #removing 'a' and 'an' from entries
    dataTable[2] = "http://cdn.coldfront.net/thekolwiki/images/1/1b/" + (dataTable[2].strip('()')) #imageURL
    return dataTable

def main():
    monsterList = list()
    #monsterURLFile = open('monsterdataurls', 'r')
    id = 10000
    #for line in monsterURLFile:
    #    monsterList.append(Monster(pullData(line),id))
    #    id = id + 1
    #monsterURLFile.close()
    monsterList.append(Monster(pullData(TESTURL),id))
    for monster in monsterList:
        monster.printMonster()

if __name__ == '__main__':
    main()



