from bs4 import BeautifulSoup
import urllib2
import re

TESTURL = "http://kol.coldfront.net/thekolwiki/index.php/Data:1335_HaXx0r"

class Monster:

    def __init__(self, dataTable, id):
        self.id = id
        self.name = dataTable['Name']
        self.hp = dataTable['Hitpoints']
        self.attack = dataTable

    def printMonster(self):
        pass
##        print("\n\n")
##        print("Name: " + self.name)
##        print("ID: " + self.id)
##        print("HP: " + self.hp)
##        print("Attack: " + self.attack)
##        print("Defense: " + self.defense)
##        print("Safe moxie: " + self.safeMoxie)
##        print("Initiative: " + self.initiative)
##        print("Meat: " + self.meat)
##        print("Element: " + self.element)
##        print("iURL: " + self.iURL)
##        print("Phylum: " + self.phylum)

def pullData(url):
    dataTable = dict()
    print(url)
    soup =  BeautifulSoup(urllib2.urlopen(url))
    monsterDiv = soup.find("div", { "class" : "mw-content-ltr" })
    monsterLIs = monsterDiv.find_all("li")
    i = 0
    for li in monsterLIs:
        textSplit = li.text.rsplit("-", 1)
        print (textSplit)
        if textSplit[0].strip().split(" ")[0] in ['Meat', 'Items']:
            textSplit = li.text.split("-",1)
        dataTable[textSplit[0].strip()] = textSplit[1].strip()
    dataTable["Name"] = (re.sub('^an* ', '', dataTable["Name"])) #removing 'a' and 'an' from names
    return dataTable

def main():
    monsterList = list()
    #monsterURLFile = open('monsterdataurls', 'r')
    id = 100000
    #for line in monsterURLFile:
    #    monsterList.append(Monster(pullData(line),id))
    #    id = id + 1
    #monsterURLFile.close()
    monsterList.append(Monster(pullData(TESTURL),id))
    for monster in monsterList:
        monster.printMonster()

if __name__ == '__main__':
    main()



