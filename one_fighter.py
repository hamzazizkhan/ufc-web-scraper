import requests
from bs4 import BeautifulSoup
import os
from main_table import tables

url = "https://en.wikipedia.org/wiki/Khabib_Nurmagomedov"
fighter_name, prof_rec_table, main_rec_table = tables(url)


prof_rec_data = {}
prof_rec_list = prof_rec_table.tbody.get_text().split()

for i in range(len(prof_rec_list)):
    if i%2==0 and i<6:
        prof_rec_data[prof_rec_list[i+1]] = prof_rec_list[i]
    if prof_rec_list[i]=='By':
        prof_rec_data[prof_rec_list[i+1]+ 'Wins'] =  prof_rec_list[i+2]
        prof_rec_data[prof_rec_list[i+1]+ 'Losses'] =  prof_rec_list[i+3]
print('\n')
print(prof_rec_data)

# writing to text file
if(os.path.exists('fighters.txt')): os.remove('fighters.txt')

fighters = open('fighters.txt','a')
fighters.write('firstName '+fighter_name.split()[0] + ' ')
fighters.write('lastName '+fighter_name.split()[-1] + ' ')

for k,v in prof_rec_data.items():
    text = k + ' '+v + ' '
    fighters.write(text)
fighters.close()