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

from typing import List, Optional
from pydantic import BaseModel


class Dataset(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    files: Optional[List[str]] = None
    has_study: Optional[str] = None


class Experiment(BaseModel):
    id: str
    name: Optional[str] = None
    has_study: Optional[str] = None
    instrument_model: Optional[str] = None


class File(BaseModel):
    id: str
    name: Optional[str]
    format: Optional[str]
    type: Optional[str]
    size: Optional[str]
    checksum: Optional[str]
    category: Optional[str]


class Publication(BaseModel):
    id: str
    title: Optional[str] = None


class Study(BaseModel):
    id: str
    title: Optional[str] = None
    type: Optional[str] = None
    abstract: Optional[str] = None
    publications: Optional[List[str]] = None
