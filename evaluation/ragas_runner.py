from evaluation.dataset_builder import EvalRecord
from config import RAGAS_API_KEY, EMBED_MODEL_NAME


import time
from datasets import Dataset
from openai import AsyncOpenAI
from ragas import evaluate
from ragas.llms import llm_factory
from ragas.embeddings import HuggingFaceEmbeddings
from ragas.metrics.collections import (
    AnswerRelevancy,
    Faithfulness,
    ContextRecall,
    ContextPrecision,
)

def records_to_dataset(records: list[EvalRecord]) -> Dataset:
    return Dataset.from_list([
        {
            "user_input": record.question,
            "retrieved_contexts": record.contexts,
            "response": record.answer,
            "reference": record.ground_truth,
        }
        for record in records
    ])


LLM_client = AsyncOpenAI(
    base_url="https://api.cohere.com/compatibility/v1",
    api_key=RAGAS_API_KEY,
            )



evaluator_llm = llm_factory(
    client=LLM_client,
    model="command-a-plus-05-2026",
    max_tokens=64000
                )

evaluator_embeddings = HuggingFaceEmbeddings(
    model=EMBED_MODEL_NAME,
)

answer_relevancy = AnswerRelevancy(llm=evaluator_llm,
                                  embeddings=evaluator_embeddings,
                                  strictness=1)
faithfulness = Faithfulness(llm=evaluator_llm)
context_recall = ContextRecall(llm=evaluator_llm)
context_precision=ContextPrecision(llm=evaluator_llm)
metrics = [answer_relevancy, faithfulness, context_recall, context_precision]


# def records_to_dataset(records: list[EvalRecord]) -> Dataset:
#     return Dataset.from_list([
#         {
#             "user_input": record.question,
#             "retrieved_contexts": record.contexts,
#             "response": record.answer,
#             "reference": record.ground_truth,
#         }
#         for record in records
#     ])

def evaluate_record(record: EvalRecord)-> dict:

    results = {}

    # Answer Relevancy
    result = answer_relevancy.score(
        user_input=record.question,
        response=record.answer,
    )
    results["answer_relevancy"] = result.value

    Faithfulness
    result = faithfulness.score(
        user_input=record.question,
        response=record.answer,
        retrieved_contexts=record.contexts,
    )
    results["faithfulness"] = result.value

    # Context Recall
    result = context_recall.score(
        user_input=record.question,
        retrieved_contexts=record.contexts,
        reference=record.ground_truth,
    )
    results["context_recall"] = result.value

    # Context Precision
    # result = context_precision.score(
    #     user_input=record.question,
    #     retrieved_contexts=record.contexts,
    #     reference=record.ground_truth,
    # )
    # results["context_precision"] = result.value


    return{
        "question": record.question,
        "reference": record.ground_truth,
        "response": record.answer,
        "retrieved_contexts": record.contexts,

        **results,
    }

    

def run_ragas_eval(records: list[EvalRecord]):

    results = []
    for i, record in enumerate(records, start=1):
        print(f"Evaluating: {i}/{len(records)}")

        result = evaluate_record(record)
        results.append(result)

        print(f"Evlatuation Done, Sleeping inbtween")
        time.sleep(30)

    return results

