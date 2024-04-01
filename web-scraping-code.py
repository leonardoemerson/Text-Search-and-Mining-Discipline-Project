#importing libaries
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#url used to web scraping
url = "https://criticalrole.fandom.com/wiki/Arrival_at_Kraghammer/Transcript"

#headers - key-value pairs sent between clients and servers using the HTTP protocol
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

#getting site with requests lib
site = requests.get(url, headers=headers)

#parsing site content with beautifulsoup lib
soup = BeautifulSoup(site.content, 'html.parser')

#dictionary to stores the data needed
dic_transcriptions = {'Transcription_Id':[], 'Player_Name':[], 'Transcription_Text':[], 'Stage_Of_The_Game':[]}

#filtering the html section necessary
main = soup.select("main", class_=re.compile('page__main'))

#getting the stage of the game
spans = []
for tag in main:
    spans.extend(tag.find_all('span', class_=re.compile('mw-headline')))

#getting the transcription messages
transcriptions_list=[]
for span in spans:
    transcriptions = span.find_all_next('p')
    transcriptions_list.append(list(transcriptions))

#removing intersections
for i in range(0, len(transcriptions_list)-1):
    transcriptions_list[i] = [x for x in transcriptions_list[i] if x not in transcriptions_list[i+1]]

#getting the text from tags and constructing dictionary
id_count = 0
for i in range(0, len(transcriptions_list)):
    for j in range(0, len(transcriptions_list[i])):
        transcriptions_list[i][j]= transcriptions_list[i][j].get_text().strip()
        dic_transcriptions['Transcription_Id'].append(id_count)
        dic_transcriptions['Transcription_Text'].append(transcriptions_list[i][j])
        dic_transcriptions['Stage_Of_The_Game'].append(spans[i].get_text().strip())
        dic_transcriptions['Player_Name'].append(transcriptions_list[i][j].split(':')[0])
        id_count+=1  

#converting dictionary to dataframe
df_arrival_at_kraghammer = pd.DataFrame(dic_transcriptions)

#generating csv from dataframe
df_arrival_at_kraghammer.to_csv('./arrival-at-kraghammer-transcript-corpus.csv', encoding='utf-8', sep=';')






