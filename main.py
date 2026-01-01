from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/")
def read_root():
    return {"message": "Hello, This is the main application!"}

@app.get("/About")
def about():
    return {"message": "Hello, This is the About page of the main application!"}

@app.get("/view")
def view():
    data = load_data()
    return data