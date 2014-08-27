#------------------------------------------------------------------------------
#
#Writes output files containing the URLs of all monsters and items from input
#
#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup
import urllib2

#Output Files
ITEMURLFILE = "itemurls.txt"
MONSTERURLFILE = "monsterurls.txt"
MONSTERDATAURLFILE = "monsterdataurls.txt"

#Input
MONSTERURLS=[
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(1_to_E)",
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(F_to_M)",
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(N_to_S)",
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(T_to_Z)"]
ITEMSTARTURL = \
"http://kol.coldfront.net/thekolwiki/index.php/Items_by_number_(negative)"
ITEMURL2 = \
"http://kol.coldfront.net/thekolwiki/index.php/Items_by_number_(1-99)"
REGULARITEMURL = \
"http://kol.coldfront.net/thekolwiki/index.php/Items_by_number_(100-199)"
BASEITEMURL = \
"http://kol.coldfront.net/thekolwiki/index.php/Items_by_number_("
MAXITEMPAGES = 79 #79

#-------------------------------------------------------------------------------
#
#                               MONSTER URLS
#
#-------------------------------------------------------------------------------
def getMonsterURLs():
    url_file = open(MONSTERURLFILE, 'w')
    dataurl_file = open(MONSTERDATAURLFILE, 'w')
    monsterPages = getMonsterPages()
    writeMonsterURLs(monsterPages, url_file, dataurl_file)
    url_file.close()
    dataurl_file.close()

def getMonsterPages():
    pages = list()
    for aPage in MONSTERURLS:
        pages.append(urllib2.urlopen(aPage)) #creates a list of html objects
    return pages

def writeMonsterURLs(pages,url_file,dataurl_file):
    for aPage in pages:
        soup = BeautifulSoup(aPage)
        table = soup.find_all('table')[2]
        tds = table.find_all('td', {'align':'center'})
        for i in range(1, len(tds) - 1):
            url = "http://kol.coldfront.net" + (tds[i].next.get('href') + '\n')
            url_file.write(url)
            dataurl_file.write(url[:46] + 'Data:' + url[46:])
#-------------------------------------------------------------------------------
#
#                                 ITEM URLS
#
#-------------------------------------------------------------------------------
def getItemURLs():
    url_file = open(ITEMURLFILE, 'w')
    itemPages = getItemPages()
    writeItemURLs(itemPages, url_file)
    url_file.close()

def getItemPages():
    pages = list()
    currentURL =ITEMSTARTURL
    for i in range(0, MAXITEMPAGES):
        print (currentURL)
        pages.append(urllib2.urlopen(currentURL))
        currentURL = getNextURL(currentURL)
    return pages

def getNextURL(inputURL):
    if inputURL == ITEMSTARTURL:
        return ITEMURL2
    elif inputURL == ITEMURL2:
        return REGULARITEMURL
    else:
        pageNumbers = ((inputURL.rsplit("(")[1]).split(")")[0]).split('-')
        pageNumbers = map(lambda x: str(int(x)+100), pageNumbers)
        return (BASEITEMURL + pageNumbers[0] + "-" + pageNumbers[1]) + ")"

def writeItemURLs(pages, url_file):
    for aPage in pages:
        soup = BeautifulSoup(aPage)
        itemDiv = soup.find("div", { "class" : "mw-content-ltr" })
        itemTable = itemDiv.find("table")
        for link in itemTable.find_all('a'):
            url = "http://kol.coldfront.net" + link.get('href') + '\n'
            url_file.write(url)
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def main():
    getMonsterURLs()
    getItemURLs()

if __name__ == '__main__':
    main()


