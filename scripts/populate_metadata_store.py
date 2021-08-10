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
import typer
import json
import requests


def _check_response(response):
    if response.status_code != 200:
        print(response.json())
        exit()


def main(url: str = "http://localhost:8000"):
    study_records = json.load(open("examples/studies.json"))
    publication_records = json.load(open("examples/publications.json"))
    dataset_records = json.load(open("examples/datasets.json"))
    experiment_records = json.load(open("examples/experiments.json"))
    file_records = json.load(open("examples/files.json"))
    dap_records = json.load(open("examples/data_access_policies.json"))
    dac_records = json.load(open("examples/data_access_committees.json"))

    for study in study_records["studies"]:
        route = f"{url}/studies"
        response = requests.post(route, json=study)
        _check_response(response)

    for publication in publication_records["publications"]:
        route = f"{url}/publications"
        response = requests.post(route, json=publication)
        _check_response(response)

    for dataset in dataset_records["datasets"]:
        route = f"{url}/datasets"
        response = requests.post(route, json=dataset)
        _check_response(response)

    for experiment in experiment_records["experiments"]:
        route = f"{url}/experiments"
        response = requests.post(route, json=experiment)
        _check_response(response)

    for file in file_records["files"]:
        route = f"{url}/files"
        response = requests.post(route, json=file)
        _check_response(response)

    for dap in dap_records["data_access_policies"]:
        route = f"{url}/data_access_policies"
        response = requests.post(route, json=dap)
        _check_response(response)

    for dac in dac_records["data_access_committees"]:
        route = f"{url}/data_access_committees"
        response = requests.post(route, json=dac)
        _check_response(response)


if __name__ == "__main__":
    typer.run(main)
