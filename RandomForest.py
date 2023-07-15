from SourceData import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class RandomForest:
    def __init__(self, *sensor_data_list: SensorData) -> None:
        features = []
        labels = []
        for sensor_data in sensor_data_list:
            df = sensor_data.dataframing()
            features.append(self.extract_features(df))
            labels.append(sensor_data.state)
        features_df = pd.DataFrame(features)
        labels_s = pd.Series(labels)
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_df)
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(features_scaled, labels_s)
        self.classifier = clf
        self.scaler = scaler

    def extract_features(self, df: pd.DataFrame) -> list[float]:
        features = []
        for col in df.columns:
            features.append(df[col].mean())
            features.append(df[col].std())
            features.append(df[col].skew())
            features.append(df[col].kurtosis())
        return features

    def predict_state(self, sensor_data: SensorData) -> np.ndarray:
        df = sensor_data.dataframing()
        features = self.extract_features(df)
        features_df = pd.DataFrame([features])
        features_scaled = self.scaler.transform(features_df)
        state = self.classifier.predict(features_scaled)
        return state
