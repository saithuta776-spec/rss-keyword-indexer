import sqlite3
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re 


conn = sqlite3.connect('raw_xml.sqlite')
cur = conn.cursor()

conn1 = sqlite3.connect('Data.sqlite')
cur1 = conn1.cursor()

cur1.execute(''' DROP TABLE IF EXISTS Info''')
cur1.execute(''' CREATE TABLE IF NOT EXISTS Info 
             (id INTEGER PRIMARY KEY, xml_id INTEGER, source TEXT,time INTGER,link TEXT UNIQUE,
             title TEXT, description TEXT, publish_date TEXT, summary TEXT,
             category TEXT) ''')

def clean_html(raw) :
    soup = BeautifulSoup(raw,'html.parser').get_text(separator='').strip()
    return soup


cur.execute('''SELECT id,source,fetched_at,xml FROM XML_DATA''')
for row in cur :
    (xml_id,source,fetched_at,xml) = row
    fetched_at_slice = fetched_at[:20]

    root = ET.fromstring(xml)
    items = root.findall('.//item')

    if not items : 
        items = root.findall('{*}entry')
        is_atom = True
    
    else :
        is_atom = False
    
    for item in items :
        if is_atom :
            title = clean_html(item.findtext('{*}title'))
            link = item.find('{*}link').attrib.get('href')
            source = row[1]
            publish_date = item.findtext('{*}published')

            summary_raw = clean_html(item.findtext('{*}summary'))
            text = re.sub(r'\s*\[.*?]\s*$','',summary_raw)
            text_split = re.split(r'\.\s+',text)

            if len(text_split) >= 2 :
                summary = text_split[0]+'.'+text_split[1]+'.'

            else :
                summary = text_split[0]
                if not summary.endswith('.') :
                    summary = summary + '.'
            

            description_raw = item.findtext('{*}description')
            description = description_raw if description_raw else summary

            category_raw = item.findall('{*}category')
            cate_list = [cate.get('term') for cate in category_raw if not category_raw is None]
            category = ','.join(cate_list)

            

        else : 
            title_raw= item.findtext('title')
            title = title_raw.strip().replace('\n','') if title_raw is not None else ''
            link = item.findtext('link')
            publish_date = item.findtext('pubDate')

            description_raw = clean_html(item.findtext('description'))
            junk_pattern = r'Continue reading\.\.\.|Read more|\[\.\.\.\]'
            description = re.sub(junk_pattern,'',description_raw,flags=re.IGNORECASE).strip()

            category_raw = item.findall('category')
            cate_list = [cate.text for cate in category_raw if cate.text is not None ] 
            category = ','.join(cate_list) or 'General'
            # if not category : 
            #     category = 'General'

            source = row[1]
            summary_raw = item.findtext('summary')
            summary = summary_raw if summary_raw else description
        cur1.execute(''' INSERT OR IGNORE INTO Info 
                        (xml_id,source,time,link,title,description,publish_date,summary,category)
                        VALUES (?,?,?,?,?,?,?,?,?) ''',
                        (xml_id,source,fetched_at_slice,link,title,description,publish_date,summary,category))
                
        conn1.commit()
            
cur.close()
cur1.close()
        




























