import argparse
import csv
import random
import os


def generate_prompts(num_shots, context_sentences):
    base_prompt = ""
    examples_tag = "<EXAMPLES>"
    question_tag = "<QUESTION>"
    with open("prompts/base_prompt.txt", "r") as f:
        base_prompt = f.read()

    sentences = []
    with open("classifications/classification.csv", "r") as f:
        lines = list(csv.DictReader(f, delimiter=";"))
        sentences = random.sample(lines, num_shots)

    question_with_context = []
    random_file = random.sample(os.listdir("transcripts"), 1)
    max_context = max(context_sentences)
    with open("transcripts/" + random_file[0], "r") as f:
        lines = list(csv.DictReader(f, delimiter=";"))
        line_number = random.randint(0, len(lines))
        for i in range(line_number - max_context - 1, line_number + 1):
            if i < 0:
                continue
            question = '"' + lines[i]["Transcription_Text"] + '"'
            question_with_context.append(question)

    def get_sentence_context(sentence, context):
        previous_sentences = []
        with open("transcripts/" + sentence["Filename"], "r") as f:
            lines = list(csv.DictReader(f, delimiter=";"))
            line_number = int(sentence["LineNumber"])
            for i in range(line_number - context - 1, line_number - 1):
                if i < 0:
                    continue
                transcript = lines[i]["Transcription_Text"]
                previous_sentences.append('"' + transcript + '"')
        return previous_sentences

    examples_with_context = {}
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
        examples_with_context[context] = "\n".join(examples)

    prompts = []
    for context, example in examples_with_context.items():
        prompt = base_prompt.replace(examples_tag, example, 1)
        questions = "\n".join(question_with_context[-context - 1 :])
        prompt = prompt.replace(question_tag, questions, 1)
        prompts.append(prompt)

    return prompts


if __name__ == "__main__":
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
