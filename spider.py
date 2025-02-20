'''
to run this: python 3 spider.py x
where x is the number of MMA fighter web pages to visit
'''
import sqlite3
import requests
from bs4 import BeautifulSoup
import os
from main_table import tables
from main_table import links_qu
import sys


conn = sqlite3.connect('fighters.sqlite')
cur = conn.cursor()
try:
    amount = int(sys.argv[1])
except:
    print('input is: python3 spider.py number_of_web_pages')

seed_url = "https://en.wikipedia.org/wiki/Khabib_Nurmagomedov"

def create_tables(cur):

    cur.execute('''
    CREATE TABLE IF NOT EXISTS profesional_record_data (firstName TEXT, lastName TEXT, matches INT, wins INT, losses INT, 
                knockoutWins INT, knockoutLosses INT, submissionWins INT, submissionLosses INT, 
                decisionWins INT, decisionLosses INT)
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS MMA_record (firstName TEXT, lastName TEXT, result TEXT, record NUMERIC, opponent TEXT, method TEXT, event TEXT,
                date DATE, round INT, time NUMERIC, location TEXT, notes TEXT)
    ''')


    cur.execute(''' 
    CREATE TABLE IF NOT EXISTS visited_links (firstName STR,lastName STR, href STR, html STR)
    ''')

    cur.execute(''' 
    CREATE TABLE IF NOT EXISTS qu (firstName STR,lastName STR, links STR, href STR,
                fromFirstName STR, fromLastName STR, html STR, rowid INT)
    ''')

def check_start_crawl(cur, seed_url):
    cur.execute('''
    SELECT links FROM qu
    ''')

    links = cur.fetchone()

    if links is None:  # crawl has not started
        url = seed_url
        html = requests.get(url).text

        fighter_name, prof_rec_table, main_rec_table = tables(html)

        qu = links_qu(main_rec_table)

        qu_str = ''
        for e in qu:
            qu_str = qu_str + e + ' '

        first_name = fighter_name.split()[0]
        last_name = fighter_name.split()[1]
        cur.execute('''
        INSERT INTO qu (firstName, lastName, links, href, fromFirstName, fromLastName, html, rowid) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
            ''',(first_name, last_name, qu_str, url,'seed','seed',html, 1))

        
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

def BFS(amount):
    qu_items=0
    while qu_items<amount:
        cur.execute('''
        SELECT firstName, lastName, html, href FROM qu
        ''')

        first_fighter = cur.fetchall()
        first_fighter_first_name = first_fighter[0][0]
        first_fighter_second_name = first_fighter[0][1]
        first_fighter_html = first_fighter[0][2]
        first_fighter_url = first_fighter[0][3]
        #print(first_fighter_first_name,first_fighter_second_name)
        cur.execute('''
        SELECT links FROM qu
        ''')
        links = cur.fetchone()
        links = links[0].split()  
        
        #print(f'looping through links obtained from {first_fighter_first_name, first_fighter_second_name}')  

        rowid = None
        for link in links:
            cur.execute('''
            SELECT href FROM visited_links WHERE href=?
            ''',(link,))
            all_hrefs = cur.fetchall()

            cur.execute('''
            SELECT href FROM qu WHERE href=?
            ''',(link,))

            all_hrefs_qu = len(cur.fetchall())

            # print(f'testing match {all_hrefs[0], link}')
            # print(all_hrefs)
            if len(all_hrefs)>0: 
                print(f'this link has been visited {link} from {first_fighter_first_name}')
                continue
            if all_hrefs_qu>0:
                print(f'this link is alrdy in qu {link} from {first_fighter_first_name}')
                continue

            html = requests.get(link).text
            fighter_name, prof_rec_table, main_rec_table = tables(html)
            #print(f'currently GETTING ALL LINKS FROM {fighter_name}\n')
            qu = links_qu(main_rec_table)
            #print(qu)

            qu_str = ''
            for e in qu:
                if (e,) in all_hrefs: 
                    print(f'this link was skipped {e} from {fighter_name.split()[0]}')
                    continue
                qu_str = qu_str + e + ' '

            first_name = fighter_name.split()[0]
            last_name = fighter_name.split()[1]

            cur.execute('''
            SELECT firstName, lastName, rowid FROM qu WHERE (firstName, lastName)=(?,?)
            ''',(first_name,last_name))
            alrdy_in_qu=cur.fetchall()
            if len(alrdy_in_qu)>0:
                print(f'{alrdy_in_qu} occurences of {first_name} already in qu. intial skip failed. deleting from qu')
                cur.execute('''
                DELETE FROM qu WHERE rowid = ?
                ''',(alrdy_in_qu[0][2],))
                conn.commit()

                

            cur.execute('''
            SELECT rowid FROM qu ORDER BY rowid 
                ''')
            
            rowid = cur.fetchall()[-1][0]+1
            #print(f'rowid to add :{rowid}')

            cur.execute('''
            INSERT INTO qu (firstName, lastName, links, href, fromFirstName, fromLastName, html, rowid) VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
                ''',(first_name, last_name, qu_str, link, first_fighter_first_name, first_fighter_second_name, html, rowid))
            
            conn.commit()
            #print(f'adding to end of qu {first_name, last_name} at row id: {rowid}\n')
            #print(f'adding to visited links {first_name, last_name} \n')
        
        conn.commit()
        # print(f'all links for {first_fighter_first_name} gone through')
        # print(f'deleting {first_fighter_first_name} from qu')
        # print(f'adding {first_fighter_first_name} to visited links')
        cur.execute('''
        INSERT INTO visited_links (firstName, lastName, href, html) VALUES (?, ?, ?, ?) 
            ''',(first_fighter_first_name, first_fighter_second_name, first_fighter_url, 
                first_fighter_html))

        cur.execute('''
            SELECT rowid FROM qu ORDER BY rowid 
                ''')
        first_fighter_rowid = cur.fetchall()[0][0]

        cur.execute('DELETE FROM qu WHERE rowid=?',(first_fighter_rowid,))

        conn.commit()

        # cur.execute('SELECT * FROM qu')
        # qu_end_iter =cur.fetchall()
        #print(f'first two values in qu at end of iteration {qu_end_iter[0], qu_end_iter[1]} \n')

        # cur.execute('SELECT firstName, lastName FROM visited_links')
        # visi_end_iter = cur.fetchall()
        #print(f'last  value of visited set at end of iteration {visi_end_iter[-1]} \n')
        
        qu_items+=1

create_tables(cur)
check_start_crawl(cur, seed_url)
BFS(amount)

cur.close()
