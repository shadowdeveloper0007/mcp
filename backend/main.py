from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from data import TENANTS, UNITS, MAINTENANCE

app = FastAPI(title="Rent Manager API")


# ─────────────────────────────────────────
# REQUEST BODY MODELS
# Pydantic models define what data a POST
# request must contain
# ─────────────────────────────────────────

class MaintenanceRequest(BaseModel):
    unit: str
    issue: str
    priority: str = "normal"  # default value


# TENANT ENDpoints
@app.get("/tenants")
def get_all_tenants():
    """Return alll tenants"""
    return {"tenants":TENANTS,"total":len(TENANTS)}

@app.get("/tenants/unpaid")
def get_unpaid_tenants():
    """return tenants who have not paid this month"""
    unpaid=[t for t in TENANTS if not t["paid_this_month"]]
    return {"unpaid_tenants":unpaid,"total":len(unpaid)}


@app.get("/tenants/{tenant_id}")
def get_tenant(tenant_id:str):
    """Returns a single tenant by their ID"""
    tenant=next((t for t in TENANTS if t["id"]==tenant_id),None)
    if not tenant:
        raise HTTPException(status_code=404,detail="Tenant not found")
    return tenant

# UNIT ENDPOINTS

@app.get("/units")
def get_all_units():
    """return all units"""
    return {"units":UNITS,"total":len(UNITS)}

@app.get("/units/vacant")
def get_vacant_units():
    """retur all vacant units"""
    vacant=[u for u in UNITS if u["status"]=="vacant"]
    return {"vacant_units":vacant,"total":len(vacant)}

# MAINTENANCE ENDPOINTS
@app.get("/maintenance")
def get_all_maintenance():
    """return all maintenance requests"""
    return {"requests":MAINTENANCE,"total":len(MAINTENANCE)}


@app.get("/maintenance/open")
def get_open_maintenance():
    """return only open maintenance request"""
    open_requests=[m for m in MAINTENANCE if m["sttus"]=="open"]
    return {"open_requests":open_requests,"total":len(open_requests)}


@app.post("/maintenance")
def create_maintenance(request: MaintenanceRequest):
    """Creates a new maintenance request"""
    new_id = f"M{str(len(MAINTENANCE) + 1).zfill(3)}"
    new_request = {
        "id": new_id,
        "unit": request.unit,
        "issue": request.issue,
        "status": "open",
        "priority": request.priority
    }
    MAINTENANCE.append(new_request)
    return {"message": "Maintenance request created", "request": new_request}

# ─────────────────────────────────────────
# SUMMARY ENDPOINT
# ─────────────────────────────────────────

@app.get("/summary")
def get_summary():
    """Returns a portfolio-wide summary"""
    vacant  = [u for u in UNITS    if u["status"] == "vacant"]
    unpaid  = [t for t in TENANTS  if not t["paid_this_month"]]
    open_mx = [m for m in MAINTENANCE if m["status"] == "open"]

    return {
        "total_units":        len(UNITS),
        "vacant_units":       len(vacant),
        "total_tenants":      len(TENANTS),
        "unpaid_this_month":  len(unpaid),
        "open_maintenance":   len(open_mx)
    }