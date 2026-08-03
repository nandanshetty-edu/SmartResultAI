from pathlib import Path

from services.excel_service import ExcelService

excel_folder = Path("sample_data/excel")

excel_path = list(excel_folder.glob("*.xlsx"))[0]

print("Using:", excel_path.name)

workbook, sheet = ExcelService.load_template(excel_path)

subject_map = ExcelService.build_subject_map(sheet)

result_columns = ExcelService.build_result_column_map(sheet)

print()

print(subject_map)

print()

print(result_columns)