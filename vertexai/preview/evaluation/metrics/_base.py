# -*- coding: utf-8 -*-

# Copyright 2024 Google LLC
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
"""Base classes for evaluation metrics."""

import abc
from typing import Any, Callable, Dict, Literal, Union

from vertexai.preview.evaluation import constants
from vertexai.preview.evaluation.metrics import (
    metric_prompt_template as metric_prompt_template_base,
)


class _Metric(abc.ABC):
    """The abstract class for evaluation metric."""

    def __init__(self, metric: str):
        self._metric = metric

    def __str__(self):
        return self.metric_name

    @property
    def metric_name(self) -> str:
        return self._metric


class _ModelBasedMetric(_Metric):
    # TODO(b/354796368) Update the link to the public doc or the link content.
    """A Model-based Metric.

    An evaluation metric that evaluate generative AI model responses with a
    generative model as a rater. It can be for a single model, or two models.

    For more details on when to use model-based metrics, see
    [Evaluation methods and metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval).
    """

    def __init__(
        self,
        *,
        metric: str,
        metric_prompt_template: Union[
            metric_prompt_template_base.PointwiseMetricPromptTemplate,
            metric_prompt_template_base.PairwiseMetricPromptTemplate,
            str,
        ],
    ):
        """Initializes the model-based evaluation metric.

        Args:
          metric: Generic model based metric name.
          metric_prompt_template: A metric prompt template for performing
            the model-based evaluation. A freeform string is also accepted.
        """
        super().__init__(metric=metric)
        self.metric_prompt_template = str(metric_prompt_template)


class CustomMetric(_Metric):
    """The custom evaluation metric.

    A fully-customized CustomMetric that can be used to evaluate a single model
    by defining a metric function for a computation-based metric. The
    CustomMetric is computed on the client-side using the user-defined metric
    function in SDK only, not by the Vertex Gen AI Evaluation Service.

      Attributes:
        name: The name of the metric.
        metric_function: The user-defined evaluation function to compute a metric
          score. Must use the dataset row dictionary as the metric function
          input and return per-instance metric result as a dictionary output.
          The metric score must mapped to the name of the CustomMetric as key.
    """

    def __init__(
        self,
        name: str,
        metric_function: Callable[
            [Dict[str, Any]],
            Dict[str, Any],
        ],
    ):
        """Initializes the evaluation metric."""
        super().__init__(name)
        self.name = name
        self.metric_function = metric_function


class _AutomaticMetric(_Metric):
    """An automatic metric that computes deterministic score based on reference.

    An lexicon-based evaluation metric that evaluate a generative model's
    response on the given evaluation task with reference ground truth answers.
    It is a type of pointwise evaluation metric.

    For more details on when to use automatic metrics, see
    [Evaluation methods and
    metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval).
    """

    def __init__(
        self,
        metric: Literal[constants.Metric.ROUGE],
    ):
        """Initializes the automatic evaluation metric.

        Args:
          metric: The automatic evaluation metric name.
        """
        super().__init__(metric=metric)
