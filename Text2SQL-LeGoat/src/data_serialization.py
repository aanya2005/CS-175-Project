import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SPIDER_DIR = Path("spider") / "spider_data"
TABLES_JSON = SPIDER_DIR / "tables.json"


def load_tables(tables_path: Path = TABLES_JSON) -> List[Dict]:
    with open(tables_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_db_index(tables_data: List[Dict]) -> Dict[str, Dict]:
    return {item["db_id"]: normalize_spider_schema(item) for item in tables_data}


def normalize_spider_schema(raw_schema: Dict) -> Dict:
    table_names = raw_schema["table_names_original"]
    column_names = raw_schema["column_names_original"]
    primary_keys = set(raw_schema["primary_keys"])
    foreign_keys = raw_schema["foreign_keys"]     


    fk_map = {}
    relationships = []

    for src_idx, tgt_idx in foreign_keys:
        src_table_id, src_col = column_names[src_idx]
        tgt_table_id, tgt_col = column_names[tgt_idx]

        src_table = table_names[src_table_id]
        tgt_table = table_names[tgt_table_id]

        fk_map[src_idx] = f"{tgt_table}.{tgt_col}"
        relationships.append({
            "source": f"{src_table}.{src_col}",
            "target": f"{tgt_table}.{tgt_col}"
        })

    tables = []
    for table_id, table_name in enumerate(table_names):
        cols = []
        for col_idx, (col_table_id, col_name) in enumerate(column_names):
            if col_table_id != table_id:
                continue
            cols.append({
                "name": col_name,
                "is_pk": col_idx in primary_keys,
                "fk_target": fk_map.get(col_idx)
            })

        tables.append({
            "table_name": table_name,
            "columns": cols
        })

    return {
        "db_id": raw_schema["db_id"],
        "tables": tables,
        "relationships": relationships
    }


def reduce_schema(schema, question):
    """
    Very simple heuristic:
    keep tables whose names appear in the question,
    plus bridge tables linked by FK if needed.
    """
    if question is None:
        return schema

    q = question.lower()
    kept_tables = []

    for table in schema["tables"]:
        if table["table_name"].lower() in q:
            kept_tables.append(table["table_name"])

    # fallback: if nothing matched, just keep full schema
    if not kept_tables:
        return schema

    # keep directly matched tables + tables connected by relationships
    expanded = set(kept_tables)
    for rel in schema.get("relationships", []):
        src_table = rel["source"].split(".")[0]
        tgt_table = rel["target"].split(".")[0]
        if src_table in expanded or tgt_table in expanded:
            expanded.add(src_table)
            expanded.add(tgt_table)

    reduced_tables = [t for t in schema["tables"] if t["table_name"] in expanded]
    reduced_relationships = []
    for rel in schema.get("relationships", []):
        src_table = rel["source"].split(".")[0]
        tgt_table = rel["target"].split(".")[0]
        if src_table in expanded and tgt_table in expanded:
            reduced_relationships.append(rel)

    reduced_schema = dict(schema)
    reduced_schema["tables"] = reduced_tables
    reduced_schema["relationships"] = reduced_relationships
    return reduced_schema


def serialize_schema(schema, schema_mode="full", include_fk_relationships=True, question=None):
    """
    schema: parsed Spider schema info
    schema_mode: 'full' or 'reduced'
    include_fk_relationships: whether to include RELATIONSHIPS section
    question: optional, used for reduced-schema filtering
    """

    if schema_mode == "reduced":
        schema = reduce_schema(schema, question)

    parts = []
    parts.append(f"DATABASE: {schema['db_id']}")

    for table in schema["tables"]:
        parts.append(f"\nTABLE {table['table_name']}")
        for col in table["columns"]:
            col_line = f"- {col['name']}"
            if col.get("is_pk"):
                col_line += " [PK]"
            if col.get("fk_target"):
                col_line += f" [FK -> {col['fk_target']}]"
            parts.append(col_line)

    if include_fk_relationships:
        parts.append("\nRELATIONSHIPS:")
        for rel in schema.get("relationships", []):
            parts.append(f"- {rel['source']} -> {rel['target']}")

    return "\n".join(parts)


def build_text2sql_prompt(
    question: str,
    schema_serialized: str,
    dialect_hint: str = "SQLite",
    prompt_style: str = "plain",
):
    plain_prompt = f"""You are a Text-to-SQL system.
Convert the user question into a correct {dialect_hint} SQL query using ONLY the given database schema.

DATABASE SCHEMA:
{schema_serialized}

QUESTION:
{question}

Return ONLY the SQL query. Do not include explanation, comments, or markdown.
SQL:
"""
    if prompt_style == "plain":
        return plain_prompt

    elif prompt_style == "chat":
        return [
            {
                "role": "system",
                "content": f"You are a Text-to-SQL system. Convert the user question into a correct {dialect_hint} SQL query using only the given schema. Return only SQL."
            },
            {
                "role": "user",
                "content": f"DATABASE SCHEMA:\n{schema_serialized}\n\nQUESTION:\n{question}"
            }
        ]
    elif prompt_style == "reason_sql":
        return [
            {
                "role": "system",
                "content": f"You are a Text-to-SQL system. First briefly reason about the schema/question, then provide the final {dialect_hint} SQL query."
            },
            {
                "role": "user",
                "content": f"DATABASE SCHEMA:\n{schema_serialized}\n\nQUESTION:\n{question}"
            }
        ]
    else:
        raise ValueError(f"Unknown prompt_style: {prompt_style}")

def build_spider_prompt(
    example: Dict,
    db_index: Dict[str, Dict],
    schema_mode: str = "full",
    include_fk_relationships: bool = True,
    prompt_style: str = "plain",
):
    schema = db_index[example["db_id"]]
    schema_text = serialize_schema(
        schema,
        schema_mode=schema_mode,
        include_fk_relationships=include_fk_relationships,
        question=example["question"],
    )
    return build_text2sql_prompt(
        example["question"],
        schema_text,
        prompt_style=prompt_style,
    )

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

