import argparse
import csv
import random
import os


def generate_system_prompt():
    base_prompt = ""
    with open("prompts/base_prompt.txt", "r") as f:
        base_prompt = f.read()
    return base_prompt


def generate_examples(shot, context):
    examples = []
    with open("classifications/classification.csv", "r") as f:
        lines = list(csv.DictReader(f, delimiter=";"))
        lines_numbers = random.sample(range(len(lines)), context + 1)
        for line_number in lines_numbers:
            question = lines[line_number]
            contexts = ""
            for j in range(line_number - context, line_number + 1):
                if j < 0:
                    continue
                contexts += '"' + lines[j]["Transcription"] + '"\n'
            answer = question["Classification"]
            examples.append((contexts, answer))

    return examples
