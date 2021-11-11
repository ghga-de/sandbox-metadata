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
from typing import List, Set, Dict, Union
import typer


ghga_objects: Dict = {
    "members": {},
    "data_access_committees": {},
    "data_access_policies": {},
    "studies": {},
    "datasets": {},
    "files": {},
    "publications": {},
    "samples": {},
    "technologies": {},
    "experiments": {},
    "biospecimens": {},
    "individuals": {},
}

ghga_map: Dict = {}


def generate_uuid() -> str:
    """
    Generate UUID
    """
    return str(uuid.uuid4())


def parse_attributes(
    original_obj: Dict, ghga_obj: Dict, parsed_fields: Set, attribute_fields: Set
) -> None:
    """
    Parse non-canonical fields as attributes.
    """
    if "has_attribute" not in ghga_obj:
        ghga_obj["has_attribute"] = []
    for field in attribute_fields:
        if field in original_obj and original_obj[field] and field not in parsed_fields:
            attribute_obj = {"key": field, "value": original_obj[field]}
            ghga_obj["has_attribute"].append(attribute_obj)


def generate_sample_entities(
    original_dataset: Dict, ghga_dataset: Dict, embedded: bool = False
) -> None:
    """
    Generate new Sample, Biospecimen, Individual, Experiment, Technology, and File entities.

    This method is basically simulating the metadata.
    """
    experiments = []
    for i in range(0, original_dataset["numSamples"]):
        ghga_sample = {
            "id": generate_uuid(),
            "name": f"Sample {i} for Dataset {ghga_dataset['id']}",
        }
        ghga_biospecimen = {
            "id": generate_uuid(),
            "name": f"Biospecimen for Sample {ghga_sample['id']}",
        }
        ghga_individual = {
            "id": generate_uuid(),
            "name": f"Individual for Sample {ghga_sample['id']}",
        }
        if embedded:
            ghga_biospecimen["has_individual"] = ghga_individual
            ghga_sample["has_individual"] = ghga_individual
            ghga_sample["has_biospecimen"] = ghga_biospecimen
        else:
            ghga_biospecimen["has_individual"] = ghga_individual["id"]
            ghga_sample["has_individual"] = ghga_individual["id"]
            ghga_sample["has_biospecimen"] = ghga_biospecimen["id"]

        ghga_objects["samples"][ghga_sample["id"]] = ghga_sample
        ghga_objects["biospecimens"][ghga_biospecimen["id"]] = ghga_biospecimen
        ghga_objects["individuals"][ghga_individual["id"]] = ghga_individual
        if "technology" in original_dataset:
            ghga_technology = {
                "id": generate_uuid(),
                "name": ", ".join(original_dataset["technology"]),
            }
            # TODO: Note, this is a quick fix for the scenario where
            # there is more than one technology lumped together in
            # dataset
            ghga_objects["technologies"][ghga_technology["id"]] = ghga_technology
        ghga_file = {
            "id": generate_uuid(),
            "name": f"File for Dataset {ghga_dataset['id']}",
        }
        ghga_objects["files"][ghga_file["id"]] = ghga_file
        ghga_experiment = {
            "id": generate_uuid(),
            "name": f"Experiment for Dataset {ghga_dataset['id']}",
            "has_sample": ghga_sample,
        }
        if embedded:
            ghga_experiment["has_technology"] = ghga_technology
            ghga_experiment["has_file"] = ghga_file
        else:
            ghga_experiment["has_technology"] = ghga_technology["id"]
            ghga_experiment["has_file"] = ghga_file["id"]

        experiments.append(ghga_experiment["id"])
        ghga_objects["experiments"][ghga_experiment["id"]] = ghga_experiment
    if embedded:
        ghga_dataset["has_experiment"] = [
            ghga_objects["experiments"][x] for x in experiments
        ]
    else:
        ghga_dataset["has_experiment"] = experiments


def parse_ega_dacs(dacs: List[Dict], embedded: bool = False) -> None:
    """
    Translate EGA DAC to GHGA DataAccessCommittee objects.
    """
    parsed_fields = {"egaStableId", "title", "alias", "creationTime"}
    attribute_fields = {"centerName", "released", "releasedDate", "published"}
    for dac in dacs:
        ghga_dac = {
            "id": generate_uuid(),
            "accession": dac["egaStableId"],
            "title": dac["title"],
            "main_contact": None,
            "xref": [],
        }
        if dac["alias"]:
            ghga_dac["xref"].append(dac["alias"])
        if "creationTime" in dac:
            ghga_dac["creation_date"] = dac["creationTime"]
        ghga_objects["data_access_committees"][ghga_dac["accession"]] = ghga_dac
        parse_attributes(dac, ghga_dac, parsed_fields, attribute_fields)
        if "contacts" in dac:
            ghga_dac["has_member"] = []
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
                    ghga_dac["main_contact"] = ghga_member["id"]
                if embedded:
                    ghga_dac["has_member"].append(ghga_member)
                else:
                    ghga_dac["has_member"].append(ghga_member["id"])


def parse_ega_datasets(datasets: List[Dict], embedded: bool = False):
    """
    Translate EGA Dataset to GHGA Dataset objects.
    """
    parsed_fields = {
        "egaStableId",
        "title",
        "description",
        "datasetTypes",
        "alias",
        "creationTime",
        "policyStableId",
        "dacs",
        "numSamples",
        "files",
        "technology",
    }
    attribute_fields = {
        "centerName",
        "availableInBeacon",
        "numSamples",
        "released",
        "releasedDate",
        "technology",
    }

    for dataset in datasets:
        ghga_dataset = {
            "id": generate_uuid(),
            "accession": dataset["egaStableId"],
            "title": dataset["title"],
            "description": dataset["description"],
            "type": dataset["datasetTypes"],
            "xref": [],
            "has_attribute": [],
        }
        if dataset["alias"]:
            ghga_dataset["xref"].append(dataset["alias"])
        if "creationTime" in dataset:
            ghga_dataset["creation_date"] = dataset["creationTime"]
        ghga_objects["datasets"][ghga_dataset["accession"]] = ghga_dataset
        ghga_dap = {"id": generate_uuid(), "accession": dataset["policyStableId"]}
        if embedded:
            ghga_dataset["has_data_access_policy"] = ghga_dap
        else:
            ghga_dataset["has_data_access_policy"] = ghga_dap["id"]

        if "numSamples" in dataset:
            generate_sample_entities(dataset, ghga_dataset, embedded=embedded)
        parse_attributes(dataset, ghga_dataset, parsed_fields, attribute_fields)
        if dataset["dacs"]:
            dacs = dataset["dacs"]
            if len(dacs) > 1:
                raise ValueError(
                    f"More than one EGA DAC associated with the same dataset: {dataset}"
                )
            ghga_dac = ghga_objects["data_access_committees"][dacs[0]]
            dap = {
                "id": generate_uuid(),
                "accession": ghga_dataset["has_data_access_policy"],
            }
            if embedded:
                dap["has_data_access_committee"] = ghga_dac
            else:
                dap["has_data_access_committee"] = ghga_dac["id"]
            ghga_objects["data_access_policies"][ghga_dap["accession"]] = ghga_dap
        if ghga_dap["accession"] in ghga_objects["data_access_policies"]:
            ghga_objects["data_access_policies"][ghga_dap["accession"]].update(ghga_dap)
        else:
            ghga_objects["data_access_policies"][ghga_dap["accession"]] = ghga_dap


def parse_ega_studies(studies: List[Dict], embedded: bool = False):
    """
    Translate EGA Study to GHGA Study objects.
    """
    parsed_fields = {
        "egaStableId",
        "title",
        "description",
        "studyType",
        "datasets",
        "studyAbstract",
        "alias",
        "creationTime",
        "pubMedIds",
    }
    attribute_fields = {"centerName", "released", "releasedDate", "published"}
    for study in studies:
        ghga_study = {
            "id": generate_uuid(),
            "accession": study["egaStableId"],
            "title": study["title"],
            "description": study["description"],
            "type": study["studyType"],
            "xref": [],
            "has_attribute": [],
        }
        if study["studyAbstract"]:
            if (
                len(study["description"])
                and study["studyAbstract"] != study["description"]
            ):
                raise ValueError(
                    f"EGA Study Abstract is different from EGA Study Description for {study['egaStableId']}"
                )
            if not len(study["description"]):
                ghga_study["description"] = study["studyAbstract"]

        if study["alias"]:
            ghga_study["xref"].append(study["alias"])
        if "creationTime" in study:
            ghga_study["creation_date"] = study["creationTime"]
        ghga_objects["studies"][ghga_study["accession"]] = ghga_study
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
        parse_attributes(study, ghga_study, parsed_fields, attribute_fields)
        for dataset_id in study["datasets"]:
            if dataset_id in ghga_objects["datasets"]:
                dataset = ghga_objects["datasets"][dataset_id]
                if embedded:
                    dataset["has_study"] = ghga_study
                else:
                    dataset["has_study"] = ghga_study["id"]
                for experiment in dataset["has_experiment"]:
                    if isinstance(experiment, str):
                        experiment = ghga_objects["experiments"][experiment]
                    if embedded:
                        experiment["has_study"] = ghga_study
                    else:
                        experiment["has_study"] = ghga_study["id"]
            else:
                raise KeyError(f"Error: Dataset {dataset_id} does not exist!")


def prune_embedded_objects(entities: List):
    """
    Prune embedded objects after depth of 1.
    """
    for entity in entities:
        for k1 in entity.keys():
            if k1.startswith("has_") and k1 not in {"has_attribute"}:
                embedded_obj = entity[k1]
                if isinstance(embedded_obj, dict):
                    for k2 in embedded_obj.keys():
                        if k2.startswith("has_") and k2 not in {"has_attribute"}:
                            inner_embedded_obj = embedded_obj[k2]
                            if isinstance(inner_embedded_obj, dict):
                                # one to one reference
                                _prune_embedded_object(inner_embedded_obj)
                            elif isinstance(inner_embedded_obj, list):
                                # one to many reference
                                for inner_embedded_object_entity in inner_embedded_obj:
                                    _prune_embedded_object(inner_embedded_object_entity)
                            else:
                                # string
                                pass


def _prune_embedded_object(embedded_object: Dict):
    """
    Prune an embedded object after depth of 1.
    """
    for k3 in embedded_object.keys():
        if k3.startswith("has_") and k3 not in {"has_attribute"}:
            inner_embedded_obj = embedded_object[k3]
            if isinstance(inner_embedded_obj, dict):
                embedded_object[k3] = inner_embedded_obj["id"]
            elif isinstance(inner_embedded_obj, list):
                if isinstance(inner_embedded_obj[0], dict):
                    embedded_object[k3] = [x["id"] for x in inner_embedded_obj]
            else:
                pass


def main(
    ega_dac_json: List[Path] = None,
    ega_dataset_json: List[Path] = None,
    ega_studies_json: List[Path] = None,
    output: str = os.getcwd(),
    output_prefix: str = None,
    embedded: bool = False,
):
    """
    Translate EGA metadata JSON to GHGA compatible JSON.
    """
    if ega_dac_json:
        for file in ega_dac_json:
            parse_ega_dacs(json.load(open(file)), embedded=embedded)
    if ega_dataset_json:
        for file in ega_dataset_json:
            parse_ega_datasets(json.load(open(file)), embedded=embedded)
    if ega_studies_json:
        for file in ega_studies_json:
            parse_ega_studies(json.load(open(file)), embedded=embedded)

    for coll_name, items in ghga_objects.items():
        items_list = list(items.values())
        if len(items) > 0:
            output_object = {coll_name: items_list}
            if embedded:
                prune_embedded_objects(items_list)
            if not os.path.exists(output):
                os.makedirs(output)
            if output_prefix:
                filename = f"{output}{os.path.sep}{output_prefix}_{coll_name}.json"
            else:
                filename = f"{output}{os.path.sep}{coll_name}.json"
            json.dump(output_object, open(filename, "w"), ensure_ascii=False, indent=4)

    print("Object counts\n-------------")
    for k, v in ghga_objects.items():
        print(f"{k}: {len(v.keys())}")


if __name__ == "__main__":
    typer.run(main)
