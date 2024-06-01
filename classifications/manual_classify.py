import os
import random
import csv
import keyboard

"""
Get a random file from the transcripts directory
Show a random line and 5 before and after
Ask the user to classify the line without hitting enter (y if in-game, n if out-game, q to quit)
Save the classification in a continuous csv file with the filename, line number, transcription and classification
"""

# Get every
transcript_corpus_list = []
for file in os.listdir("./transcripts"):
    transcript_corpus_list.append(file)

total_in_game = 0
total_out_game = 0

# If the classification file does not exist, create it
if not os.path.exists("classification.csv"):
    with open("classification.csv", "w") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
        writer.writerow(
            [
                "Id",
                "Filename",
                "LineNumber",
                "Player",
                "Transcription",
                "Classification",
            ]
        )
else:
    with open("classification.csv", "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            if row[5] == "1":
                total_in_game += 1
            else:
                total_out_game += 1

while True:
    file = random.choice(transcript_corpus_list)
    with open(f"./transcripts/{file}", "r") as f:
        reader = csv.reader(f, delimiter=";")
        lines = list(reader)
        line_number = random.randint(0, len(lines))
        while "MATT" == lines[line_number][1]:
            line_number = random.randint(0, len(lines))
        print(f"File: {file}")
        print(f"Line: {line_number}")
        for i in range(line_number - 5, line_number + 6):
            try:
                if i == line_number:
                    print(f"\033[95m{lines[i][1]}: {lines[i][2]}\033[0m")
                else:
                    print(f"{lines[i][1]}: {lines[i][2]}")
            except IndexError:
                pass
        print("y: in-game, n: out-game, s: skip, q: quit")
        classification = input()
        if classification == "q":
            break
        if classification == "s":
            print("Skipping...")
            print("\n" + "-" * 80 + "\n")
            continue

        last_id = 0
        with open("classification.csv", "r") as f:
            reader = csv.reader(f)
            last_id = len(list(reader)) - 2

        with open("classification.csv", "a") as f:
            writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
            writer.writerow(
                [
                    last_id + 1,
                    file,
                    line_number,
                    lines[line_number][1],
                    lines[line_number][2],
                    1 if classification == "y" else 0,
                ]
            )

        if classification == "y":
            total_in_game += 1
        else:
            total_out_game += 1

        print("\n" + "-" * 80 + "\n")

        print(f"Total in-game: {total_in_game}")
        print(f"Total out-game: {total_out_game}")

        print("\n" + "-" * 80 + "\n")
