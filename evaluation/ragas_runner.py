from evaluation.dataset_builder import EvalRecord
from config import RAGAS_API_KEY, EMBED_MODEL_NAME


from ragas import evaluate
from ragas.llms import llm_factory
from ragas.embeddings import HuggingFaceEmbeddings
from datasets import Dataset
from openai import OpenAI


LLM_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=RAGAS_API_KEY,
            )

evaluator_llm = llm_factory(
    client=LLM_client,
    model="qwen/qwen3.8-27b",
                )

evaluator_embeddings = HuggingFaceEmbeddings(
    model=EMBED_MODEL_NAME,
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

def run_ragas_eval(records: list[EvalRecord], metrics: list):

    dataset = records_to_dataset(records)
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )

    return result

