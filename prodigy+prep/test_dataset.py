# from prodigy.components.db import connect
import sqlite3

# examples = [{"text": "hello world", "_task_hash": 123, "_input_hash": 456}]

# db = connect()                               # uses settings from prodigy.json
# db.add_dataset("test_dataset")               # add dataset
# assert "test_dataset" in db                  # check that dataset was added
# db.add_examples(examples, ["test_dataset"])  # add examples to dataset
# dataset = db.get_dataset("RUSSIAN_anno")     # retrieve a dataset

# print(dataset)
conn = sqlite3.connect("russian_anno.db")
cur = conn.cursor()
cur.execute("SELECT * FROM tasks")

rows = cur.fetchall()

for row in rows:
    print(row)
