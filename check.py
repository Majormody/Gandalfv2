import pymupdf4llm
import pymupdf
import pymupdf4llm

pymupdf4llm.use_layout(False)

file_path = "/root/AIProjects/Gandalfv2/ADXL345.pdf"
doc = pymupdf.open(file_path)

for page in doc:
    tables = page.find_tables(use_layout = False)
    print(page.number, len(tables.tables))