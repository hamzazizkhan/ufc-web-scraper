import sqlite3
from one_fighter import check_tables_update

# conn = sqlite3.connect('fighters.sqlite')
# cur = conn.cursor()

########################### prof record
def add_to_prof_rec(cur):
    print('adding to profesional_record_data from fighters.txt')
    fighters_data = open('fighters.txt', 'r')
    fighters_list = fighters_data.readlines()

    line_count = 0
    for row in fighters_list:
            col = row.split()
            #print(col)
            
            cur.execute('''INSERT INTO profesional_record_data (firstName, lastName, matches, wins, losses, 
                knockoutWins, knockoutLosses, submissionWins, submissionLosses, 
                decisionWins, decisionLosses) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                (col[1],col[3],col[5],col[7],col[9],col[11], col[13], 
                col[15], col[17], col[19], col[21]) )
            #conn.commit()
    fighters_data.close()

        
########################### main table

def add_to_main_table(cur):
    print('adding to MMA_record from main_table.txt')
    main_table = open('main_table.txt','r').readlines()

    for fighter_line in main_table:
        elements = fighter_line.split('// ')
        #print(len(elements))
        fighter_first_name = elements[0].split()[0]
        fighter_last_name = elements[0].split()[1]

        for i in range(1,len(elements)-1,10):
            #print(i)
            result = elements[i]
            record = elements[i+1]
            opponent = elements[i+2]
            method = elements[i+3]
            event = elements[i+4]
            date = elements[i+5]
            round = elements[i+6]
            time = elements[i+7]
            location = elements[i+8]
            notes = elements[i+9]
            #print((result, record, opponent, method, event,
            #date, round, time, location, notes))
            cur.execute('''
                        INSERT INTO MMA_record (firstName, lastName, result, record, opponent, method, event,
            date, round, time, location, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                        ''',(fighter_first_name, fighter_last_name, result, record, opponent, method, event,
            date, round, time, location, notes))

            #conn.commit()


# diff, start_row = check_tables_update()

# if diff!=0:
#     add_to_prof_rec()
#     add_to_main_table()
# else:
#     print('tables up to date!')


# cur.close() 

