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

"""Translate EGA metadata JSON to GHGA Schema compatible JSON"""

import os
import uuid
import json
from pathlib import Path
from typing import List, Dict, Union
import typer


ghga_objects: Dict = {
    "members": {},
    "data_access_committees": {},
    "data_access_policies": {},
    "studies": {},
    "datasets": {},
    "files": {},
    "publications": {}
}


def parse_ega_dacs(dacs: List[Dict]):
    """Translate EGA DAC to GHGA DataAccessCommittee objects"""
    for dac in dacs:
        ghga_dac = {
            "id": dac["egaStableId"],
            "title": dac["title"],
            "main_contact": None,
            "xref": [],
        }
        if dac["alias"]:
            ghga_dac["xref"].append(dac["alias"])
        if "creationTime" in dac:
            ghga_dac["creation_date"] = dac["creationTime"]
        ghga_objects["data_access_committees"][ghga_dac["id"]] = ghga_dac

        for contact in dac["contacts"]:
            # Translate contacts of an EGA DAC to GHGA Member objects
            ghga_member = {
                "id": str(uuid.uuid4()),
                "name": contact["contactName"],
                "email": contact["email"],
                "telephone": contact["phoneNumber"],
                "organization": contact["organisation"],
            }
            if ghga_member["id"] in ghga_objects["members"]:
                ghga_objects["members"][ghga_member["id"]].update(ghga_member)
            else:
                ghga_objects["members"][ghga_member["id"]] = ghga_member
            if contact["mainContact"]:
                # Contact is marked as the main contact for this DAC
                ghga_dac["main_contact"] = ghga_dac["id"]


def parse_ega_datasets(datasets: List[Dict]):
    """Translate EGA Dataset to GHGA Dataset objects"""
    for dataset in datasets:
        ghga_dataset = {
            "id": dataset["egaStableId"],
            "title": dataset["title"],
            "description": dataset["description"],
            "type": dataset["datasetTypes"],
            "has_data_access_policy": dataset["policyStableId"],
            "xref": [],
        }
        if dataset["alias"]:
            ghga_dataset["xref"].append(dataset["alias"])
        if "creationTime" in dataset:
            ghga_dataset["creation_date"] = dataset["creationTime"]
        if dataset["dacs"]:
            dacs = dataset["dacs"]
            if len(dacs) > 1:
                raise ValueError(
                    f"More than one EGA DAC associated with the same dataset: {dataset}"
                )
            dap = {
                "id": ghga_dataset["has_data_access_policy"],
                "has_data_access_committee": dacs[0],
            }
            ghga_objects["data_access_policies"][dap["id"]] = dap
        ghga_objects["datasets"][ghga_dataset["id"]] = ghga_dataset

        ghga_dap = {"id": dataset["policyStableId"]}
        if ghga_dap["id"] in ghga_objects["data_access_policies"]:
            ghga_objects["data_access_policies"][ghga_dap["id"]].update(ghga_dap)
        else:
            ghga_objects["data_access_policies"][ghga_dap["id"]] = ghga_dap


def parse_ega_studies(studies: List[Dict]):
    """Translate EGA Study to GHGA Study objects"""
    for study in studies:
        ghga_study = {
            "id": study["egaStableId"],
            "title": study["title"],
            "description": study["description"],
            "abstract": study["studyAbstract"],
            "type": study["studyType"],
            "has_dataset": study["datasets"],
            "xref": [],
        }
        if study["alias"]:
            ghga_study["xref"].append(study["alias"])
        if "creationTime" in study:
            ghga_study["creation_date"] = study["creationTime"]
        ghga_objects["studies"][ghga_study["id"]] = ghga_study

        if study["pubMedIds"]:
            # Translate pubMedIds to GHGA Publication objects
            for publication in study["pubMedIds"]:
                ghga_publication = {"id": publication}
            if ghga_publication["id"] in ghga_objects["publications"]:
                ghga_objects["publications"][ghga_publication["id"]].update(
                    ghga_publication
                )
            else:
                ghga_objects["publications"][ghga_publication["id"]] = ghga_publication

        for dataset_id in study["datasets"]:
            ghga_dataset = {"id": dataset_id}
            if ghga_dataset["id"] in ghga_objects["datasets"]:
                dataset = ghga_objects["datasets"][dataset_id]
                dataset["has_study"] = ghga_study["id"]
            else:
                raise KeyError(f"Error: Dataset {ghga_dataset['id']} does not exist!")


def main(
    ega_dac_json: List[Path] = None,
    ega_dataset_json: List[Path] = None,
    ega_studies_json: List[Path] = None,
    output: str = os.getcwd(),
    output_prefix: str = None,
):
    """Translate EGA metadata JSON to GHGA compatible JSON"""
    if ega_dac_json:
        for file in ega_dac_json:
            parse_ega_dacs(json.load(open(file)))
    if ega_dataset_json:
        for file in ega_dataset_json:
            parse_ega_datasets(json.load(open(file)))
    if ega_studies_json:
        for file in ega_studies_json:
            parse_ega_studies(json.load(open(file)))

    for coll_name, items in ghga_objects.items():
        items_list = list(items.values())
        if len(items) > 0:
            output_object = {coll_name: items_list}
            if output_prefix:
                filename = f"{output}{os.path.sep}{output_prefix}_{coll_name}.json"
            else:
                filename = f"{output}{os.path.sep}{coll_name}.json"
            json.dump(output_object, open(filename, "w"), indent=4)


if __name__ == "__main__":
    typer.run(main)
