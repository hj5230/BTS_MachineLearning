from SourceData import *
import numpy as np
import pandas as pd
import torch
from torch import nn, optim
from sklearn.preprocessing import StandardScaler


class NeuralNetwork:
    def __init__(self, *sensor_data_list: SensorData) -> None:
        features = []
        labels = []
        for sensor_data in sensor_data_list:
            df = sensor_data.dataframing()
            features.append(self.extract_features(df))
            labels.append(sensor_data.state)
        features = torch.Tensor(features)
        labels = torch.Tensor(labels).long()
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        self.scaler = scaler
        self.model = nn.Sequential(nn.Linear(features_scaled.shape[1], 64),
                                   nn.ReLU(),
                                   nn.Linear(64, 32),
                                   nn.ReLU(),
                                   nn.Linear(32, len(set(labels))),
                                   nn.LogSoftmax(dim=1))
        self.criterion = nn.NLLLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.003)
        epochs = 100
        for e in range(epochs):
            self.optimizer.zero_grad()
            output = self.model.forward(features_scaled)
            loss = self.criterion(output, labels)
            loss.backward()
            self.optimizer.step()

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
        features = torch.Tensor([features])
        features_scaled = self.scaler.transform(features)
        with torch.no_grad():
            logps = self.model(features_scaled)
        ps = torch.exp(logps)
        top_p, top_class = ps.topk(1, dim=1)
        return top_class.numpy()[0][0]
