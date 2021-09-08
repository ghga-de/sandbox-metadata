#!/usr/bin/env python3

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

"""Populates the database with example data for each record type"""

import os
import json
from pathlib import Path
from typing import Literal, get_args
import requests
from requests.models import Response
import typer

HERE = Path(__file__).parent.resolve()

DEFAULT_EXAMPLES_DIR = HERE.parent.resolve() / "examples"

RecordTypes = Literal[
    "studies",
    "datasets",
    "files",
    "experiments",
    "data_access_committees",
    "publications",
    "data_access_policies",
]


def populate_record(
    base_url: str,
    example_dir: Path,
    record_type: RecordTypes,
    exit_on_error: bool = True,
) -> Response:
    """Populate the database with data for a specific record type"""

    file = os.path.join(example_dir, f"{record_type}.json")
    if os.path.exists(file):
        with open(file) as records_file:
            records = json.load(records_file)
        route = f"{base_url}/{record_type}"
        for record in records[record_type]:
            response = requests.post(route, json=record)
            if exit_on_error:
                # If non-2xx status code, will raise an exception:
                response.raise_for_status()
        return response
    return None


def main(
    base_url: str = "http://localhost:8080",
    example_dir: Path = DEFAULT_EXAMPLES_DIR,
    exit_on_error: bool = True,
):
    """Populate the database with examples for all record types"""

    typer.echo("This will populate the database with examples for all record types.")

    record_types = get_args(RecordTypes)
    for record_type in record_types:
        typer.echo(f"  - working on record type: {record_type}")
        response = populate_record(
            base_url=base_url,
            example_dir=example_dir,
            record_type=record_type,
            exit_on_error=exit_on_error,
        )
        if response:
            typer.echo(f"  - done with status code: {response.status_code}")

    typer.echo("Done.")


if __name__ == "__main__":
    typer.run(main)
