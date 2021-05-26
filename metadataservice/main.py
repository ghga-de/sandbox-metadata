from fastapi import FastAPI
from metadataservice.routers.studies import studies_router
from metadataservice.routers.datasets import dataset_router
from metadataservice.routers.publications import publication_router
from metadataservice.routers.experiments import experiment_router
from metadataservice.routers.files import file_router

app = FastAPI(
    title="Metadata Service API",
    version="0.0.1",
)

app.include_router(studies_router)
app.include_router(dataset_router)
app.include_router(experiment_router)
app.include_router(file_router)
app.include_router(publication_router)
