# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines API endpoints."""

from fastapi import FastAPI
from ghga_service_chassis_lib.api import configure_app

from metadata_service.database import get_db, close_db
from metadata_service.config import get_config
from metadata_service.routes.studies import studies_router
from metadata_service.routes.datasets import dataset_router
from metadata_service.routes.publications import publication_router
from metadata_service.routes.experiments import experiment_router
from metadata_service.routes.files import file_router
from metadata_service.routes.data_access_policy import data_access_policy_router
from metadata_service.routes.data_access_committee import data_access_committee_router
from metadata_service.routes.health import health_router
from metadata_service import __version__


app = FastAPI(
    title="Metadata Service API",
    version=__version__,
)
configure_app(app, config=get_config())

app.include_router(studies_router)
app.include_router(dataset_router)
app.include_router(experiment_router)
app.include_router(file_router)
app.include_router(publication_router)
app.include_router(publication_router)
app.include_router(data_access_policy_router)
app.include_router(data_access_committee_router)
app.include_router(health_router)
app.add_event_handler("startup", get_db)
app.add_event_handler("shutdown", close_db)
