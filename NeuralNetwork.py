from SourceData import *
import numpy as np
import pandas as pd
import torch
from torch import nn, optim
from sklearn.preprocessing import StandardScaler


class ConvNetModel(nn.Module):
    def __init__(self):
        super(ConvNetModel, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
        )
        self.layer2 = nn.Sequential(
            nn.Conv1d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
        )
        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(1000, 10)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.drop_out(out)
        out = self.fc1(out)
        return out


class ConvolutionalNeuralNetwork:
    def __init__(self, *sensor_data_list: SensorData) -> None:
        self.model = ConvNetModel()
        self.scaler = StandardScaler()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

        features = []
        labels = []
        for sensor_data in sensor_data_list:
            df = sensor_data.dataframing()
            features.append(self.extract_features(df))
            labels.append(sensor_data.state)
        features = np.stack(features)
        labels = np.array(labels)

        self.scaler.fit(features)
        features = self.scaler.transform(features)

        features = torch.from_numpy(features).float().to(self.device)
        labels = torch.from_numpy(labels).long().to(self.device)

        self.model.train()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)

        for epoch in range(5):  # loop over the dataset multiple times
            optimizer.zero_grad()
            outputs = self.model(features.unsqueeze(1))
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    def extract_features(self, df: pd.DataFrame) -> list[float]:
        features = df.values.astype(np.float32)
        return features

    def predict_state(self, sensor_data: SensorData) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            df = sensor_data.dataframing()
            features = self.extract_features(df)
            features = self.scaler.transform(features.reshape(1, -1))
            features = torch.from_numpy(features).float().to(self.device)
            outputs = self.model(features.unsqueeze(1))
            _, predicted = torch.max(outputs.data, 1)
        return predicted.cpu().numpy()
