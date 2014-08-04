from bs4 import BeautifulSoup
import urllib2
import re
import unicodedata

class Monster:
    def __init__(self, dataTable ):
        self.name = dataTable[0]
        self.phylum = dataTable[1]
        self.iURL = dataTable[2]
        self.hp = dataTable[3]
        self.attack = dataTable[4]
        self.defence = dataTable[5]
        self.safeMoxie = dataTable[6]
        self.initiative = dataTable[7]
        self.meat = dataTable[8]
        self.element = dataTable[9]

def pullData(url):
    dataTable = list()
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
            thisLI = str(thisLI).strip()
            thisLI = "" + thisLI
        i = i + 1
    dataTable[0] = (re.sub('^an* ', '', dataTable[0])) #removing 'a' and 'an' from entries
    dataTable[2] = "http://cdn.coldfront.net/thekolwiki/images/1/1b/" + (dataTable[2].strip('()')) #imageURL
    return dataTable

def main():
    monsterList = list()
    monsterURLFile = open('monsterdataurls', 'r')
    #for line in monsterURLFile:
    #    monsterList.append(Monster(pullData(line))
    monsterURLFile.close()
    print(pullData("http://kol.coldfront.net/thekolwiki/index.php/Data:1335_HaXx0r"))


if __name__ == '__main__':
    main()



