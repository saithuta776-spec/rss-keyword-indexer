import sqlite3 
import re

conn = sqlite3.connect('Data.sqlite')
cur = conn.cursor()

keyword = input('What do you want to find? - ')

search_pattern = '%' + keyword + '%'
# search_pattern = f'%{keyword}%'

cur.execute('''SELECT source,title,link,description FROM Info WHERE title LIKE ? OR 
            description LIKE ?''',(search_pattern,search_pattern))
rows = cur.fetchall()
if len(rows) >= 1 :
    pattern = rf'\b{re.escape(keyword)}\b'

    for source,title,link,description in rows :
        if re.search(pattern,title.lower()) or re.search(pattern,description.lower()) :
            print()
            print(f'Source : {source}')
            print(f'Link : {link}')
            print(f'Title : {title}')
            print(f'Description : {description}')
            print('-'*20)
else :
    print(f"Article with keyword '{keyword}' : Not found ")