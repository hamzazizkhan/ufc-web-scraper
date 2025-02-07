import sqlite3
import requests
from bs4 import BeautifulSoup
import os

# returns prof rec table and main table
def tables(link):
    html_content=requests.get(link).text
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
                print('found Mixed martial arts record section')
                # print(heading)

                # Professional record breakdown table
                for ele in heading.next_elements:
                    if ele.name == 'table':
                        prof_rec_table = ele
                        print('found Professional record breakdown table \n')
                        # print(prof_rec_table.prettify)
                        break

                # MMA record table
                for ele in prof_rec_table.next_elements:
                    if ele.name == 'table':
                        main_rec_table = ele
                        print('found main rec table \n')
                        # print(main_rec_table.prettify)
                        break
                #print('=================')
                break
    return(fighter_name, prof_rec_table, main_rec_table)



url = "https://en.wikipedia.org/wiki/Khabib_Nurmagomedov"


fighter_name, prof_rec_table, main_rec_table = tables(url)

print('\n')
print('=================')

if(os.path.exists('main_table.txt')): os.remove('main_table.txt')
file = open('main_table.txt', 'a')
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

    print(rowspan)

    print('=================')
    

    for word in text:
        file.write(word + '// ')

    print('=================')


file.close()