import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

transcript_corpus_list = []
lines_to_check = []
for i in range(1, 116):
    if i != 46:
        transcript_corpus_list.append(
            pd.read_csv(
                f"https://raw.githubusercontent.com/leonardoemerson/Text-Search-and-Mining-Discipline-Project/main/transcripts/cr1-1-transcript-corpus.csv",
                sep=";",
                engine="python",
                on_bad_lines=lines_to_check.append,
                index_col=0,
            )
        )


def preprocess_text(text):
    # lower casing the data
    text = text.lower()
    # remove special characters and digits using regular expressions
    text = re.sub(r"\d+", "", text)  # remove digits
    text = re.sub(r"[^\w\s]", "", text)  # remove special characters

    # tokenize the text
    tokens = nltk.word_tokenize(text)

    return tokens


def remove_stopwords(tokens):
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens


def perform_lemmatization(tokens):
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens


def clean_text(text):
    tokens = preprocess_text(text)
    filtered_tokens = remove_stopwords(tokens)
    lemmatized_tokens = perform_lemmatization(filtered_tokens)
    clean_text = " ".join(lemmatized_tokens)
    return clean_text


for i in range(len(transcript_corpus_list)):
    for j in range(len(transcript_corpus_list[i])):
        if transcript_corpus_list[i]["Transcription_Text"][j] is not None:
            transcript_corpus_list[i]["Transcription_Text"][j] = clean_text(
                transcript_corpus_list[i]["Transcription_Text"][j]
            )
