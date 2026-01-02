from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        return json.load(file)

@app.get("/")
def read_root():
    return {"message": "Hello, This is the main application!"}

@app.get("/view")
def view_all():
    return load_data()

@app.get("/view/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient", example="P001")
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="height | weight | bmi"),
    order: str = Query("asc", description="asc or desc")
):
    valid_fields = {"height", "weight", "bmi"}
    valid_orders = {"asc", "desc"}

    sort_by = sort_by.lower()
    order = order.lower()

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort key. Choose from {valid_fields}"
        )

    if order not in valid_orders:
        raise HTTPException(
            status_code=400,
            detail="Order must be 'asc' or 'desc'"
        )

    data = load_data()
    reverse = order == "desc"

    return sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )
