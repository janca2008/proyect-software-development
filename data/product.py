import csv
from models.product import ProductBase,ProductID

data_base = "animal.csv"

column_fields = [
    "name",
    "starting_price",
    "finish_price",
    "utility",
    "description",
    "department",
    "category",
    "status",
]

def auto_id():
    try:
        with open(data_base,"r") as csvfile:
            reader = csv.DictReader(csvfile, column_fields)
            max_id = max(
                int(row["id"]) for row in reader
            )
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1


def write_product_into_csv(register: ProductID):
    with open(
            data_base, mode="a", newline=""
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )
        writer.writerow(register.model_dump())
