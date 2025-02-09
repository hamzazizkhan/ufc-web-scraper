import sqlite3

conn = sqlite3.connect('fighters.sqlite')
cur = conn.cursor()

profesional_record_data=False
MMA_record=False
qu=False
visited_links=False
all=False

if all:
    cur.execute('DROP TABLE IF EXISTS profesional_record_data')
    cur.execute('DROP TABLE IF EXISTS MMA_record')
    cur.execute('DROP TABLE IF EXISTS qu')
    cur.execute('DROP TABLE IF EXISTS visited_links')
if profesional_record_data:
    cur.execute('DROP TABLE IF EXISTS profesional_record_data')
if MMA_record:
    cur.execute('DROP TABLE IF EXISTS MMA_record')
if qu:
    cur.execute('DROP TABLE IF EXISTS qu')
if visited_links:
    cur.execute('DROP TABLE IF EXISTS visited_links')

conn.commit()