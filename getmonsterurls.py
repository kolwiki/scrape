from bs4 import BeautifulSoup

pages = ['compendium1.html', 'compendium2.html', 'compendium3.html', 'compendium4.html']

url_file = open('monsterurls', 'w')
dataurl_file = open('monsterdataurls', 'w')

for page in pages:

    soup = BeautifulSoup(open(page)) # a soup
    
    table = soup.find_all('table')[2] # tag
    
    tds = table.find_all('td', {'align':'center'}) # a result set (group of tags)
    
    for i in range(1, len(tds) - 1):
        url = (tds[i].next.get('href') + '\n')
        url_file.write(url)
        dataurl_file.write(url[:46] + 'Data:' + url[46:])

url_file.close()
dataurl_file.close()
