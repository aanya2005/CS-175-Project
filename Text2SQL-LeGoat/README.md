# Text2SQL-LeGoat

**CS 175 Final Project — Winter 2026**  
**Project Name:** LeGoat

## Team Members
- Aanya Agrawal — 50709128 — aanyaa2@uci.edu
- Daniel Meza — 28162136 — mezada2@uci.edu
- Jesse James Gacs — 34264660 — jgacs@uci.edu

## Project Overview

Text2SQL-LeGoat studies how well instruction-tuned language models can translate natural language questions into SQL queries on the Spider benchmark. Our project compares a smaller model, **Gemma-3-4B-IT**, against **Mistral-7B-Instruct**, and also evaluates a **LoRA fine-tuned Gemma model**.

The main goal of this project is to understand when a smaller model can match or outperform a larger baseline in Text-to-SQL generation through:
- schema-aware prompting
- structured schema serialization
- prompt formatting choices
- parameter-efficient fine-tuning with LoRA
- error analysis across SQL difficulty levels

We evaluate our system using:
- **Exact Match (EM)**
- **Execution Accuracy (EX)**
- qualitative error analysis
- latency analysis
- small ablation studies on prompt and schema design

---
## Repository Structure

```text
CS-175-PROJECT/
├── runs/
│   ├── gemma-3-4b-it_dev_first100.jsonl
│   ├── gemma-3-4b-it_evaluations.csv
│   ├── gemma-3-4b-it_spider_results.csv
│   ├── gemma-3-4b-tuned_chat_full_fk_20.jsonl
│   ├── gemma-3-4b-tuned_chat_full_no_fkrel_20.jsonl
│   ├── gemma-3-4b-tuned_chat_reduced_fk_20.jsonl
│   ├── gemma-3-4b-tuned_dev_all_spider_results.csv
│   ├── gemma-3-4b-tuned_dev_all.jsonl
│   ├── gemma-3-4b-tuned_eval.jsonl
│   ├── gemma-3-4b-tuned_plain_full_fk_20.jsonl
│   ├── Mistral-7B-Instruct-v0.2_dev_all_results.csv
│   ├── Mistral-7B-Instruct-v0.2_dev_first100.jsonl
│   ├── Mistral-7B-Instruct-v0.2_evaluation.csv
│   └── Mistral-7B-Instruct-v0.2_spider_results.csv
├── spider/
│   └── spider_data/
│       ├── database/
│       ├── dev_gold.sql
│       ├── dev.json
│       ├── tables.json
│       ├── test_gold.sql
│       ├── test_tables.json
│       ├── test.json
│       ├── train_gold.sql
│       ├── train_others.json
│       └── train_spider.json
├── Text2SQL-LeGoat/
│   └── src/
│       ├── gemma-lora/
│       ├── gemma-lora-final/
│       ├── D.461/
│       ├── CS175.ipynb
│       ├── data_exploration.py
│       ├── data_serialization.py
│       ├── data_serialization_sample.py
│       ├── utils.py
│       ├── visual_analysis.py
│       └── visualization.py
├── README.md
├── requirements.txt
├── .gitignore
└── venv/

## Setup Instructions

## External Libraries Used

- PyTorch (`torch`) — https://pytorch.org/
- Hugging Face Transformers (`transformers`) — https://huggingface.co/docs/transformers/index
- Hugging Face Datasets (`datasets`) — https://huggingface.co/docs/datasets/index
- PEFT (`peft`) — https://huggingface.co/docs/peft/index
- TRL (`trl`) — https://huggingface.co/docs/trl/index
- BitsAndBytes (`bitsandbytes`) — https://github.com/TimDettmers/bitsandbytes
- Pandas (`pandas`) — https://pandas.pydata.org/
- Matplotlib (`matplotlib`) — https://matplotlib.org/
- SQLite (`sqlite3`) — Python standard library
- JSON (`json`) — Python standard library
- Regular Expressions (`re`) — Python standard library
- Path handling (`pathlib`) — Python standard library
- Time (`time`) — Python standard library
- Collections (`collections.Counter`) — Python standard library

## Publicly Available Code Used

- No public external repository code was directly copied or adapted into our project beyond standard usage of official libraries, model APIs, and dataset resources.
- Public resources used include:
  - Spider dataset — https://yale-lily.github.io/spider
  - Gemma model page — https://huggingface.co/google/gemma-3-4b-it
  - Mistral model page — https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
  - PEFT / LoRA documentation — https://huggingface.co/docs/peft/index


Project Components we wrote
1. Model Pipeline

Implemented pipelines to load and configure:
Gemma models
Mistral models
Integrated quantization using BitsAndBytesConfig
Applied parameter-efficient fine-tuning using LoRA

2. Data Preprocessing

Built serialization functions to convert Spider dataset entries into model-ready prompts
Included:
Schema formatting
Query-context construction
Text-to-SQL prompt engineering

3. Training

Used SFTTrainer from TRL for supervised fine-tuning
Trained models on the Spider dataset
Configured LoRA adapters for efficient training

4. Model Outputs

Generated SQL predictions from fine-tuned models
Stored outputs for evaluation and comparison

5. Evaluation

Implemented metrics:
Exact Match Accuracy
Execution Accuracy (if applicable)
Compared predicted SQL queries against ground truth

6. Visualization

Created plots to analyze performance
Used matplotlib for:
Accuracy vs difficulty
Performance breakdowns across query features
---

## Code Written Entirely by Our Team

- `data_serialization.py` — approximately 250 lines  
  Normalizes Spider schemas, serializes database schemas into prompt-ready text, supports schema reduction for ablation tests, and builds Text-to-SQL prompts.

- `data_exploration.py` — approximately 60 lines  
  Performs exploratory analysis on the Spider dataset, including question statistics, SQL complexity trends, and dataset distribution analysis.

- `visual_analysis.ipynb` — approximately 3 cells  
  Produces analysis plots for model performance, latency, and error trends across experiments.
Creates project figures and visual summaries such as difficulty distributions, SQL clause analysis, and model comparison plots.

- `CS175.ipynb` — approximately 20 cells / major notebook sections  
  Demonstrates loading the dataset, loading models, generating SQL predictions, running evaluations, and showing sample outputs and ablation experiments.
