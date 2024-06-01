import argparse
import csv
import random

parser = argparse.ArgumentParser(description="Generate prompts for the model")
parser.add_argument(
    "-n", "--num_shots", type=int, default=3, help="Number of shots to generate"
)
parser.add_argument(
    "-c",
    "--context_sentences",
    type=int,
    nargs="+",
    default=[0, 3, 5],
    help="List of context sentences to generate",
)

args = parser.parse_args()
num_shots = args.num_shots
context_sentences = args.context_sentences

base_prompt = ""
examples_tag = "<EXAMPLES>"
with open("prompts/base_prompt.txt", "r") as f:
    base_prompt = f.read()

sentences = []
with open("classification.csv", "r") as f:
    lines = list(csv.DictReader(f, delimiter=";"))
    sentences = random.sample(lines, num_shots)


def get_sentence_context(sentence, context):
    previous_sentences = []
    with open("transcripts/" + sentence["Filename"], "r") as f:
        lines = list(csv.DictReader(f, delimiter=";"))
        line_number = int(sentence["LineNumber"])
        for i in range(line_number - context - 1, line_number - 1):
            transcript = lines[i]["Transcription_Text"]
            previous_sentences.append('"' + transcript + '"')
    return previous_sentences


examples_with_context = []
for context in context_sentences:
    examples = []
    for sentence in sentences:
        prompt = "Q:\n"

        sentence_contexts = get_sentence_context(sentence, context)
        for sentence_context in sentence_contexts:
            prompt += sentence_context + "\n"

        prompt += '"' + sentence["Transcription"] + '"\n'
        prompt += "A: " + sentence["Classification"] + "\n"
        examples.append(prompt)
    examples_with_context.append("\n".join(examples))

for example in examples_with_context:
    prompt = base_prompt.replace(examples_tag, example, 1)
    print("Prompt:")
    print(prompt)
    print()
    print("=" * 30)
