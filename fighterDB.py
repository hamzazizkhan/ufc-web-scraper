import sqlite3

conn = sqlite3.connect('fighters.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS data
''')

cur.execute('''
CREATE TABLE data (firstName TEXT, lastName TEXT, matches INT, wins INT, losses INT, 
            knockoutWins INT, knockoutLosses INT, submissionWins INT, submissionLosses INT, 
            decisionWins INT, decisionLosses INT)
''')
fighters_data = open('fighters.txt', 'r')
fighters_list = fighters_data.readlines()

line_count = 0
for row in fighters_list:
        col = row.split()
        print(col)

        cur.execute('''INSERT INTO data (firstName, lastName, matches, wins, losses, 
            knockoutWins, knockoutLosses, submissionWins, submissionLosses, 
            decisionWins, decisionLosses) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (col[1],col[3],col[5],col[7],col[9],col[11], col[13], 
             col[15], col[17], col[19], col[21]) )
        conn.commit()
        
cur.close()

