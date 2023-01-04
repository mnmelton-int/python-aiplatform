# -*- coding: utf-8 -*-

# Copyright 2022 Google LLC
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

from typing import Optional, Dict, Union

from google.cloud.aiplatform_v1.types import (
    io as gca_io,
    model_monitoring as gca_model_monitoring_v1,
)

# TODO(b/242108750): remove temporary logic once model monitoring for batch prediction is GA
from google.cloud.aiplatform_v1beta1.types import (
    model_monitoring as gca_model_monitoring_v1beta1,
)

gca_model_monitoring = gca_model_monitoring_v1

TF_RECORD = "tf-record"
CSV = "csv"
JSONL = "jsonl"


class _SkewDetectionConfig:
    def __init__(
        self,
        data_source: Optional[str] = None,
        skew_thresholds: Union[Dict[str, float], float, None] = None,
        target_field: Optional[str] = None,
        attribute_skew_thresholds: Optional[Dict[str, float]] = None,
        data_format: Optional[str] = None,
    ):
        """Base class for training-serving skew detection.
        Args:
            data_source (str):
                Optional. Path to training dataset.

            skew_thresholds: Union[Dict[str, float], float, None]:
                Optional. Key is the feature name and value is the
                threshold. If a feature needs to be monitored
                for skew, a value threshold must be configured
                for that feature. The threshold here is against
                feature distribution distance between the
                training and prediction feature. If a float is passed,
                then all features will be monitored using the same
                threshold. If None is passed, all feature will be monitored
                using alert threshold 0.3 (Backend default).

            target_field (str):
                Optional. The target field name the model is to
                predict. This field will be excluded when doing
                Predict and (or) Explain for the training data.

            attribute_skew_thresholds (Dict[str, float]):
                Optional. Key is the feature name and value is the
                threshold. Feature attributions indicate how much
                each feature in your model contributed to the
                predictions for each given instance.

            data_format (str):
                Optional. Data format of the dataset, only applicable
                if the input is from Google Cloud Storage.
                The possible formats are:

                "tf-record"
                The source file is a TFRecord file.

                "csv"
                The source file is a CSV file.

                "jsonl"
                The source file is a JSONL file.
        """
        self.data_source = data_source
        self.skew_thresholds = skew_thresholds
        self.attribute_skew_thresholds = attribute_skew_thresholds
        self.data_format = data_format
        self.target_field = target_field

    def as_proto(
        self,
    ) -> gca_model_monitoring.ModelMonitoringObjectiveConfig.TrainingPredictionSkewDetectionConfig:
        """Converts _SkewDetectionConfig to a proto message.

        Returns:
            The GAPIC representation of the skew detection config.
        """
        skew_thresholds_mapping = {}
        attribution_score_skew_thresholds_mapping = {}
        default_skew_threshold = None
        if self.skew_thresholds is not None:
            if isinstance(self.skew_thresholds, float):
                default_skew_threshold = gca_model_monitoring.ThresholdConfig(
                    value=self.skew_thresholds
                )
            else:
                for key in self.skew_thresholds.keys():
                    skew_threshold = gca_model_monitoring.ThresholdConfig(
                        value=self.skew_thresholds[key]
                    )
                    skew_thresholds_mapping[key] = skew_threshold
        if self.attribute_skew_thresholds is not None:
            for key in self.attribute_skew_thresholds.keys():
                attribution_score_skew_threshold = gca_model_monitoring.ThresholdConfig(
                    value=self.attribute_skew_thresholds[key]
                )
                attribution_score_skew_thresholds_mapping[
                    key
                ] = attribution_score_skew_threshold
        return gca_model_monitoring.ModelMonitoringObjectiveConfig.TrainingPredictionSkewDetectionConfig(
            skew_thresholds=skew_thresholds_mapping,
            attribution_score_skew_thresholds=attribution_score_skew_thresholds_mapping,
            default_skew_threshold=default_skew_threshold,
        )


class _DriftDetectionConfig:
    def __init__(
        self,
        drift_thresholds: Dict[str, float],
        attribute_drift_thresholds: Dict[str, float],
    ):
        """Base class for prediction drift detection.
        Args:
            drift_thresholds (Dict[str, float]):
                Required. Key is the feature name and value is the
                threshold. If a feature needs to be monitored
                for drift, a value threshold must be configured
                for that feature. The threshold here is against
                feature distribution distance between different
                time windws.
            attribute_drift_thresholds (Dict[str, float]):
                Required. Key is the feature name and value is the
                threshold. The threshold here is against
                attribution score distance between different
                time windows.
        """
        self.drift_thresholds = drift_thresholds
        self.attribute_drift_thresholds = attribute_drift_thresholds

    def as_proto(
        self,
    ) -> gca_model_monitoring.ModelMonitoringObjectiveConfig.PredictionDriftDetectionConfig:
        """Converts _DriftDetectionConfig to a proto message.

        Returns:
            The GAPIC representation of the drift detection config.
        """
        drift_thresholds_mapping = {}
        attribution_score_drift_thresholds_mapping = {}
        if self.drift_thresholds is not None:
            for key in self.drift_thresholds.keys():
                drift_threshold = gca_model_monitoring.ThresholdConfig(
                    value=self.drift_thresholds[key]
                )
                drift_thresholds_mapping[key] = drift_threshold
        if self.attribute_drift_thresholds is not None:
            for key in self.attribute_drift_thresholds.keys():
                attribution_score_drift_threshold = (
                    gca_model_monitoring.ThresholdConfig(
                        value=self.attribute_drift_thresholds[key]
                    )
                )
                attribution_score_drift_thresholds_mapping[
                    key
                ] = attribution_score_drift_threshold
        return gca_model_monitoring.ModelMonitoringObjectiveConfig.PredictionDriftDetectionConfig(
            drift_thresholds=drift_thresholds_mapping,
            attribution_score_drift_thresholds=attribution_score_drift_thresholds_mapping,
        )


class _ExplanationConfig:
    def __init__(self):
        """Base class for ExplanationConfig."""
        self.enable_feature_attributes = False

    def as_proto(
        self,
    ) -> gca_model_monitoring.ModelMonitoringObjectiveConfig.ExplanationConfig:
        """Converts _ExplanationConfig to a proto message.

        Returns:
            The GAPIC representation of the explanation config.
        """
        return gca_model_monitoring.ModelMonitoringObjectiveConfig.ExplanationConfig(
            enable_feature_attributes=self.enable_feature_attributes
        )


class _ObjectiveConfig:
    def __init__(
        self,
        skew_detection_config: Optional[
            "gca_model_monitoring._SkewDetectionConfig"
        ] = None,
        drift_detection_config: Optional[
            "gca_model_monitoring._DriftDetectionConfig"
        ] = None,
        explanation_config: Optional["gca_model_monitoring._ExplanationConfig"] = None,
    ):
        """Base class for ObjectiveConfig.
        Args:
            skew_detection_config (_SkewDetectionConfig):
                Optional. An instance of _SkewDetectionConfig.
            drift_detection_config (_DriftDetectionConfig):
                Optional. An instance of _DriftDetectionConfig.
            explanation_config (_ExplanationConfig):
                Optional. An instance of _ExplanationConfig.
        """
        self.skew_detection_config = skew_detection_config
        self.drift_detection_config = drift_detection_config
        self.explanation_config = explanation_config
        # TODO(b/242108750): remove temporary logic once model monitoring for batch prediction is GA
        self._config_for_bp = False

    def as_proto(self) -> gca_model_monitoring.ModelMonitoringObjectiveConfig:
        """Converts _ObjectiveConfig to a proto message.

        Returns:
            The GAPIC representation of the objective config.
        """
        training_dataset = None
        if self.skew_detection_config is not None:
            training_dataset = (
                gca_model_monitoring.ModelMonitoringObjectiveConfig.TrainingDataset(
                    target_field=self.skew_detection_config.target_field
                )
            )
            if self.skew_detection_config.data_source.startswith("bq:/"):
                training_dataset.bigquery_source = gca_io.BigQuerySource(
                    input_uri=self.skew_detection_config.data_source
                )
            elif self.skew_detection_config.data_source.startswith("gs:/"):
                training_dataset.gcs_source = gca_io.GcsSource(
                    uris=[self.skew_detection_config.data_source]
                )
                if (
                    self.skew_detection_config.data_format is not None
                    and self.skew_detection_config.data_format
                    not in [TF_RECORD, CSV, JSONL]
                ):
                    raise ValueError(
                        "Unsupported value in skew detection config. `data_format` must be one of %s, %s, or %s"
                        % (TF_RECORD, CSV, JSONL)
                    )
                training_dataset.data_format = self.skew_detection_config.data_format
            else:
                training_dataset.dataset = self.skew_detection_config.data_source

        # TODO(b/242108750): remove temporary logic once model monitoring for batch prediction is GA
        gapic_config = gca_model_monitoring.ModelMonitoringObjectiveConfig(
            training_dataset=training_dataset,
            training_prediction_skew_detection_config=self.skew_detection_config.as_proto()
            if self.skew_detection_config is not None
            else None,
            prediction_drift_detection_config=self.drift_detection_config.as_proto()
            if self.drift_detection_config is not None
            else None,
            explanation_config=self.explanation_config.as_proto()
            if self.explanation_config is not None
            else None,
        )
        if self._config_for_bp:
            return (
                gca_model_monitoring_v1beta1.ModelMonitoringObjectiveConfig.deserialize(
                    gca_model_monitoring.ModelMonitoringObjectiveConfig.serialize(
                        gapic_config
                    )
                )
            )
        return gapic_config


class SkewDetectionConfig(_SkewDetectionConfig):
    """A class that configures skew detection for models deployed to an endpoint.

    Training-serving skew occurs when input data in production has a different
    distribution than the data used during model training. Model performance
    can deteriorate when production data deviates from training data.
    """

    def __init__(
        self,
        data_source: Optional[str] = None,
        target_field: Optional[str] = None,
        skew_thresholds: Union[Dict[str, float], float, None] = None,
        attribute_skew_thresholds: Optional[Dict[str, float]] = None,
        data_format: Optional[str] = None,
    ):
        """Initializer for SkewDetectionConfig.

        Args:
            data_source (str):
                Optional. Path to training dataset.

            target_field (str):
                Optional. The target field name the model is to
                predict. This field will be excluded when doing
                Predict and (or) Explain for the training data.

            skew_thresholds: Union[Dict[str, float], float, None]:
                Optional. Key is the feature name and value is the
                threshold. If a feature needs to be monitored
                for skew, a value threshold must be configured
                for that feature. The threshold here is against
                feature distribution distance between the
                training and prediction feature. If a float is passed,
                then all features will be monitored using the same
                threshold. If None is passed, all feature will be monitored
                using alert threshold 0.3 (Backend default).

            attribute_skew_thresholds (Dict[str, float]):
                Optional. Key is the feature name and value is the
                threshold. Feature attributions indicate how much
                each feature in your model contributed to the
                predictions for each given instance.

            data_format (str):
                Optional. Data format of the dataset, only applicable
                if the input is from Google Cloud Storage.
                The possible formats are:

                "tf-record"
                The source file is a TFRecord file.

                "csv"
                The source file is a CSV file.

                "jsonl"
                The source file is a JSONL file.

        Raises:
            ValueError for unsupported data formats.
        """
        super().__init__(
            data_source=data_source,
            skew_thresholds=skew_thresholds,
            target_field=target_field,
            attribute_skew_thresholds=attribute_skew_thresholds,
            data_format=data_format,
        )


class DriftDetectionConfig(_DriftDetectionConfig):
    """A class that configures prediction drift detection for models deployed to an endpoint.

    Prediction drift occurs when feature data distribution changes noticeably
    over time, and should be set when the original training data is unavailable.
    If original training data is available, SkewDetectionConfig should
    be set instead.
    """

    def __init__(
        self,
        drift_thresholds: Optional[Dict[str, float]] = None,
        attribute_drift_thresholds: Optional[Dict[str, float]] = None,
    ):
        """Initializer for DriftDetectionConfig.

        Args:
            drift_thresholds (Dict[str, float]):
                Optional. Key is the feature name and value is the
                threshold. If a feature needs to be monitored
                for drift, a value threshold must be configured
                for that feature. The threshold here is against
                feature distribution distance between different
                time windws.

            attribute_drift_thresholds (Dict[str, float]):
                Optional. Key is the feature name and value is the
                threshold. The threshold here is against
                attribution score distance between different
                time windows.
        """
        super().__init__(drift_thresholds, attribute_drift_thresholds)


class ExplanationConfig(_ExplanationConfig):
    """A class that enables Vertex Explainable AI.

    Only applicable if the model has explanation_spec populated. By default, explanation config is disabled. Instantiating this class will enable the config.
    """

    def __init__(self):
        """Initializer for ExplanationConfig."""
        super().__init__()
        self.enable_feature_attributes = True


class ObjectiveConfig(_ObjectiveConfig):
    """A class that captures skew detection, drift detection, and explanation configs."""

    def __init__(
        self,
        skew_detection_config: Optional["SkewDetectionConfig"] = None,
        drift_detection_config: Optional["DriftDetectionConfig"] = None,
        explanation_config: Optional["ExplanationConfig"] = None,
    ):
        """Initializer for ObjectiveConfig.
        Args:
            skew_detection_config (SkewDetectionConfig):
                Optional. An instance of SkewDetectionConfig.
            drift_detection_config (DriftDetectionConfig):
                Optional. An instance of DriftDetectionConfig.
            explanation_config (ExplanationConfig):
                Optional. An instance of ExplanationConfig.
        """
        super().__init__(
            skew_detection_config, drift_detection_config, explanation_config
        )
