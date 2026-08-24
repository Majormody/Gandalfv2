import pymupdf4llm
import pymupdf

file_path = "/root/AIProjects/Gandalfv2/pic.pdf"
doc = pymupdf.open(file_path)

for page in doc:
    tables = page.find_tables()

    for table in tables.tables:
        data = table.extract()

        if not data:
            continue

        num_columns = len(data[0])

        for row in data:
            print(len(row), num_columns)