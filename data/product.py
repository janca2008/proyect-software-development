import csv
from datetime import datetime
from models.product import ProductBase, ProductID
from enums.status import Status

data_base = "producto.csv"
history_base = "historial_producto.csv"

column_fields = [
    "id",
    "name",
    "starting_price",
    "finish_price",
    "description",
    "department",
    "category",
    "status"
]

history_fields = [
    "date",
    "product_id",
    "name",
    "action",
    "old_status",
    "new_status",
]


def auto_id():
    try:
        with open(data_base, "r") as csvfile:
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
        writer.writerow(register.model_dump(mode="json"))


def rewrite_all_products(products: list[ProductID]):
    with open(
        data_base, mode="w", newline=""
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )
        for product in products:
            writer.writerow(product.model_dump(mode="json"))


def write_history(product: ProductID, old_status: str, new_status: str):
    with open(history_base, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=history_fields)
        writer.writerow({
            "date": datetime.now().isoformat(timespec="seconds"),
            "product_id": product.id,
            "name": product.name,
            "action": "deactivated",
            "old_status": old_status,
            "new_status": new_status,
        })


def create_product(product: ProductBase):
    new_id = auto_id()
    new_product_ID = ProductID(
        id=new_id,
        **product.model_dump()
    )

    write_product_into_csv(new_product_ID)
    return new_product_ID


def read_all_products():
    try:
        with open(data_base) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=column_fields)
            return [ProductID(**row) for row in reader]
    except FileNotFoundError:
        return []


def read_active_products():
    return [
        p for p in read_all_products()
        if p.status == Status("active")
    ]


def read_one_product_by_id(product_id: int):
    for product in read_active_products():
        if product.id == product_id:
            return product
    return None

def filter_products(
    name: str | None = None,
    description: str | None = None,
    department: str | None = None,
    category: str | None = None,
    status: Status | None = None,
    min_starting_price: float | None = None,
    max_starting_price: float | None = None,
    min_finish_price: float | None = None,
    max_finish_price: float | None = None,
):
    def contains(value, text: str) -> bool:
        return text.lower() in str(value).lower()

    def same(value, text: str) -> bool:
        raw = getattr(value, "value", value)
        return str(raw).lower() == text.lower()

    results = read_all_products()

    if name:
        results = [p for p in results if contains(p.name, name)]
    if description:
        results = [p for p in results if contains(p.description, description)]
    if department:
        results = [p for p in results if same(p.department, department)]
    if category:
        results = [p for p in results if same(p.category, category)]
    if status is not None:
        results = [p for p in results if p.status == status]
    if min_starting_price is not None:
        results = [p for p in results if p.starting_price >= min_starting_price]
    if max_starting_price is not None:
        results = [p for p in results if p.starting_price <= max_starting_price]
    if min_finish_price is not None:
        results = [p for p in results if p.finish_price >= min_finish_price]
    if max_finish_price is not None:
        results = [p for p in results if p.finish_price <= max_finish_price]

    return results


def read_history():
    try:
        with open(history_base, newline="") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=history_fields)
            return list(reader)
    except FileNotFoundError:
        return []


def update_product(product_id: int, product: ProductBase):
    products = read_all_products()
    for i, current in enumerate(products):
        if current.id == product_id:
            products[i] = ProductID(
                id=product_id,
                **product.model_dump()
            )
            rewrite_all_products(products)
            return products[i]
    return None


def delete_product(product_id: int):
    products = read_all_products()
    for i, current in enumerate(products):
        if current.id == product_id:
            if current.status == Status("inactive"):
                return current
            old_status = current.status.value
            products[i] = current.model_copy(
                update={"status": Status("inactive")}
            )
            rewrite_all_products(products)
            write_history(products[i], old_status, "inactive")
            return products[i]
    return None
