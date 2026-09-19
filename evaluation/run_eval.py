from evaluation.dataset_builder import build_eval_dataset
from evaluation.ragas_runner import  run_ragas_eval, EvalRecord
from pipeline import RagPipeline
from indexing.embedder import Embedder


import csv
import json
from pathlib import Path
import os
import asyncio



def load_questions(path: str) -> list[tuple[str, str]]:
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader) #to escape headers

        return [(question, answer) for question, answer, _ in reader ]


def save_eval_records(
    records: list[EvalRecord],
    path: str,
) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            [record.__dict__ for record in records],
            file,
            ensure_ascii=False,
            indent=2,
        )

def load_eval_records(path: str) -> list[EvalRecord]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [EvalRecord(**record) for record in data]

def save_eval_batch(results, path ="/root/AIProjects/Gandalfv2/evaluation/evaluation_results.json"):
    path = Path(path)
    temp_path = path.with_suffix(".temp.json")


    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            all_results = json.load(f)

    else:
        all_results = []

    all_results.extend(results)

    

    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
        f.flush
        os.fsync(f.fileno())

    os.replace(temp_path, path)


def load_results(path: str | Path)->list[dict]:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# Uncomment to generate answers
# with open("/root/AIProjects/Gandalfv2/stm32h753ii.pdf","rb") as f: #load the datasheet as bytes
#     datasheet = f.read()

# print("Datasheet Read!")

# loaded_qa = load_questions("/root/AIProjects/Gandalfv2/stm32h753_rag_dataset.txt")  #load the quesiton

# print("QA Loaded")

# rag = RagPipeline(Embedder())  #load the RAG pipeline

# print("Pipeline Created")

# rag.ingest(pdf_bytes=datasheet, file_name="stm32h753ii")  #ingestint the datasheet
# print("Datasheet ingested")

# records = build_eval_dataset(
#     pipeline=rag,
#     qa_pairs=loaded_qa[60:]
#     )

# print("Records Built")

# save_eval_records(
#     records,
#     "/root/AIProjects/Gandalfv2/evaluation/eval_records60.json",
# )


# print("Records Saved")

# Uncomment to evaluate:
# records = load_eval_records("/root/AIProjects/Gandalfv2/evaluation/eval_records60.json")

# print("Records Loaded")

# records_to_evaluate = records[13:]

# for i,record in enumerate(records_to_evaluate, start=1):
#     results = run_ragas_eval(records=[record])

#     print("Result Generated")

#     excluded = {
#     "question",
#     "reference",
#     "response",
#     "retrieved_contexts",
#     }

#     metrics = results[0].keys() - excluded

#     for metric in metrics:
#         values = [
#         record[metric]
#         for record in results
#         if isinstance(record.get(metric), (int, float))
#         ]

#         if values:
#             print(f"{metric}: {sum(values) / len(values):.4f}")

#     print("Result is being Saved")

#     save_eval_batch(results)

#     print("Result saved")

#     print(f"Record {i}/{len(records_to_evaluate)} done!")


# print("Finished Evaluating this batch")

# Uncomment to calculaye all metrics
records = load_results("evaluation/evaluation_results.json")

excluded = {
    "question",
    "reference",
    "response",
    "retrieved_contexts",
    "context_precision",
    }

metrics = records[0].keys() - excluded

for metric in metrics:
        values = [
        record[metric]
        for record in records
        if isinstance(record.get(metric), (int, float))
        ]

        if values:
            print(f"{metric}: {sum(values) / len(values):.4f}")


