# Copyright 2020 Google LLC
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
#


def make_parent(parent: str) -> str:
    # Sample function parameter parent in create_annotation_spec_sample
    parent = parent

    return parent


def make_annotation_spec(
    display_name: str,
) -> google.cloud.aiplatform_v1alpha1.types.annotation_spec.AnnotationSpec:
    annotation_spec = {"display_name": display_name}

    return annotation_spec
