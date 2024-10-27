import string
import random


def load_text_from_file(filepath):
    with open(filepath) as f:
        corpus = f.read()
    return corpus


def preprocess_text(text):
    cleaned_text = text.lower()
    cleaned_text = cleaned_text.translate(str.maketrans("", "", string.punctuation))
    cleaned_text = cleaned_text.replace("\n", " ")
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text


def build_prefix_stats(text, prefix_length):
    prefix_stats = {}
    words = text.split()

    for i in range(len(words) - prefix_length):
        prefix = tuple(words[i : i + prefix_length])
        suffix = words[i + prefix_length]
        prefix_stats.setdefault(prefix, []).append(suffix)

    return prefix_stats


def generate_text(prefix_stats, initial_prefix, length):
    current_prefix = tuple(initial_prefix.split())
    generated_text = list(current_prefix)

    while len(generated_text) < length:
        if current_prefix not in prefix_stats or not prefix_stats[current_prefix]:
            break

        next_word = random.choice(prefix_stats[current_prefix])
        generated_text.append(next_word)
        current_prefix = tuple(generated_text[-len(current_prefix) :])

    return " ".join(generated_text)


def main():
    source_filepath = "source.txt"
    answer_filepath = "answer.txt"

    prefix_length = 1
    initial_prefix = "my"
    text_length = 1000

    corpus = load_text_from_file(source_filepath)
    cleaned_text = preprocess_text(corpus)
    prefix_stats = build_prefix_stats(cleaned_text, prefix_length)
    initial_prefix = initial_prefix.lower()
    generated_text = generate_text(prefix_stats, initial_prefix, text_length)

    with open(answer_filepath, "w") as f:
        f.write(generated_text)


if __name__ == "__main__":
    main() 