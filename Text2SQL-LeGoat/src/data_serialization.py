import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SPIDER_DIR = Path("spider") / "spider_data"
TABLES_JSON = SPIDER_DIR / "tables.json"


def load_tables(tables_path: Path = TABLES_JSON) -> List[Dict]:
    with open(tables_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_db_index(tables_data: List[Dict]) -> Dict[str, Dict]:
    #Schema Dict access
    return {item["db_id"]: item for item in tables_data}

def serialize_schema(schema: Dict) -> str:
    table_names = schema["table_names_original"]
    column_names = schema["column_names_original"]
    primary_keys = set(schema["primary_keys"])
    foreign_keys = schema["foreign_keys"]

    fk_src_to_tgt = {src: tgt for src, tgt in foreign_keys}
    table_to_cols: Dict[int, List[int]] = {i: [] for i in range(len(table_names))}
    for col_idx, (table_idx, _col_name) in enumerate(column_names):
        if table_idx != -1:
            table_to_cols[table_idx].append(col_idx)

    lines: List[str] = []
    lines.append(f"DATABASE: {schema['db_id']}\n")

    for table_idx, table_name in enumerate(table_names):
        lines.append(f"TABLE {table_name} (")
        col_lines = []
        for col_idx in table_to_cols[table_idx]:
            _tidx, col_name = column_names[col_idx]
            tag = ""
            if col_idx in primary_keys:
                tag = " [PK]"
            if col_idx in fk_src_to_tgt:
                tgt_idx = fk_src_to_tgt[col_idx]
                tgt_table_idx, tgt_col_name = column_names[tgt_idx]
                tgt_table_name = table_names[tgt_table_idx]
                tag = f" [FK -> {tgt_table_name}.{tgt_col_name}]"
            col_lines.append(f"  {col_name}{tag}")
        lines.append(",\n".join(col_lines))
        lines.append(")\n")
    
    lines.append("RELATIONSHIPS:")
    if foreign_keys:
        for src, tgt in foreign_keys:
            src_table_idx, src_col_name = column_names[src]
            tgt_table_idx, tgt_col_name = column_names[tgt]
            lines.append(
                f"{table_names[src_table_idx]}.{src_col_name} -> "
                f"{table_names[tgt_table_idx]}.{tgt_col_name}"
            )
    else:
        lines.append("(none)")

    return "\n".join(lines)

def build_text2sql_prompt(
    question: str,
    schema_serialized: str,
    dialect_hint: str = "SQLite",
) -> str:
    return f"""You are a Text-to-SQL system.
Convert the user question into a correct {dialect_hint} SQL query using ONLY the given database schema.

DATABASE SCHEMA:
{schema_serialized}

QUESTION:
{question}

Return ONLY the SQL query. Do not include explanation, comments, or markdown.
SQL:
"""

def build_spider_prompt(example: Dict, db_index: Dict[str, Dict]) -> str:
    schema = db_index[example["db_id"]]
    schema_text = serialize_schema(schema)
    return build_text2sql_prompt(example["question"], schema_text)

if __name__ == "__main__":
    tables = load_tables()
    db_index = build_db_index(tables)

    db_id = "perpetrator" if "perpetrator" in db_index else tables[0]["db_id"]

    schema = db_index[db_id]
    schema_text = serialize_schema(schema)

    question = "List the names of all people."
    prompt = build_text2sql_prompt(question, schema_text)

    print("=== DB ID ===")
    print(db_id)
    print("\n=== SCHEMA (first 40 lines) ===")
    print("\n".join(schema_text.splitlines()[:40]))
    print("\n=== PROMPT (first 80 lines) ===")
    print("\n".join(prompt.splitlines()[:80]))

#Sample^
""" Another Prompt ask it directly to translate
Translate the question into a SQLite SQL query using the database schema below.

SCHEMA:
{schema}

QUESTION:
{question}

SQL:
"""

"""
You are an expert in translating natural language to SQL.

Use ONLY the tables and columns listed in the schema.
Do NOT invent table or column names.
If a column or table is not listed, do not use it.

DATABASE SCHEMA:
{schema}

QUESTION:
{question}

Return only a valid SQLIte SQL query.
SQL:
"""

