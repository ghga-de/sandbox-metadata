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

"""
This module provides Configuration for the API
"""

from functools import lru_cache
from ghga_service_chassis_lib.config import config_from_yaml
from ghga_service_chassis_lib.api import ApiConfigBase


@config_from_yaml(prefix="sandbox_metadata")
class Config(ApiConfigBase):
    """
    Config class that extends ghga_service_chassis_lib.api.ApiConfigBase
    """

    # config parameter needed for the api server
    # are inherited from ApiConfigBase
    db_url: str = "mongodb://localhost:27017"
    db_name: str = "metadata"
    fastapi_options: dict = {
        "root_path": "/",
        "openapi_url": "/openapi.json",
        "docs_url": "/docs",
    }


@lru_cache
def get_config() -> Config:
    """
    Get the Config object that encapsulates all the
    configuration for this application.
    """
    return Config()
