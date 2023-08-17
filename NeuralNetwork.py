from SourceData import *
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv1d(1, 32, 3)
        self.pool = nn.MaxPool1d(2)
        self.fc1 = nn.Linear(32*2, 64)
        self.fc2 = nn.Linear(64, 2)  # Assuming binary classification

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, 32*2)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class ConvolutionalNeuralNetwork:
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
        features_tensor = torch.tensor(features_scaled, dtype=torch.float32).unsqueeze(1)
        labels_tensor = torch.tensor(labels_s, dtype=torch.long)
        dataset = TensorDataset(features_tensor, labels_tensor)
        loader = DataLoader(dataset, batch_size=32, shuffle=True)

        self.model = SimpleCNN()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        for epoch in range(10):  # Training for 10 epochs
            for data, target in loader:
                optimizer.zero_grad()
                outputs = self.model(data)
                loss = criterion(outputs, target)
                loss.backward()
                optimizer.step()

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
        features_tensor = torch.tensor(features_scaled, dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            outputs = self.model(features_tensor)
            _, predicted = torch.max(outputs, 1)
        return predicted.numpy()


if __name__ == '__main__':
    ConvolutionalNeuralNetwork()
