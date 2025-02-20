import requests
from bs4 import BeautifulSoup
import os
from main_table import tables
import sqlite3

# conn = sqlite3.connect('fighters.sqlite')
# cur = conn.cursor()


def check_tables_update(cur):
    cur.execute('SELECT * FROM profesional_record_data')
    have = len(cur.fetchall())

    cur.execute('SELECT * FROM visited_links')
    all = len(cur.fetchall())

    diff = all-have
    print(f'number of fighters in visited links {all} - fighters in profesional_record_data {have} = {diff} \n missing {diff} entries' )

    start_row = all-diff
    print(f'write to text from row {start_row} in visited links')
    return(diff,start_row)

def write_to_txt(diff, start_row, cur):
    fighters = open('fighters.txt','w')
    file = open('main_table.txt', 'w')


    if diff==0:
        start=False
        return
    else:
        start=True

    cur.execute('SELECT firstName, lastName, html FROM visited_links')
    data = cur.fetchall()
    if start:
        for row_index in range(start_row,len(data)):
            #print(row[0])
            html = data[row_index][2]
            fighter_name, prof_rec_table, main_rec_table = tables(html)
            #print(fighter_name, row_index)

            prof_rec_data = {}
            prof_rec_list = prof_rec_table.tbody.get_text().split()

            for i in range(len(prof_rec_list)):
                if i%2==0 and i<6:
                    prof_rec_data[prof_rec_list[i+1]] = prof_rec_list[i]
                if prof_rec_list[i]=='By':
                    prof_rec_data[prof_rec_list[i+1]+ 'Wins'] =  prof_rec_list[i+2]
                    prof_rec_data[prof_rec_list[i+1]+ 'Losses'] =  prof_rec_list[i+3]
            # print('\n')
            # print(prof_rec_data)

            # writing to text file
            
            fighters.write('firstName '+fighter_name.split()[0] + ' ')
            fighters.write('lastName '+fighter_name.split()[1] + ' ')

            for k,v in prof_rec_data.items():
                text = k + ' '+v + ' '
                fighters.write(text)
            fighters.write('\n')

            ################################ main table

            # print('\n')
            # print('=================')

            
            file.write(fighter_name.split()[0] + ' ' + fighter_name.split()[1]+ '// ')

            rows = main_rec_table.find_all('tr')
            qu = []
            i=0
            rowspan = []
            inserts=0
            for row in rows:
                if i ==0:
                    i=1
                    continue
                #print(row)
                td = row.find_all('td')
                text = [td_tag.text.strip() for td_tag in td]
                
                
                if len(rowspan)!=0:
                    for ele in rowspan:
                        text_insert = ele[0]
                        index_insert = ele[1]
                        
                        text.insert(index_insert, text_insert)
                    if inserts==1:
                        rowspan=[]
                        inserts=0
                    else:
                        inserts-=1

                else:
                    #rowspan = [(int(td_tag['rowspan'])-1, td_tag.text.strip(), i) for i, td_tag in enumerate(td) if 'rowspan' in td_tag.attrs]
                    for i, td_tag in enumerate(td):
                        if 'rowspan' in td_tag.attrs:
                            rowspan.append((td_tag.text.strip(), i))
                            inserts = int(td_tag['rowspan'])-1
                if len(text)<10:
                    diff = 10-len(text)
                    for _ in range(diff):
                        text.append('Null')


                #print(rowspan)

                #print('=================')
                

                for word in text:
                    file.write(word + '// ')

                #print('=================')
            file.write('\n')


        file.close()
        fighters.close()

    print('program started?', start)

# if __name__=="__one_fighter__":
#     pass

# diff, start_row = check_tables_update()
# write_to_txt(diff,start_row)