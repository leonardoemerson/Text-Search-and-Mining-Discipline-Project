from chatgpt import ChatGPT
from prompts.generate_prompts import generate_prompts
import argparse


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

prompts = generate_prompts(num_shots, context_sentences)
chats = []

for prompt in prompts:
    chat = ChatGPT(prompt)
    chats.append(chat)
    response = chat.get_response()
    print(response)

input("Press Enter to exit")
for chat in chats:
    chat.quit()
