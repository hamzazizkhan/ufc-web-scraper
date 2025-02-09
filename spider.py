import sqlite3
import requests
from bs4 import BeautifulSoup
import os
from main_table import tables
from main_table import links_qu

def validate():
    cur.execute('''
    SELECT * FROM qu
    ''')
    print('current qu:')
    hmmm = cur.fetchall()
    print(hmmm[0][2])
    print('\nqu obtained from:')
    print(hmmm[0][0])


    # cur.execute('''
    #     SELECT firstName, lastName, href FROM visited_links
    # ''')
    # print('\nvisited:')
    # print(cur.fetchall()[-1])
    # print('============================= \n')

conn = sqlite3.connect('fighters.sqlite')
cur = conn.cursor()

cur.execute(''' 
CREATE TABLE IF NOT EXISTS visited_links (firstName STR,lastName STR, href STR, html STR)
''')

cur.execute(''' 
CREATE TABLE IF NOT EXISTS qu (firstName STR,lastName STR, links STR, href STR,
            fromFirstName STR, fromLastName STR, rowid INT)
''')

cur.execute('''
SELECT links FROM qu
''')

links = cur.fetchone()

if links is None:  # crawl has not started
    url = "https://en.wikipedia.org/wiki/Khabib_Nurmagomedov"
    html = requests.get(url).text

    fighter_name, prof_rec_table, main_rec_table, html_content = tables(html)

    qu = links_qu(main_rec_table)

    qu_str = ''
    for e in qu:
        qu_str = qu_str + e + ' '

    first_name = fighter_name.split()[0]
    last_name = fighter_name.split()[1]
    cur.execute('''
    INSERT INTO qu (firstName, lastName, links, href, fromFirstName, fromLastName, rowid) 
                VALUES (?, ?, ?, ?, ?, ?, ?) 
        ''',(first_name, last_name, qu_str, url,'seed','seed', 1))

    
    conn.commit()
else:
    cur.execute('''
    SELECT firstName, lastName FROM qu 
    ''')
    names = cur.fetchone()
    first = names[0]
    last = names[1]

    cur.execute('''
    DELETE FROM qu WHERE (fromFirstName, fromLastName) = (?,?)
    ''', (first,last))

qu_items=0
while qu_items<6:
    cur.execute('''
    SELECT firstName, lastName, href FROM qu
    ''')

    first_fighter = cur.fetchall()
    first_fighter_first_name = first_fighter[0][0]
    first_fighter_second_name = first_fighter[0][1]
    first_fighter_url = first_fighter[0][2]
    print(first_fighter_first_name,first_fighter_second_name)
    cur.execute('''
    SELECT links FROM qu
    ''')
    links = cur.fetchone()
    links = links[0].split()  
    
    print(f'looping through links obtained from {first_fighter_first_name, first_fighter_second_name}')  

    rowid = None
    for link in links:
        cur.execute('''
        SELECT href FROM visited_links
        ''')
        all_hrefs = cur.fetchall()

        # print(f'testing match {all_hrefs[0], link}')
        # print(all_hrefs)
        if (link,) in all_hrefs: continue

        html = requests.get(link).text
        fighter_name, prof_rec_table, main_rec_table, html_content = tables(html)
        print(f'currently GETTING ALL LINKS FROM {fighter_name}\n')
        qu = links_qu(main_rec_table)

        qu_str = ''
        for e in qu:
            qu_str = qu_str + e + ' '

        first_name = fighter_name.split()[0]
        last_name = fighter_name.split()[1]
        cur.execute('''
        SELECT rowid FROM qu ORDER BY rowid 
            ''')
        
        rowid = cur.fetchall()[-1][0]+1
        #print(f'rowid to add :{rowid}')

        cur.execute('''
        INSERT INTO qu (firstName, lastName, links, href, fromFirstName, fromLastName, rowid) VALUES (?, ?, ?, ?, ?, ?, ?) 
            ''',(first_name, last_name, qu_str, link, first_fighter_first_name, first_fighter_second_name, rowid))
        
        conn.commit()
        print(f'adding to end of qu {first_name, last_name} at row id: {rowid}\n')
        #print(f'adding to visited links {first_name, last_name} \n')
    
    conn.commit()
    print(f'all links for {first_fighter_first_name} gone through')
    print(f'deleting {first_fighter_first_name} from qu')
    print(f'adding {first_fighter_first_name} to visited links')
    cur.execute('''
    INSERT INTO visited_links (firstName, lastName, href, html) VALUES (?, ?, ?, ?) 
        ''',(first_fighter_first_name, first_fighter_second_name, first_fighter_url, 
             requests.get(first_fighter_url).text))

    cur.execute('''
        SELECT rowid FROM qu ORDER BY rowid 
            ''')
    first_fighter_rowid = cur.fetchall()[0][0]

    cur.execute('DELETE FROM qu WHERE rowid=?',(first_fighter_rowid,))

    conn.commit()

    cur.execute('SELECT * FROM qu')
    qu_end_iter =cur.fetchall()
    print(f'first two values in qu at end of iteration {qu_end_iter[0], qu_end_iter[1]} \n')

    cur.execute('SELECT firstName, lastName FROM visited_links')
    visi_end_iter = cur.fetchall()
    print(f'last  value of visited set at end of iteration {visi_end_iter[-1]} \n')
    
    qu_items+=1


validate()
cur.close()
