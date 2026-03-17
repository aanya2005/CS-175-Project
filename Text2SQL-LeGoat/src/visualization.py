"""This script analyzes the Spider development dataset (dev.json) and visualizes
the distribution of natural language question lengths.
It loads the dataset, computes the number of tokens in each question, and
generates a histogram showing how question lengths are distributed across
the dataset.

Purpose:
This analysis helps us understand the linguistic complexity of input queries
in the Text-to-SQL task. Although most questions are relatively short, they
often require complex SQL reasoning (e.g., joins, aggregation), which motivates
the need for schema-aware prompting."""

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
