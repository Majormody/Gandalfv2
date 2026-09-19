from dataclasses import dataclass

import time

@dataclass
class EvalRecord:
    question: str
    contexts: list[str]
    answer: str
    ground_truth: str


from pipeline import RagPipeline

def build_eval_dataset(pipeline: RagPipeline, qa_pairs: list[tuple[str, str]])-> list[EvalRecord]:
    eval_records =[]

    for question, ground_truth in qa_pairs:
        gen_result = pipeline.ask(question)
        time.sleep(23)
        model_answer = gen_result.answer
        contexts = []
        for text_chunk in gen_result.sources.text_chunks:
            contexts.append(text_chunk.chunk.content)

        for table_chunk in gen_result.sources.table_chunks:
                    contexts.append(table_chunk.chunk.content)

        eval_records.append(EvalRecord(
              question=question,
              answer=model_answer,
              contexts=contexts,
              ground_truth=ground_truth
        ))

    return eval_records

        

        







