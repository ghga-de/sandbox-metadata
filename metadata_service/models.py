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

from typing import List, Optional, Union
from pydantic import BaseModel


class Publication(BaseModel):
    __references__ = set()
    __collection__ = "publication"
    id: str
    title: Optional[str] = None


class Experiment(BaseModel):
    __references__ = set()
    __collection__ = "experiment"
    id: str
    name: Optional[str] = None
    instrument_model: Optional[str] = None


class Study(BaseModel):
    __references__ = {("publications", Publication), ("has_experiment", Experiment)}
    __collection__ = "study"
    id: str
    title: Optional[str] = None
    type: Optional[str] = None
    abstract: Optional[str] = None
    publications: Optional[List[Union[str, Publication]]] = None
    has_experiment: Optional[Union[str, Experiment]] = None


class File(BaseModel):
    __references__ = set()
    __collection__ = "file"
    id: str
    name: Optional[str]
    format: Optional[str]
    type: Optional[str]
    size: Optional[str]
    checksum: Optional[str]
    category: Optional[str]


class DataAccessCommittee(BaseModel):
    __references__ = set()
    __collection__ = "data_access_committee"
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    main_contact: Optional[str] = None
    has_members: Optional[List[str]] = None


class DataAccessPolicy(BaseModel):
    __references__ = {("has_data_access_committee", DataAccessCommittee)}
    __collection__ = "data_access_policy"
    id: str
    description: str = None
    policy_text: str = None
    policy_url: Optional[str] = None
    has_data_access_committee: Optional[Union[str, DataAccessCommittee]] = None


class Dataset(BaseModel):
    __references__ = {
        ("files", File), ("has_study", Study),
        ("has_data_access_policy", DataAccessPolicy)
    }
    __collection__ = "dataset"
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    files: Optional[List[Union[str, File]]] = None
    has_study: Optional[Union[str, Study]] = None
    has_data_access_policy: Optional[Union[str, DataAccessPolicy]] = None
