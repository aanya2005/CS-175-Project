import json
from pathlib import Path
from typing import Dict, List, Tuple


SPIDER_DIR = Path("spider") / "spider_data"
TABLES_JSON = SPIDER_DIR / "tables.json"


def load_tables() -> List[Dict]:
   with open(TABLES_JSON, "r") as f:
       return json.load(f)


def get_db_schema(tables_data: List[Dict], db_id: str) -> Dict:
   for item in tables_data:
       if item["db_id"] == db_id:
           return item
   raise ValueError(f"db_id '{db_id}' not found in tables.json")


def serialize_schema(schema: Dict) -> str:
   table_names = schema["table_names_original"]
   column_names = schema["column_names_original"]
   foreign_keys = schema["foreign_keys"]


   table_to_cols: Dict[str, List[str]] = {t: [] for t in table_names}


   for (table_idx, col_name) in column_names:
       if table_idx == -1:
           continue
       table = table_names[table_idx]
       table_to_cols[table].append(col_name)
   lines = []
   lines.append(f"Database: {schema['db_id']}")
   lines.append("Tables:")


   for t in table_names:
       cols = ", ".join(table_to_cols[t])
       lines.append(f"- {t}({cols})")


   # Foreign keys
   if foreign_keys:
       lines.append("Foreign Keys:")
       for c1, c2 in foreign_keys:
           t1_idx, col1 = column_names[c1]
           t2_idx, col2 = column_names[c2]
           t1 = table_names[t1_idx]
           t2 = table_names[t2_idx]
           lines.append(f"- {t1}.{col1} -> {t2}.{col2}")


   return "\n".join(lines)


if __name__ == "__main__":
   tables = load_tables()


   # Pick a db to test. You can change this after printing the first few ids.
   example_db_id = tables[0]["db_id"]


   schema = get_db_schema(tables, example_db_id)
   print(serialize_schema(schema))

