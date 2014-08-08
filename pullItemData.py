from bs4 import BeautifulSoup
import re
import urllib2

TEST_PAGES = ['bling.html', 'slippers.html', 'flower.html']
#TEST_PAGES = ['staff.html', 'slippers.html']

class Item(object):
    def __init__(self, name, itemType, sellPrice, tradable, discardable, questItem):
        self.name = name
        self.itemType = itemType
        self.sellPrice = sellPrice
        self.tradable = tradable
        self.discardable = discardable
        self.questItem = questItem
        
class Gear(Item):
    def __init__(self, name, itemType, sellPrice, tradable, discardable, questItem, requirement, power, enchantment):
        super(Gear, self).__init__(name, itemType, sellPrice, tradable, discardable, questItem)
        self.requirement = requirement
        self.power = power
        self.enchantment = enchantment

class TurnGen(Item):
    def __init__(self, name, itemType, sellPrice, tradable, discardable, questItem, size, adventures, stats, enchantment, quality, requirement):
        super(Gear, self).__init__(name, itemType, sellPrice, tradable, discardable, questItem)
        self.size = size
        self.adventures = adventures
        self.stats = stats
        self.enchantment = enchantment
        self.quality = quality
        self.requirement = requirement

class Potion(Item):
    def __init__(self, name, itemType, sellPrice, tradable, discardable, questItem, enchantment, duration):
        super(Gear, self).__init__(name, itemType, sellPrice, tradable, discardable, questItem)
        self.enchantment = enchantment
        self.duration = duration

class Usable(Item):
    def __init__(self, name, itemType, sellPrice, tradable, discardable, questItem, enchantment):
        super(Gear, self).__init__(name, itemType, sellPrice, tradable, discardable, questItem)
        self.enchantment = enchantment

class Familiar(Item):
    def __init__(self, name, itemType, sellPrice, tradable, discardable, questItem):
        super(Gear, self).__init__(name, itemType, sellPrice, tradable, discardable, questItem)
    
class Ingredients(Item):
    def __init__(self, name, itemType, sellPrice, tradable, discardable, questItem):
        super(Gear, self).__init__(name, itemType, sellPrice, tradable, discardable, questItem)
    
def pullItemData(url):
    #soup =  BeautifulSoup(urllib2.urlopen(url))
    soup = BeautifulSoup(open(url))

    #    monsterDiv = soup.find("div", { "id" : "mw-content-text" })
    
    type = soup.find(text=re.compile(r'Type: ')).next.getText()

    if (type == 'accessory'):
        pullAccessoryData(url)
    #elif (type == ""):
        #pass
    else:
        raise TypeError('Unknown item type: ' + type)

def pullAccessoryData(url):
    soup = BeautifulSoup(open(url))

    name = str(soup.title.getText().split(' - ')[0])

    description = soup.find('blockquote').next.strip()
    
    itemDiv = soup.find('div', { 'id' : 'mw-content-text' }).find('div')
    itemStrings = list(itemDiv.strings)
    #[string.strip() for string in itemStrings]

    requirement = None
    reqIndex = itemStrings.index(u' Required: ') if u' Required: ' in itemStrings else None
    if reqIndex == None:
        pass # non tradable etc
    else:
        requirement = itemStrings[reqIndex - 1] + itemStrings[reqIndex] + itemStrings[reqIndex + 1]

    tradable = False if (u'Cannot be traded' in itemStrings) or (u'Cannot be traded or discarded' in itemStrings) else True
    discardable = False if (u'Cannot be discarded' in itemStrings) or (u'Cannot be traded or discarded' in itemStrings) else True
    questItem = True if u'Quest Item' in itemStrings else False

    enchantment = itemDiv.find('span', { 'style' : 'color:blue;font-weight:bold' })
    if enchantment != None:
        enchantment = ', '.join(list(enchantment.strings))

    sellPrice = None
    priceIndex = itemStrings.index(u'Selling Price: ') if u'Selling Price: ' in itemStrings else None
    if priceIndex != None:
        sellPrice = itemStrings[priceIndex + 1]

#    print itemStrings

    print
    print name
    print description
    if (requirement != None):
        print requirement
    print "Discardable: " + str(discardable)
    print "Tradable: " + str(tradable)
    print "Quest Item: " + str(questItem)
    print "Enchantment: " + str(enchantment)
    print "Selling price: " + str(sellPrice)

def main():
    itemList = list()
    #monsterURLFile = open('monsterdataurls', 'r')
    #for line in monsterURLFile:
    #    monsterList.append(Monster(pullData(line))
    #monsterURLFile.close()

    for page in TEST_PAGES:
        pullItemData(page)

if __name__ == '__main__':
    main()



