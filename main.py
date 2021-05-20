from fastapi import FastAPI, HTTPException

db = {
    "studies": {
        "STU:0000001": {
            "id": "STU:0000001",
            "title": "Whole Genome Sequencing of an individual",
            "type": "genomic",
            "abstract": "Whole genome sequencing of an individual with an uncharacterized disease",
            "publications": [
                "PMID:0000001",
                "PMID:0000002"
            ]
        },
        "STU:0000002": {
            "id": "STU:0000002",
            "title": "Whole Exome Sequencing of an individual",
            "type": "genomic",
            "abstract": "Whole exome sequencing of an individual with an uncharacterized disease",
            "publications": [
                "PMID:0000003",
                "DOI:00001234"
            ]
        }
    }
}

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/studies")
async def get_all_studies():
    return db["studies"]

@app.get("/studies/{id}")
async def get_studies(study_id):
    study = None
    if study_id not in db["studies"]:
        raise HTTPException(status_code=404, detail=f"Study with id {study_id} not found")
    study = db["studies"][study_id]    
    return study

@app.put("/studies/{id}")
async def update_studies(study_id, data: dict):
    if study_id not in db["studies"]:
        raise HTTPException(status_code=404, detail=f"Study with id {study_id} not found")
    study = db["studies"][study_id] = data
    return study
