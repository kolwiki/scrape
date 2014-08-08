from bs4 import BeautifulSoup
import collections
import re
import urllib2

#TEST_PAGES = ['cold.html']
TEST_PAGES = ['cold.html', 'mae.html']
#TEST_PAGES = ['hat.html', 'shield.html']
#TEST_PAGES = ['bling.html', 'slippers.html', 'flower.html']
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
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, requirement, power, enchantment, 
                 location):
        super(Gear, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.requirement = requirement
        self.power = power
        self.enchantment = enchantment

    def __str__(self):
        return 'Name: {}\nDescription: {}\nItem type: {}\nSelling price: {}\nTradable: {}\nDiscardable: {}\nQuest item: {}' \
            '\n{}\n{}\nEffect: {}\nLocation: {}\n'.format(self.name, self.description, self.itemType, self.sellPrice, 
                                                                self.tradable, self.discardable, self.questItem, self.requirement, 
                                                                self.power, self.enchantment, self.location)

class TurnGen(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, size, adventures, stats, 
                 enchantment, quality, requirement, location):
        super(TurnGen, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.size = size
        self.adventures = adventures
        self.stats = stats
        self.enchantment = enchantment
        self.quality = quality
        self.requirement = requirement

    def __str__(self):
        return 'Name: {}\nDescription: {}\nItem type: {}\nQuality: {}\nSize: {}\nLevel required: {}\nAdventures gained: {}' \
            '\nStats gained: {}\nSelling price: {}\nTradable: {}\nDiscardable: {}\nQuest item: {}' \
            '\nEnchantment: {}\nLocation: {}'.format(self.name, self.description, self.itemType, self.quality, self.size, 
                                                     self.requirement, self.adventures, self.stats, self.sellPrice, 
                                                     self.tradable, self.discardable, self.questItem, self.enchantment, 
                                                     self.location)

class Potion(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, enchantment, duration, location):
        super(Potion, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.enchantment = enchantment
        self.duration = duration

class Usable(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, enchantment, location):
        super(Usable, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
        self.enchantment = enchantment

class Familiar(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, location):
        super(Familiar, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
    
class Ingredients(Item):
    def __init__(self, name, description, itemType, sellPrice, tradable, discardable, questItem, location):
        super(Ingredients, self).__init__(name, description, itemType, sellPrice, tradable, discardable, questItem, location)
    
def getName(soup):
    return str(soup.title.getText().split(' - ')[0])

def getItemType(soup):
    return soup.find(text=re.compile(r'Type: ')).next.getText()

def getSellPrice(soup):   
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)
 
    sellPrice = None
    priceIndex = stringIndex(soup, u'Selling Price: ')
    if priceIndex != None:
        sellPrice = itemStrings[priceIndex + 1][:-1].lower()
    
    return sellPrice

def getTradable(soup):
    return (not (inItemStrings(soup, u'Cannot be traded'))) and (not (inItemStrings(soup, u'Cannot be traded or discarded')))

def getDiscardable(soup):
    return (not inItemStrings(soup, u'Cannot be discarded')) and (not inItemStrings(soup, u'Cannot be traded or discarded'))

def getQuestItem(soup):
    return inItemStrings(soup, u'Quest Item')

def getLocation(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    location = None
    location = soup.find('dl')

    # TODO bug: this goes for first dl so breaks if there is an extra one eg from complaints etc

    if location != None:
        location = location.getText().encode('utf8').replace('\n','\n\t').strip()

    return location

def getRequirement(soup):
    requirement = 'Requirement: None'
    reqIndex = stringIndex(soup, u' Required: ')
    if reqIndex != None:
        requirement = getItemString(soup, reqIndex - 1) + getItemString(soup, reqIndex) + getItemString(soup, reqIndex + 1)

    return requirement    

def getEnchantment(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')

    enchantment = itemDiv.find('span', { 'style' : 'color:blue;font-weight:bold' })
    if enchantment != None:
        enchantment = ', '.join(list(enchantment.strings))

    return enchantment        

def getPower(soup):
    power = "Power: None"

    powerIndex = stringIndex(soup, u'Power: ')
    if powerIndex != None:
        power = 'Power: ' + getItemString(soup, powerIndex + 1)

    drIndex = stringIndex(soup, u'Damage Reduction: ')
    if drIndex != None:
        power = 'Damage Reduction: ' + getItemString(soup, drIndex + 1)

    return power

# TODO needs fixing eg. 'cold.html'
def getDescription(soup):
    name = str(soup.title.getText().split(' - ')[0])

    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    lowerStrings = [string.lower() for string in itemStrings]
    return itemStrings[lowerStrings.index(name.lower()) + 1].strip()

def getEffect(soup):
    effect = None

    effectIndex = stringIndex(soup, u'Effect: ')
    if effectIndex != None:
        effect = getItemString(soup, effectIndex + 1)

    return effect

def getLevelRequirement(soup):
    requirement = None

    reqIndex = stringIndex(soup, u'Level required: ')
    if reqIndex != None:
        requirement = getItemString(soup, reqIndex + 1)
    
    return requirement    

def getSize(soup):
    size = None

    sizeIndex = stringIndex(soup, u'Size: ')
    if sizeIndex == None:
        sizeIndex = stringIndex(soup, u'Potency: ')

    if sizeIndex != None:
        size = getItemString(soup, sizeIndex + 1)

    return size

def getAdventures(soup):
    advText = soup.find('a', {'title' : 'Adventures'}).next.next.getText().strip()
    adventures = re.search(r'\d+-\d+', advText).group()
    
    return adventures
    
def getStats(soup):
    stats = [0,0,0]

    statTags = soup.find_all('a', {'title' : re.compile(r'Substat')})
    for tag in statTags:
        gain = re.search(r'\d+-\d+', tag.previous).group()
        if (tag.next == 'Beefiness'):
            stats[0] = gain
        elif (tag.next == 'Magicalness'):
            stats[1] = gain
        elif (tag.next == 'Roguishness'):
            stats[2] = gain

    return ', '.join(str(s) for s in stats)

def getTurnGenQuality(soup):
    return soup.find(text=re.compile(r'Type: ')).next.next.next.getText().strip()[1:-1]

# returns index of given string in item details div, or None if not found
def stringIndex(soup, string):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    if string in itemStrings:                        
        return itemStrings.index(string)
    else:
        return None

# returns a given string from the list of detail strings
def getItemString(soup, index):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    return itemStrings[index]

# checks if a given string is in list of item detail strings
def inItemStrings(soup, string):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)

    return string in itemStrings

# debug
def printItemStrings(soup):
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)
    print itemStrings

def pullItemData(url):
    soup = BeautifulSoup(open(url))

    type = soup.find(text=re.compile(r'Type: ')).next.getText()

    if (type in ['accessory', 'back', 'shirt', 'hat', 'pants', 'offhand']) or ('handed' in type) or ('off-hand item' in type):
        return pullGearData(soup)
    elif ('food' in type) or ('booze' in type):
        return pullTurnGenData(soup)
    else:
        raise TypeError('Unknown item type: ' + type)

# gear
def pullGearData(soup):
    return Gear(getName(soup), getDescription(soup), getItemType(soup), getSellPrice(soup), getTradable(soup), getDiscardable(soup), 
                getQuestItem(soup), getRequirement(soup), getPower(soup), getEnchantment(soup), getLocation(soup))

# food/booze
def pullTurnGenData(soup):    
    tg = TurnGen(getName(soup), getDescription(soup), getItemType(soup), getSellPrice(soup), getTradable(soup), getDiscardable(soup), 
                   getQuestItem(soup), getSize(soup), getAdventures(soup), getStats(soup), getEffect(soup), getTurnGenQuality(soup),
                   getLevelRequirement(soup), getLocation(soup))

    print tg
    return tg

def main():
    itemList = list()
    #monsterURLFile = open('monsterdataurls', 'r')
    #for line in monsterURLFile:
    #    monsterList.append(Monster(pullData(line))
    #monsterURLFile.close()

    for page in TEST_PAGES:
        #print pullItemData(page)
        pullItemData(page)
        print

if __name__ == '__main__':
    main()



