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

"""Entrypoint of the package"""

from typing import Optional
import typer
from ghga_service_chassis_lib.api import run_server
from metadata_service.config import get_config
from metadata_service.api import app  # noqa: F401 pylint: disable=unused-import


def run(config: Optional[str] = typer.Option(None, help="Path to config yaml.")):
    """Starts backend server"""
    run_server(app="metadata_service.__main__:app", config=get_config())
    print(config)


def run_cli():
    """Run the command line interface"""
    typer.run(run)


if __name__ == "__main__":
    run_cli()
