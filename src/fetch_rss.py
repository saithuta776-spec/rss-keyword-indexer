from urllib.request import urlopen
import ssl 
import urllib.request
from datetime import datetime
from urllib.parse import urlparse
import sqlite3

conn = sqlite3.connect('raw_xml.sqlite')
cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS XML_DATA 
            (id INTEGER PRIMARY KEY, source TEXT, fetched_at TEXT,
            xml BLOB)''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rss = [

'https://www.nasa.gov/news-release/feed/',                      # NASA (Space/Science)
'https://www.aljazeera.com/xml/rss/all.xml',                    # Al Jazeera (Global News)
'https://www.economist.com/finance-and-economics/rss.xml',      # The Economist (Finance)
'https://www.sciencedaily.com/rss/all.xml',                     # Science Magazine (Science)
'https://www.theguardian.com/world/rss'  ,                      # The Guardian (World News)
'http://feeds.bbci.co.uk/news/world/rss.xml',                   # BBC
'https://techcrunch.com/feed/',                                 # Techcrunch 
'https://www.theverge.com/rss/index.xml',                       # Theverge
'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',    # New York Times
'https://feeds.arstechnica.com/arstechnica/index'               # Arstechnica
]

SOURCE_MAP = {
    'Nasa' : 'NASA' ,
    'Aljazeera' : 'Al Jazeera', 
    'Economist' : 'The Economist',
    'Sciencedaily' : 'ScienceDaily',
    'Theguardian'  : 'The Guardian',
    'Bbci' : 'BBC' ,
    'Theverge' : 'The Verge' ,
    'Nytimes' : 'The New York Times',
    'Arstechnica' : 'Ars Technica'
}

def get_source_url(url) : 
    
    domain = urlparse(url).netloc
    domain_split = domain.split('.')
    prefix_removes = {'www','feeds','rss'}
    if domain_split[0] in prefix_removes :
        domain = domain_split[1]
    else :
        domain = domain_split[0]
    
    domain = domain.capitalize()
    source = SOURCE_MAP.get(domain,domain)
    return source


for url in rss :
    print(f'RSS that you retrieved : {url}')
    source = get_source_url(url)
    print(f'{source}')
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*'
    }
    
    req = urllib.request.Request(url, headers=headers)

    try :
        connection = urlopen(req,timeout=30,context=ctx)
        data = connection.read().decode()
        # print(f'{data[:100]}\n')
        fetched_at = datetime.now()
        fetched_at_iso = fetched_at.isoformat(timespec='seconds')
        print(f'{fetched_at_iso}\n')

    except Exception as e :
        print(f'Error - Failed to retrieved RSS : {e}\n')

    cur.execute('''INSERT OR IGNORE INTO XML_DATA 
                (source,fetched_at,xml) VALUES (?,?,?)''',(source,fetched_at_iso,data))
    conn.commit()
cur.close()