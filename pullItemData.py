from bs4 import BeautifulSoup
import collections
import re
import urllib2

#TEST_PAGES = ['hat.html', 'shield.html']
TEST_PAGES = ['bling.html', 'slippers.html', 'flower.html']
#TEST_PAGES = ['staff.html', 'slippers.html']

soup = None

class Item(object):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, location):
        self.name = name
        self.description = description
        self.itemType = itemType
        self.sellPrice = sellPrice
        self.tradable = tradable
        self.discardable = discardable
        self.questItem = questItem
        self.location = location
        
class Gear(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, requirement, power, enchantment, location):
        super(Gear, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.requirement = requirement
        self.power = power
        self.enchantment = enchantment

    def __str__(self):
        return 'Name: {}\nDescription: {}\nItem type: {}\nSelling price: {}\nTradable: {}\nDiscardable: {}\nQuest item: {}' \
            '\n{}\n{}\nEnchantment: {}\nLocation: {}'.format(self.name, self.description, self.itemType, self.sellPrice, 
                                                                self.tradable, self.discardable, self.questItem, self.requirement, 
                                                                self.power, self.enchantment, self.location)

class TurnGen(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, size, adventures, stats, enchantment, quality, requirement, location):
        super(Gear, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.size = size
        self.adventures = adventures
        self.stats = stats
        self.enchantment = enchantment
        self.quality = quality
        self.requirement = requirement

class Potion(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, enchantment, duration, location):
        super(Gear, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.enchantment = enchantment
        self.duration = duration

class Usable(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, enchantment, location):
        super(Gear, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.enchantment = enchantment

class Familiar(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, location):
        super(Gear, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
    
class Ingredients(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, location):
        super(Gear, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
    
def getName(soup):
    return str(soup.title.getText().split(' - ')[0])

def getItemType(soup):
    return soup.find(text=re.compile(r'Type: ')).next.getText()

def getSellPrice(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    sellPrice = None
    priceIndex = itemStrings.index(u'Selling Price: ') if u'Selling Price: ' in itemStrings else None
    if priceIndex != None:
        sellPrice = itemStrings[priceIndex + 1][:-1].lower()
    
    return sellPrice

def getTradable(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    return (not u'Cannot be traded' in itemStrings) and (not u'Cannot be traded or discarded' in itemStrings)

def getDiscardable(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    return (not u'Cannot be discarded' in itemStrings) and (not u'Cannot be traded or discarded' in itemStrings)

def getQuestItem(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    return u'Quest Item' in itemStrings

def getLocation(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    location = None
    location = soup.find('dl')

    # TODO bug: this goes for first dl so breaks if there is an extra one eg from complaints etc

    if location != None:
        location = location.getText().encode('utf8').replace('\n','\n\t')

    return location

def getRequirement(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    requirement = None
    reqIndex = itemStrings.index(u' Required: ') if u' Required: ' in itemStrings else None
    if reqIndex != None:
        requirement = itemStrings[reqIndex - 1] + itemStrings[reqIndex] + itemStrings[reqIndex + 1]

    if requirement == None:
        requirement = 'Requirement: None'

    return requirement    

def getEnchantment(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')

    enchantment = itemDiv.find('span', { 'style' : 'color:blue;font-weight:bold' })
    if enchantment != None:
        enchantment = ', '.join(list(enchantment.strings))

    return enchantment        

def getPower(soup): # TODO expand to include damage reduction
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    power = "Power: None"

    powerIndex = itemStrings.index(u'Power: ') if u'Power: ' in itemStrings else None
    if powerIndex != None:
        power = 'Power: ' + itemStrings[powerIndex + 1]

    drIndex = itemStrings.index(u'Damage Reduction: ') if u'Damage Reduction: ' in itemStrings else None
    if drIndex != None:
        power = 'Damage Reduction: ' + itemStrings[drIndex + 1]
    
    return power

def getDescription(soup):
    return None

def pullItemData(url):
    soup = BeautifulSoup(open(url))

    type = soup.find(text=re.compile(r'Type: ')).next.getText()

    if (type in ['accessory', 'back', 'shirt']):
        return pullGearData(soup)
    elif (type in ['hat', 'pants', 'offhand']) or ('handed' in type) or ('off-hand item' in type):
        return pullPowerGearData(soup)
    else:
        raise TypeError('Unknown item type: ' + type)

# gear without power attribute
def pullGearData(soup):
    return Gear(getName(soup), getDescription(soup), 'Accessory', getSellPrice(soup), getTradable(soup), getDiscardable(soup), getQuestItem(soup), getRequirement(soup), None, getEnchantment(soup), getLocation(soup))

# gear with power attribute
def pullPowerGearData(soup):
    return Gear(getName(soup), getDescription(soup), 'Hat', getSellPrice(soup), getTradable(soup), getDiscardable(soup), getQuestItem(soup), getRequirement(soup), getPower(soup), getEnchantment(soup), getLocation(soup))

def main():
    itemList = list()
    #monsterURLFile = open('monsterdataurls', 'r')
    #for line in monsterURLFile:
    #    monsterList.append(Monster(pullData(line))
    #monsterURLFile.close()

    for page in TEST_PAGES:
        print pullItemData(page)
#        pullItemData(page)

if __name__ == '__main__':
    main()



