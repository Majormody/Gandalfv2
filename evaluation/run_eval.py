from evaluation.dataset_builder import build_eval_dataset
from evaluation.ragas_runner import  run_ragas_eval, EvalRecord
from pipeline import RagPipeline
from indexing.embedder import Embedder


import csv
import json
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)
    



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



with open("/root/AIProjects/Gandalfv2/stm32h753ii.pdf","rb") as f: #load the datasheet as bytes
    datasheet = f.read()

print("Datasheet Read!")

loaded_qa = load_questions("/root/AIProjects/Gandalfv2/stm32h753_rag_dataset.txt")  #load the quesiton

print("QA Loaded")

rag = RagPipeline(Embedder())  #load the RAG pipeline

print("Pipeline Created")

rag.ingest(pdf_bytes=datasheet, file_name="stm32h753ii")  #ingestint the datasheet

print("Datasheet ingested")

records = build_eval_dataset(
    pipeline=rag,
    qa_pairs=loaded_qa
    )

print("Records Built")

save_eval_records(
    records,
    "/root/AIProjects/Gandalfv2/evaluation/eval_records.json",
)

print("Records Saved")

#result = run_ragas_eval(records=records,metrics=[answer_relevancy, faithfulness, context_recall, context_precision])

#print(result)
