import sqlite3
import re
from collections import Counter, defaultdict
from dateutil import parser
from datetime import datetime

conn = sqlite3.connect('Data.sqlite')
cur = conn.cursor()



def tokenize(text) :
    info = re.sub(r'<.*?>','',text)
    info = info.lower().strip()
    info = re.sub(r'[^\w\s]','',info)
    info = info.split()
    return info

keywords = {'trump','china','president','stockmarkets','trade','war','americans','companies','americas','sanctions','music',
            'democrats','scientists','billion','ocean','stanford','ecosystems','cancer','quantum','billions','mars',
            'christmas','suparcharging','uk','chinas','iran','nuclear','republican','democracy','military','myanmar',
            'business','korea','thailand','us','japan','electricity','israel','artificial','gaza','migrants','apple'}

keywords_count = {
    'NASA' : Counter() ,
    'Al Jazeera' : Counter(), 
    'The Economist' : Counter(),
    'ScienceDaily' : Counter(),
    'The Guardian' : Counter(),
    'BBC' : Counter(),
    'Techcrunch' : Counter(),
    'The Verge' : Counter(),
    'The New York Times' : Counter(),
    'Ars Technica' : Counter()
}

all_words = defaultdict(list)

stopped_words = {'eat','your','out','to','how','the','over','under','a','an','am','i','is','are','were','will',
                 'they','them','under','in','might','as','be','from','for','those','these','of','on','above','its','it',
                 'he','she','or','with','up','all','can','and','the','that','at','down','due','until','how','off',
                 'far','than','itself','after','not','back','which','when','who','where','has','have','very','us','if',
                 'around','any','along','by','did','been','still','from'}

longest_title = ('',0)
longest_description = ('',0)

article_per_day = Counter()

cur.execute('''SELECT source,title,description,publish_date FROM Info''')
for row in cur :
    (source,title,description,publish_date) = row

    title_word = tokenize(title)
    description_word = tokenize(description)
    # print(title_word)
    # print(description_word)

    matching_keys = [word for word in title if word in keywords]
    if matching_keys :
        print(f'--- {source} Match Found ---')
        print(f"Title: {title}")
        print(f"Detected Keywords: {matching_keys}")
        print("-" * 20)

    for key in title_word + description_word :
        if not key in stopped_words :
            if key in keywords :
                keywords_count[source][key] += 1
            if key.isalpha() :
                all_words[source].append(key)

    if title and len(title) > longest_title[1] :
        longest_title = (title,len(title))
        
    
    if description and len(description) > longest_description[1] :
        longest_description = (description,len(description))
    
    if publish_date :
        try :

            # date = datetime.strptime(publish_date[:25],'%a, %d %b %Y %H:%M:%S').date()
            date = parser.parse(publish_date[:25]).date()
            article_per_day[date] += 1

        except :
            pass

print(f'Longest Title : {longest_title}')
print(f'Longest Description : {longest_description}')

print(f'\nArticle Per Day\n')
for word, count in article_per_day.items():
    print(word,count)

print(f'\nKeyword Counts : \n')
for i in keywords_count :
    print(i,dict(keywords_count[i]))
print()