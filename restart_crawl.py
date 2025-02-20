import sqlite3

conn = sqlite3.connect('fighters.sqlite')
cur = conn.cursor()

all=input('del all? ')



if all=='y':
    hmm = input('are you sure you want to delete all tables? y/n')
    if hmm=='y':
        cur.execute('DROP TABLE IF EXISTS profesional_record_data')
        cur.execute('DROP TABLE IF EXISTS MMA_record')
        cur.execute('DROP TABLE IF EXISTS qu')
        cur.execute('DROP TABLE IF EXISTS visited_links')
        print('all tables in fighters.sqlite deleted')
    
if all=='n':
    profesional_record_data=input('del profesional_record_data? ')
    MMA_record=input('del MMA_record? ')
    qu=input('del qu? ')
    visited_links=input('del visited_links? ')

    if profesional_record_data=='y':
        hmm = input('are you sure you want to delete profesional_record_data? y/n')
        if hmm=='y':
            cur.execute('DROP TABLE IF EXISTS profesional_record_data')
            print('deleted profesional_record_data')
    if MMA_record=='y':
        hmm = input('are you sure you want to delete MMA_record? y/n')
        if hmm=='y':
            cur.execute('DROP TABLE IF EXISTS MMA_record')
            print('deleted MMA_record')
    if qu=='y':
        hmm = input('are you sure you want to delete qu? y/n')
        if hmm=='y':
            cur.execute('DROP TABLE IF EXISTS qu')
            print('deleted qu')
    if visited_links=='y':
        hmm = input('are you sure you want to delete visited_links? y/n')
        if hmm=='y':
            cur.execute('DROP TABLE IF EXISTS visited_links')
            print('deleted visited_links')

conn.commit()
cur.close()
