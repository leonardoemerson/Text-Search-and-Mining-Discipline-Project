import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"
}

print("Getting the list of episodes...")
main_url = "https://www.kryogenix.org/crsearch/html/index.html"
site = requests.get(main_url, headers=headers)
soup = BeautifulSoup(site.content, "html.parser")
episodes_list = soup.find_all("a", href=re.compile("cr1-"))
episodes_url = [episode["href"].replace(".html", "") for episode in episodes_list][::-1]
print(f"Found {len(episodes_url)} episodes, starting to scrape...")

for episode_name in tqdm(episodes_url):
    url = f"https://www.kryogenix.org/crsearch/html/{episode_name}.html"

    # getting site with requests lib
    site = requests.get(url, headers=headers)

    # parsing site content with beautifulsoup lib
    soup = BeautifulSoup(site.content, "html.parser")

    # dictionary to stores the data needed
    dic_transcriptions = {"Player_Name": [], "Transcription_Text": []}

    # find div with id "lines"
    main = soup.find_all("div", id="lines")

    # for each tag
    # check if dt or dd
    # if dt, save the name of the player
    # for every dd, save the text of the transcription
    current_line = 0
    for tag in main[0]:
        if tag.name == "dt":
            player_name = tag.get_text().strip().replace("# ", "")
            dic_transcriptions["Player_Name"].append(player_name)
            current_line += 1
        elif tag.name == "dd":
            transcript = tag.get_text().strip().replace(" →", "").replace('"', '""')
            if len(dic_transcriptions["Transcription_Text"]) < current_line:
                dic_transcriptions["Transcription_Text"].append(transcript)
            else:
                last_index = current_line - 1
                dic_transcriptions["Transcription_Text"][last_index] += "|" + transcript

    # converting dictionary to dataframe
    df_episode = pd.DataFrame(dic_transcriptions)

    # generating csv from dataframe
    df_episode.to_csv(
        f"./transcripts/{episode_name}-transcript-corpus.csv",
        encoding="utf-8",
        sep=";",
    )
