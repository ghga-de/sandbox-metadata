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
Models
"""
from typing import Set, List, Optional, Union
from pydantic import BaseModel


class Publication(BaseModel):
    """
    Publication
    """

    __references__: Set = set()
    __collection__: str = "publication"
    id: str
    title: Optional[str] = None
    xref: Optional[List[str]] = None
    creation_date: Optional[str] = None
    update_date: Optional[str] = None


class Experiment(BaseModel):
    """
    Experiment
    """

    __references__: Set = set()
    __collection__: str = "experiment"
    id: str
    name: Optional[str] = None
    instrument_model: Optional[str] = None
    xref: Optional[List[str]] = None
    creation_date: Optional[str] = None
    update_date: Optional[str] = None


class Study(BaseModel):
    """
    Study
    """

    __references__: Set = {
        ("publications", Publication),
        ("has_experiment", Experiment),
    }
    __collection__: str = "study"
    id: str
    title: Optional[str] = None
    type: Optional[Union[str, List]] = None
    abstract: Optional[str] = None
    publications: Optional[List[Union[str, Publication]]] = None
    has_experiment: Optional[Union[str, Experiment]] = None
    xref: Optional[List[str]] = None
    creation_date: Optional[str] = None
    update_date: Optional[str] = None


class File(BaseModel):
    """
    File
    """

    __references__: Set = set()
    __collection__: str = "file"
    id: str
    name: Optional[str]
    format: Optional[str]
    type: Optional[Union[str, List]]
    size: Optional[str]
    checksum: Optional[str]
    category: Optional[str]
    xref: Optional[List[str]] = None
    creation_date: Optional[str] = None
    update_date: Optional[str] = None


class DataAccessCommittee(BaseModel):
    """
    Data Access Committee
    """

    __references__: Set = set()
    __collection__: str = "data_access_committee"
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    main_contact: Optional[str] = None
    has_members: Optional[List[str]] = None
    xref: Optional[List[str]] = None
    creation_date: Optional[str] = None
    update_date: Optional[str] = None


class DataAccessPolicy(BaseModel):
    """
    Data Access Policy
    """

    __references__: Set = {("has_data_access_committee", DataAccessCommittee)}
    __collection__: str = "data_access_policy"
    id: str
    description: Optional[str] = None
    policy_text: Optional[str] = None
    policy_url: Optional[str] = None
    has_data_access_committee: Optional[Union[str, DataAccessCommittee]] = None
    xref: Optional[List[str]] = None
    creation_date: Optional[str] = None
    update_date: Optional[str] = None


class Dataset(BaseModel):
    """
    Dataset
    """

    __references__: Set = {
        ("files", File),
        ("has_study", Study),
        ("has_data_access_policy", DataAccessPolicy),
    }
    __collection__: str = "dataset"
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Union[str, List]] = None
    files: Optional[List[Union[str, File]]] = None
    has_study: Optional[Union[str, Study]] = None
    has_data_access_policy: Optional[Union[str, DataAccessPolicy]] = None
    xref: Optional[List[str]] = None
    creation_date: Optional[str] = None
    update_date: Optional[str] = None
