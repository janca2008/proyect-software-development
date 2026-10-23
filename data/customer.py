import csv
from datetime import datetime
from models.person import CustomerBase, CustomerID
from enums.status import Status

data_base = "cliente.csv"
history_base = "historial_cliente.csv"

column_fields = [
    "id",
    "first_name",
    "last_name",
    "id_type",
    "id_number",
    "phone_number",
    "email",
    "status",
    "address"
]

history_fields = [
    "date",
    "customer_id",
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


def write_customer_into_csv(register: CustomerID):
    with open(
        data_base, mode="a", newline=""
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )
        writer.writerow(register.model_dump(mode="json"))


def rewrite_all_customers(customers: list[CustomerID]):
    with open(
        data_base, mode="w", newline=""
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )
        for customer in customers:
            writer.writerow(customer.model_dump(mode="json"))


def write_history(customer: CustomerID, old_status: str, new_status: str):
    with open(history_base, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=history_fields)
        writer.writerow({
            "date": datetime.now().isoformat(timespec="seconds"),
            "customer_id": customer.id,
            "name": f"{customer.first_name} {customer.last_name}",
            "action": "deactivated",
            "old_status": old_status,
            "new_status": new_status,
        })


def create_customer(customer: CustomerBase):
    new_id = auto_id()
    new_customer_ID = CustomerID(
        id=new_id,
        **customer.model_dump()
    )

    write_customer_into_csv(new_customer_ID)
    return new_customer_ID


def read_all_customers():
    try:
        with open(data_base) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=column_fields)
            return [CustomerID(**row) for row in reader]
    except FileNotFoundError:
        return []


def read_active_customers():
    return [
        c for c in read_all_customers()
        if c.status == Status("active")
    ]


def read_one_customer_by_id(customer_id: int):
    for customer in read_active_customers():
        if customer.id == customer_id:
            return customer
    return None


def read_history():
    try:
        with open(history_base, newline="") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=history_fields)
            return list(reader)
    except FileNotFoundError:
        return []


def update_customer(customer_id: int, customer: CustomerBase):
    customers = read_all_customers()
    for i, current in enumerate(customers):
        if current.id == customer_id:
            customers[i] = CustomerID(
                id=customer_id,
                **customer.model_dump()
            )
            rewrite_all_customers(customers)
            return customers[i]
    return None


def delete_customer(customer_id: int):
    customers = read_all_customers()
    for i, current in enumerate(customers):
        if current.id == customer_id:
            if current.status == Status("inactive"):
                return current  # ya estaba desactivado, no repite el historial
            old_status = current.status.value
            customers[i] = current.model_copy(
                update={"status": Status("inactive")}
            )
            rewrite_all_customers(customers)
            write_history(customers[i], old_status, "inactive")
            return customers[i]
    return None