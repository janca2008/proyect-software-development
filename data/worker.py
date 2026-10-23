import csv
from datetime import datetime
from models.person import WorkerBase, WorkerID
from enums.status import Status

data_base = "trabajador.csv"
history_base = "historial_trabajador.csv"

column_fields = [
    "id",
    "first_name",
    "last_name",
    "id_type",
    "id_number",
    "phone_number",
    "email",
    "status",
    "position"
]

history_fields = [
    "date",
    "worker_id",
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


def write_worker_into_csv(register: WorkerID):
    with open(
        data_base, mode="a", newline=""
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )
        writer.writerow(register.model_dump(mode="json"))


def rewrite_all_workers(workers: list[WorkerID]):
    with open(
        data_base, mode="w", newline=""
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields,
        )
        for worker in workers:
            writer.writerow(worker.model_dump(mode="json"))


def write_history(worker: WorkerID, old_status: str, new_status: str):
    with open(history_base, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=history_fields)
        writer.writerow({
            "date": datetime.now().isoformat(timespec="seconds"),
            "worker_id": worker.id,
            "name": f"{worker.first_name} {worker.last_name}",
            "action": "deactivated",
            "old_status": old_status,
            "new_status": new_status,
        })


def create_worker(worker: WorkerBase):
    new_id = auto_id()
    new_worker_ID = WorkerID(
        id=new_id,
        **worker.model_dump()
    )

    write_worker_into_csv(new_worker_ID)
    return new_worker_ID


def read_all_workers():
    try:
        with open(data_base) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=column_fields)
            return [WorkerID(**row) for row in reader]
    except FileNotFoundError:
        return []


def read_active_workers():
    return [
        w for w in read_all_workers()
        if w.status == Status("active")
    ]


def read_one_worker_by_id(worker_id: int):
    for worker in read_active_workers():
        if worker.id == worker_id:
            return worker
    return None


def read_history():
    try:
        with open(history_base, newline="") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=history_fields)
            return list(reader)
    except FileNotFoundError:
        return []


def update_worker(worker_id: int, worker: WorkerBase):
    workers = read_all_workers()
    for i, current in enumerate(workers):
        if current.id == worker_id:
            workers[i] = WorkerID(
                id=worker_id,
                **worker.model_dump()
            )
            rewrite_all_workers(workers)
            return workers[i]
    return None


def delete_worker(worker_id: int):
    workers = read_all_workers()
    for i, current in enumerate(workers):
        if current.id == worker_id:
            if current.status == Status("inactive"):
                return current  # ya estaba desactivado, no repite el historial
            old_status = current.status.value
            workers[i] = current.model_copy(
                update={"status": Status("inactive")}
            )
            rewrite_all_workers(workers)
            write_history(workers[i], old_status, "inactive")
            return workers[i]
    return None