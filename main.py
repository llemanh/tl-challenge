from modules import WikiXmlHandler, unzip_gzip, download_abstract
import pandas as pd
import xml.sax
import dask.bag as db


if __name__ == "__main__":
    df=pd.read_csv('movies_metadata.csv.zip')
    df['budget']=df['budget'].apply(pd.to_numeric, errors='coerce')
    df['ratio']=df['revenue']/df['budget']
    df = df.drop([col for col in df.columns if col not in ['title','budget','release_date','revenue','vote_average','ratio','production_companies']], axis=1)
    df = df.sort_values('ratio',ascending = False).head(1000).reset_index(drop=True)
    unzip_gzip('enwiki-latest-abstract.xml.gz','enwiki-latest-abstract.xml')
    handler = WikiXmlHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    for line in open('enwiki-latest-abstract.xml', encoding="utf8"):
        parser.feed(line)
    frame=[]
    for title in df['title']:
        try:
            frame.append({'title': title, 'url':handler._content[title][0], 'abstract':handler._content[title][1]})
        except KeyError:
            pass
    df_2 = pd.DataFrame(frame)
    df = pd.merge(left=df, right=df_2, how='left', left_on='title', right_on='title')





