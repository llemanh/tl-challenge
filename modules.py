import pandas as pd
import gzip
import shutil
import requests
import ssl
import zipfile
import xml.sax
import subprocess
import ssl


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

