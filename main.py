from modules import WikiXmlHandler, unzip_gzip, download_abstract, process_movies, process_wiki_data, publish_to_pg
import pandas as pd


if __name__ == "__main__":
    df = process_movies('movies_metadata.csv.zip',['title','budget','release_date','revenue','vote_average','ratio','production_companies'])
    #download_abstract('https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz', 'enwiki-latest-abstract.xml.gz')
    #unzip_gzip('enwiki-latest-abstract.xml.gz','enwiki-latest-abstract.xml')
    #df_2 = process_wiki_data('enwiki-latest-abstract.xml','utf-8',df['title'])
    #df = pd.merge(left=df, right=df_2, how='left', left_on='title', right_on='title')
    publish_to_pg(db='new_db',table='movie',df=df)




