from ingestion.table_chunker import chunk_tables
from data_schemas import RawTable, Chunk


def test_first_case():
    table = RawTable(
        page_number = 1,
        table_index = 2,
        cells = [["Target Value", "min", "max", "operational"],
                 ["Voltage", "1", "20", "10"],
                 ["Voltage", "2", "20", "10"],
                 ["Voltage", "3", "20", "10"],
                 ["Voltage", "4", "20", "10"],
                 ["Voltage", "5", "20", "10"],
                 ["Voltage", "6", "20", "10"],
                 ["Voltage", "7", "20", "10"],
                 ["Voltage", "8", "20", "10"]]
    )

    chunks = chunk_tables([table], doc_id = "11")

    assert len(chunks) == 2
    assert len(chunks[0].metadata["rows"]) == 5
    assert len(chunks[1].metadata["rows"]) == 3



def test_second_case():
    table = RawTable(
        page_number = 1,
        table_index = 2,
        cells = [["Target Value", "min", "max", "operational"],
                 ["Voltage", "1", "20", "10"],
                 ["Voltage", "2", "20", "10"],
                 ["Voltage", "3", "20", "10"],
                 ]
    )

    chunks = chunk_tables([table], doc_id = "11")

    assert len(chunks) == 1
    assert len(chunks[0].metadata["rows"]) == 3


def test_third_case():
    table = RawTable(
        page_number = 1,
        table_index = 2,
        cells = [[None, None, None, None],
                 ["Voltage", "1", "20", "10"],
                 ["Voltage", "2", "20", "10"],
                 ["Voltage", "3", "20", "10"],
                 ]
    )

    chunks = chunk_tables([table], doc_id = "11")

    assert len(chunks) == 0


def test_fourth_case():
    table = RawTable(
        page_number = 1,
        table_index = 2,
        cells = [
                 ]
    )

    chunks = chunk_tables([table], doc_id = "11")

    assert len(chunks) == 0


def test_fifth_case():

    chunks = chunk_tables([], doc_id = "11")

    assert len(chunks) == 0


def test_sixth_case():
    table = RawTable(
        page_number = 1,
        table_index = 2,
        cells = [["Target Value", "min", "min", "operational"],
                 ["Voltage", "1", "20", "10"],
                 ["Voltage", "2", "20", "10"],
                 ["Voltage", "3", "20", "10"],
                 ]
    )

    chunks = chunk_tables([table], doc_id = "11")

    assert chunks[0].metadata["rows"] == [["Voltage", "1", "20", "10"],
                     ["Voltage", "2", "20", "10"],
                     ["Voltage", "3", "20", "10"]]
    assert len(chunks[0].metadata["headers"]) > len(chunks[0].metadata["structured"][0])
    assert "min : 1" in chunks[0].content
    assert "min : 20" in chunks[0].content

def test_seventh_case():
    table1= RawTable(
            page_number = 1,
            table_index = 2,
            cells = [["Target Value", "min", "max", "operational"],
                     ["Voltage", "1", "20", "10"],
                     ["Voltage", "2", "20", "10"],
                     ["Voltage", "3", "20", "10"],
                     ["Voltage", "4", "20", "10"],
                     ["Voltage", "5", "20", "10"],
                     ["Voltage", "6", "20", "10"],
                     ["Voltage", "7", "20", "10"],
                     ["Voltage", "8", "20", "10"]]
        )
    table2 = RawTable(
            page_number = 1,
            table_index = 3,
            cells = [["Target Value", "min", "max", "operational"],
                     ["Ampere", "1", "20", "10"],
                     ["Ampere", "2", "20", "10"],
                     ["Ampere", "3", "20", "10"],
                     ["Ampere", "4", "20", "10"],]
        )
    chunks = chunk_tables([table1,table2], doc_id = "11")

    all_ids = [chunk.chunk_id for chunk in chunks]
    assert len(set(all_ids)) == len(all_ids)





