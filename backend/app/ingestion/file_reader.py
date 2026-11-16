
from pathlib import Path
from openpyxl import load_workbook
from docx import Document
from pypdf import PdfReader
import csv


def read_file(file_path):
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".xlsx":
        return read_excel(path)
    elif extension == ".docx":
        return read_docx(path)
    elif extension == ".pdf":
        return read_pdf(path)
    elif extension == ".csv":
        return read_csv(path)
    elif extension in [".txt", ".eml"]:
        return path.read_text(encoding="utf-8", errors="replace")
    else:
        return f"Unsupported file format: {extension}"


def read_excel(path):
    workbook = load_workbook(path, read_only=True, data_only=True)
    result = {}

    for sheet in workbook.worksheets:
        rows = sheet.iter_rows(values_only=True)
        headers = None

        for row in rows:
            non_empty = [
                value for value in row
                if value is not None and str(value).strip()
            ]

            if len(non_empty) >= 2:
                headers = [
                    str(value).strip() if value is not None else None
                    for value in row
                ]
                break

        if headers is None:
            result[sheet.title] = []
            continue

        records = []

        for row in rows:
            if not any(value is not None for value in row):
                continue

            record = {
                header: value
                for header, value in zip(headers, row)
                if header is not None
            }
            records.append(record)

        result[sheet.title] = records

    workbook.close()
    return result



def read_docx(path):
    document = Document(path)

    content = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            content.append(text)

    # Extract tables
    for table_number, table in enumerate(document.tables, start=1):
        content.append(f"\n[TABLE {table_number}]")

        for row in table.rows:
            row_data = [
                cell.text.strip().replace("\n", " ")
                for cell in row.cells
            ]

            content.append(" | ".join(row_data))

    return "\n".join(content)



def read_pdf(path):
    reader = PdfReader(str(path))
    return [
        {"page": number, "text": page.extract_text() or ""}
        for number, page in enumerate(reader.pages, start=1)
    ]


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))
