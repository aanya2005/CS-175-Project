import json
import pandas as pd
from collections import Counter

SPIDER_DEV = "data/spider/dev.json"
SPIDER_TRAIN = "data/spider/train_spider.json"
TABLES = "data/spider/tables.json"

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def explore_spider():
    dev_data = load_json(SPIDER_DEV)
    tables = load_json(TABLES)

    print(f"Number of dev examples: {len(dev_data)}")
    print(f"Number of databases: {len(tables)}")

    # Question length stats
    question_lengths = [len(item["question"].split()) for item in dev_data]

    print("Question length stats:")
    print(f"  Avg: {sum(question_lengths)/len(question_lengths):.2f}")
    print(f"  Min: {min(question_lengths)}")
    print(f"  Max: {max(question_lengths)}")

    # Count SQL components (simple heuristic)
    sql_keywords = ["SELECT", "WHERE", "JOIN", "GROUP BY", "ORDER BY", "HAVING"]
    keyword_counter = Counter()

    for item in dev_data:
        sql = item["query"].upper()
        for kw in sql_keywords:
            if kw in sql:
                keyword_counter[kw] += 1

    print("\nSQL Component Frequency (dev set):")
    for k, v in keyword_counter.items():
        print(f"{k}: {v}")

#extra schema stats
def schema_stats():
    tables = load_json(TABLES)
    num_tables = [len(db["table_names"]) for db in tables]

    print("\nSchema stats:")
    print(f"Avg tables per DB: {sum(num_tables)/len(num_tables):.2f}")
    print(f"Max tables in a DB: {max(num_tables)}")

schema_stats()


if __name__ == "__main__":
    explore_spider()
