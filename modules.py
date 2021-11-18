import pandas as pd
import gzip
import shutil
import requests
import ssl
import xml.sax
import ssl
import numpy as np
from sqlalchemy import create_engine


def download_abstract(url, path_out):
    ssl._create_default_https_context = ssl._create_unverified_context
    data = requests.get(url, stream=True)
    with open(path_out, 'wb') as f_out:
        shutil.copyfileobj(data.raw, f_out)


def unzip_gzip(path_in,path_out):
    with gzip.open(path_in, 'rb') as f_in:
        with open(path_out, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._content = {} # Dictionary where the movie name is key and url and abstract are values

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'url', 'abstract'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'doc':
            self._content[self._values['title'].strip('Wikipedia: ')] = [self._values['url'], self._values['abstract']]


def process_movies(path, cols_to_keep):
    df=pd.read_csv(path)
    df['budget']=df['budget'].apply(pd.to_numeric, errors='coerce')
    df = df[(df['budget'] != 0.0)]
    df['ratio']=df['revenue']/df['budget']
    df = df.drop([col for col in df.columns if col not in cols_to_keep], axis=1)
    df = df.sort_values('ratio',ascending = False).head(1000).reset_index(drop=True)
    return df

def process_wiki_data(path,encoding,titles):
    handler = WikiXmlHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    for line in open(path, encoding=encoding):
        parser.feed(line)
    frame=[]
    for title in set(titles).intersection(list(handler._content.keys())):
        frame.append({'title': title, 'url':handler._content[title][0], 'abstract':handler._content[title][1]})
    return pd.DataFrame(frame)

def publish_to_pg(db,table,df):
    engine = create_engine('postgresql://postgres@db:5432/'+db)
    con = engine.connect()
    df.to_sql(table, con, index=False)


