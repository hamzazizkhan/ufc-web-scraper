import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Khabib_Nurmagomedov"
html_content=requests.get(url).text
#print(html_content)
soup = BeautifulSoup(html_content, "html.parser")
heading_two = soup.find_all('h2')

prof_rec_table = None
for heading in heading_two:
    # Mixed martial arts record section
    if 'id' in heading.attrs:
        if heading['id']=='Mixed_martial_arts_record':
            print('found Mixed martial arts record section')
            print(heading)

            # Professional record breakdown table
            prof_rec_table = heading.string.next_element.next_element
            print('found Professional record breakdown table')
            print(prof_rec_table)
            break

prof_rec_data = {}
prof_rec_list = prof_rec_table.tbody.get_text().split()

for i in range(len(prof_rec_list)):
    if i%2==0 and i<6:
        prof_rec_data[prof_rec_list[i+1]] = int(prof_rec_list[i])
    if prof_rec_list[i]=='By':
        prof_rec_data[prof_rec_list[i+1]+ ' Wins'] =  int(prof_rec_list[i+2])
        prof_rec_data[prof_rec_list[i+1]+ ' Losses'] =  int(prof_rec_list[i+3])
print('\n')
print(prof_rec_data)
        