from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.data import MAINTENANCE, TENANTS, UNITS


app = FastAPI(title="Rent Manager API", version="1.0.0")


class MaintenanceRequest(BaseModel):
    unit: str
    issue: str
    priority: Literal["low", "normal", "high"] = "normal"


@app.get("/tenants")
def get_all_tenants() -> dict:
    return {"tenants": TENANTS, "total": len(TENANTS)}


@app.get("/tenants/unpaid")
def get_unpaid_tenants() -> dict:
    unpaid_tenants = [tenant for tenant in TENANTS if not tenant["paid_this_month"]]
    return {"unpaid_tenants": unpaid_tenants, "total": len(unpaid_tenants)}


@app.get("/tenants/{tenant_id}")
def get_tenant(tenant_id: str) -> dict:
    for tenant in TENANTS:
        if tenant["id"] == tenant_id:
            return tenant

    raise HTTPException(status_code=404, detail=f"Tenant '{tenant_id}' not found")


@app.get("/units")
def get_all_units() -> dict:
    return {"units": UNITS, "total": len(UNITS)}


@app.get("/units/vacant")
def get_vacant_units() -> dict:
    vacant_units = [unit for unit in UNITS if unit["status"] == "vacant"]
    return {"vacant_units": vacant_units, "total": len(vacant_units)}


@app.get("/maintenance")
def get_all_maintenance() -> dict:
    return {"requests": MAINTENANCE, "total": len(MAINTENANCE)}


@app.get("/maintenance/open")
def get_open_maintenance() -> dict:
    open_requests = [request for request in MAINTENANCE if request["status"] == "open"]
    return {"open_requests": open_requests, "total": len(open_requests)}


@app.post("/maintenance")
def create_maintenance(request: MaintenanceRequest) -> dict:
    request_id = f"M{len(MAINTENANCE) + 1:03d}"
    record = {
        "id": request_id,
        "unit": request.unit,
        "issue": request.issue,
        "status": "open",
        "priority": request.priority,
    }
    MAINTENANCE.append(record)
    return {"message": "Maintenance request created", "request": record}


@app.get("/summary")
def get_summary() -> dict:
    vacant_units = [unit for unit in UNITS if unit["status"] == "vacant"]
    unpaid_tenants = [tenant for tenant in TENANTS if not tenant["paid_this_month"]]
    open_requests = [request for request in MAINTENANCE if request["status"] == "open"]

    return {
        "total_units": len(UNITS),
        "vacant_units": len(vacant_units),
        "total_tenants": len(TENANTS),
        "unpaid_this_month": len(unpaid_tenants),
        "open_maintenance": len(open_requests),
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "rent-manager-backend"}
