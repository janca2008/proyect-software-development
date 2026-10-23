from fastapi import APIRouter, HTTPException
from models.person import WorkerBase, WorkerID
import data.worker as db

router = APIRouter()


@router.get("/", response_model=list[WorkerID])
def list_workers():
    return db.read_active_workers()


@router.get("/history/all")
def list_history():
    return db.read_history()


@router.get("/{worker_id}", response_model=WorkerID)
def get_worker(worker_id: int):
    worker = db.read_one_worker_by_id(worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return worker


@router.post("/", response_model=WorkerID, status_code=201)
def create_worker(worker: WorkerBase):
    return db.create_worker(worker)


@router.put("/{worker_id}", response_model=WorkerID)
def update_worker(worker_id: int, worker: WorkerBase):
    updated = db.update_worker(worker_id, worker)
    if updated is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return updated


@router.delete("/{worker_id}", response_model=WorkerID)
def delete_worker(worker_id: int):
    worker = db.delete_worker(worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return worker