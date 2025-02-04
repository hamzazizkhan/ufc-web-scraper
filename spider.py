import sqlite3
import requests
from bs4 import BeautifulSoup
import os

conn = sqlite3.connect('fighters.sqlite')
cur = conn.cursor()

cur.execute(''' 
CREATE TABLE IF NOT EXISTS visited_links (firstName STR,lastName STR, href STR, html STR)
''')

cur.execute(''' 
CREATE TABLE IF NOT EXISTS qu (firstName STR,lastName STR, links STR)
''')

cur.execute('''
SELECT links FROM qu
''')
links = cur.fetchone()
print(links)

if links is None:  # crawl has not started
    url = "https://en.wikipedia.org/wiki/Khabib_Nurmagomedov"
    html_content=requests.get(url).text
    #print(html_content)
    soup = BeautifulSoup(html_content, "html.parser")

    fighter_name = soup.find('h1').get_text()
    heading_two = soup.find_all('h2')

    prof_rec_table = None
    main_rec_table = None

    for heading in heading_two:
        # Mixed martial arts record section
        if 'id' in heading.attrs:
            if heading['id']=='Mixed_martial_arts_record':
                #print('found Mixed martial arts record section')
                #print(heading)

                # Professional record breakdown table
                prof_rec_table = heading.string.next_element.next_element
                #print('found Professional record breakdown table')

                for ele in prof_rec_table.next_elements:
                    if ele.name == 'table':
                        main_rec_table = ele
                        #print('found main rec table \n')
                        #print(main_rec_table.prettify)
                        break
                #print('=================')

                break

    #print('\n')
    #print('=================')

    rows = main_rec_table.find_all('tr')

    qu = []
    i=0
    for row in rows:
        if i ==0:
            i=1
            continue
        #print(row)
        td = row.find_all('td')
        #print('=================')
        #print('fighters link!')
        opponent = td[2]
        a_tag = opponent.a
        if a_tag is not None:
            href = a_tag['href']
            link = 'https://en.wikipedia.org'+href
            if link not in qu:
                qu.append(link)
        #print('=================')

    qu_str = ''
    for e in qu:
        qu_str = qu_str + e + ' '

    first_name = fighter_name.split()[0]
    last_name = fighter_name.split()[1]
    cur.execute('''
    INSERT INTO qu (firstName, lastName, links) VALUES (?, ?, ?) 
        ''',(first_name, last_name, qu_str))
    
    cur.execute('''
    INSERT INTO visited_links (firstName, lastName, href, html) VALUES (?, ?, ?, ?) 
        ''',(first_name, last_name, url, html_content))
    
    conn.commit()

    #print(qu)
    

cur.close()
