import sqlite3

conn = sqlite3.connect('fighters.sqlite')
cur = conn.cursor()

profesional_record_data=False
MMA_record=False
qu=False
visited_links=False
all=True

if all:
    hmm = input('are you sure you want to delete all tables? y/n')
    if hmm=='y':
        cur.execute('DROP TABLE IF EXISTS profesional_record_data')
        cur.execute('DROP TABLE IF EXISTS MMA_record')
        cur.execute('DROP TABLE IF EXISTS qu')
        cur.execute('DROP TABLE IF EXISTS visited_links')
        print('all tables in fighters.sqlite deleted')
    
    
if profesional_record_data:
    hmm = input('are you sure you want to delete profesional_record_data? y/n')
    if hmm=='y':
        cur.execute('DROP TABLE IF EXISTS profesional_record_data')
        print('deleted profesional_record_data')
if MMA_record:
    hmm = input('are you sure you want to delete MMA_record? y/n')
    if hmm=='y':
        cur.execute('DROP TABLE IF EXISTS MMA_record')
        print('deleted MMA_record')
if qu:
    hmm = input('are you sure you want to delete qu? y/n')
    if hmm=='y':
        cur.execute('DROP TABLE IF EXISTS qu')
        print('deleted qu')
if visited_links:
    hmm = input('are you sure you want to delete visited_links? y/n')
    if hmm=='y':
        cur.execute('DROP TABLE IF EXISTS visited_links')
        print('deleted visited_links')

conn.commit()
cur.close()
