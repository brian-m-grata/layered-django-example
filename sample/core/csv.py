import csv
from typing import List, Dict

def read_csv_file(file_name: str) -> List[Dict[str, str]]:
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        return [row for row in reader]
