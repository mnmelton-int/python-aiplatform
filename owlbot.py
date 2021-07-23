# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import os

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # ---------------------------------------------------------------------
    # Patch each version of the library
    # ---------------------------------------------------------------------

    # https://github.com/googleapis/gapic-generator-python/issues/413
    s.replace(
        library
        / f"google/cloud/aiplatform_{library.name}/services/prediction_service/client.py",
        "request.instances = instances",
        "request.instances.extend(instances)",
    )

    # https://github.com/googleapis/gapic-generator-python/issues/672
    s.replace(
        library
        / f"google/cloud/aiplatform_{library.name}/services/endpoint_service/client.py",
        "request.traffic_split.extend\(traffic_split\)",
        "request.traffic_split = traffic_split",
    )

    s.move(
        library,
        excludes=[
            ".pre-commit-config.yaml",
            "setup.py",
            "README.rst",
            "docs/index.rst",
            f"docs/definition_{library.name}/services.rst",
            f"docs/instance_{library.name}/services.rst",
            f"docs/params_{library.name}/services.rst",
            f"docs/prediction_{library.name}/services.rst",
            f"scripts/fixup_aiplatform_{library.name}_keywords.py",
            f"scripts/fixup_definition_{library.name}_keywords.py",
            f"scripts/fixup_instance_{library.name}_keywords.py",
            f"scripts/fixup_params_{library.name}_keywords.py",
            f"scripts/fixup_prediction_{library.name}_keywords.py",
            "google/cloud/aiplatform/__init__.py",
            f"google/cloud/aiplatform/{library.name}/schema/**/services/",
            f"tests/unit/gapic/aiplatform_{library.name}/test_prediction_service.py",
            f"tests/unit/gapic/definition_{library.name}/",
            f"tests/unit/gapic/instance_{library.name}/",
            f"tests/unit/gapic/params_{library.name}/",
            f"tests/unit/gapic/prediction_{library.name}/",
        ],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = common.py_library(cov_level=99, microgenerator=True)
s.move(
    templated_files, excludes=[".coveragerc", ".kokoro/samples/**"]
)  # the microgenerator has a good coveragerc file

# Don't treat docs warnings as errors
s.replace("noxfile.py", """["']-W["'],  # warnings as errors""", "")

# Replacement to install extra testing dependencies
s.replace(
    "noxfile.py",
    """session.install\("-e", ".", "-c", constraints_path\)""",
    """session.install("-e", ".[testing]", "-c", constraints_path)""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
