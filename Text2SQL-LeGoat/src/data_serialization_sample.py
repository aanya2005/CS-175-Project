import json
from pathlib import Path
from typing import Dict, List, Tuple


SPIDER_DIR = Path("spider") / "spider_data"
TABLES_JSON = SPIDER_DIR / "tables.json"


# Open's Spider's tables.json
def load_tables() -> List[Dict]:
   with open(TABLES_JSON, "r") as f:
       return json.load(f)

#Spider has 200 databases, find me the schema this belongs to 
#This table is perpetrator and people is a table inside
def get_db_schema(tables_data: List[Dict], db_id: str) -> Dict:
   for item in tables_data:
       if item["db_id"] == db_id:
           return item
   raise ValueError(f"db_id '{db_id}' not found in tables.json")


#Pre-proccessing
def serialize_schema(schema: Dict) -> str:
    #Pull fieldsout of the spider schema dict
    table_names = schema["table_names_original"]
    column_names = schema["column_names_original"]
    primary_keys = set(schema["primary_keys"])
    foreign_keys = schema["foreign_keys"]

    #Creates a dictionary that looks up foreign keys
    fk_src_to_tgt = {src: tgt for src, tgt in foreign_keys}

    #Group columns by table
    table_to_cols: Dict[int, List[int]] = {i: [] for i in range(len(table_names))}
    for col_idx, (table_idx, _) in enumerate(column_names):
        if table_idx != -1:
            table_to_cols[table_idx].append(col_idx)
    lines = []
    lines.append(f"DATABASE: {schema['db_id']}\n")

    #Print each line as a block
    #For each column in that table add Primary/Foreign key tags
    for table_idx, table_name in enumerate(table_names):
        lines.append(f"TABLE {table_name} (")
        col_lines = []
        for col_idx in table_to_cols[table_idx]:
            _, col_name = column_names[col_idx]
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
    
    #Takes Relationship which is why perpetrator finds people table
    lines.append("RELATIONSHIPS:")
    if foreign_keys:
        for src, tgt in foreign_keys:
            src_table_idx, src_col = column_names[src]
            tgt_table_idx, tgt_col = column_names[tgt]
            lines.append(
                f"{table_names[src_table_idx]}.{src_col} -> {table_names[tgt_table_idx]}.{tgt_col}"
            )
    else:
        lines.append("(none)")

    return "\n".join(lines)


if __name__ == "__main__":
    tables = load_tables()
    example_db_id = tables[0]["db_id"]
    schema = get_db_schema(tables, example_db_id)
    print(serialize_schema(schema))

