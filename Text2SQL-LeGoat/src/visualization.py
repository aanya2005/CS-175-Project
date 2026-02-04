import json
import matplotlib.pyplot as plt

SPIDER_DEV = "data/spider/dev.json"

def load_data():
    with open(SPIDER_DEV, "r") as f:
        return json.load(f)

def plot_question_length_distribution():
    data = load_data()
    lengths = [len(item["question"].split()) for item in data]

    plt.figure(figsize=(8, 5))
    plt.hist(lengths, bins=30)
    plt.xlabel("Question Length (tokens)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Natural Language Question Lengths (Spider Dev)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_question_length_distribution()
