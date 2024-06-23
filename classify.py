from groq import Groq
from prompts.generate_prompts import *
import argparse
from textwrap import dedent
from load_dotenv import load_dotenv
import os
from pprint import pprint
import re
from tqdm.contrib import itertools
from tqdm import trange
import pickle

load_dotenv()


def filter_answer(response):
    return re.match(r"(Classification: )?(\d)", response).group(2)


parser = argparse.ArgumentParser(description="Generate prompts for the model")
parser.add_argument(
    "-s",
    "--shots",
    type=int,
    nargs="+",
    default=list(range(0, 30, 3)),
    help="List of shots to generate",
)
parser.add_argument(
    "-c",
    "--context_sentences",
    type=int,
    nargs="+",
    default=list(range(0, 10, 1)),
    help="List of context sentences to generate",
)
parser.add_argument(
    "-n",
    "--num_prompts",
    type=int,
    default=10,
    help="Number of prompts to generate",
)

args = parser.parse_args()
num_shots = args.shots
context_sentences = args.context_sentences
num_prompts = args.num_prompts

system_prompt = generate_system_prompt()

i = 1
predictions = {}
with open("predictions.pkl", "rb") as f:
    predictions = pickle.load(f)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
for shot, context in itertools.product(num_shots, context_sentences):
    start = 0
    if (shot, context) in predictions:
        results = predictions[(shot, context)]
        if len(results) >= num_prompts:
            continue
        start = len(results)
    else:
        predictions[(shot, context)] = []
    for _ in trange(
        start,
        num_prompts,
        leave=False,
        desc=f"Generating prompts for {shot} shot and {context} context",
    ):
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        examples = generate_examples(shot, context)
        for question, answer in examples[:-1]:
            messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        user_prompt, expected_answer = examples[-1]
        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        answer = ""
        try:
            response = client.chat.completions.create(
                model=os.getenv("MODEL"), messages=messages, temperature=0.7
            )

            answer = response.choices[0].message.content
            predictions[(shot, context)].append(
                (filter_answer(answer), expected_answer)
            )
        except Exception as e:
            print("Error at shot:", shot, "context:", context)
            print("System prompt:", system_prompt)
            print("Examples:")
            pprint(examples)
            print("Answer:", answer)
            print("Error:", e)

    # Save predictions as checkpoints
    with open("predictions.pkl", "wb") as f:
        pickle.dump(predictions, f)
