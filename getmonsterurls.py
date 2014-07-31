from bs4 import BeautifulSoup
import urllib2

MONSTERURLS=[
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(1_to_E)",
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(F_to_M)",
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(N_to_S)",
"http://kol.coldfront.net/thekolwiki/index.php/Monster_Compendium_(T_to_Z)"
]

def getLists():
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

def main():
    url_file = open('monsterurls', 'w')
    dataurl_file = open('monsterdataurls', 'w')
    monsterLists = getLists()
    writeMonsterURLs(monsterLists, url_file, dataurl_file)
    url_file.close()
    dataurl_file.close()
    print("Done")

if __name__ == '__main__':
    main()


