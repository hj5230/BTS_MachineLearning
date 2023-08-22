import numpy as np
import torch
import torch.nn as nn
from SourceData import *

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class ConvolutionalNeuralNetwork(nn.Module):
    def __init__(self, *sensor_data_list: [SensorData], num_layers=2, num_filters=16):
        super(ConvolutionalNeuralNetwork, self).__init__()
        self.num_layers = num_layers
        self.num_filters = num_filters

        features = []
        labels = []
        for sensor_data in sensor_data_list:
            df = sensor_data.dataframing()
            features.append(torch.Tensor(df.values))
            labels.append(sensor_data.state)
        features_tensor = torch.cat(features)
        self.label_to_index = {label: index for index, label in enumerate(np.unique(labels))}
        labels = [self.label_to_index[label] for label in labels]
        labels_tensor = torch.Tensor(np.array(labels)).to(torch.long)
        features_tensor = features_tensor.view(len(features), 1, -1)
        input_size = (features_tensor.shape[0], features_tensor.shape[2])
        layers = []
        input_channel = 1
        for i in range(num_layers):
            layers.append(nn.Conv1d(input_channel, num_filters, kernel_size=3))
            layers.append(nn.ReLU(inplace=True))
            input_channel = num_filters
            num_filters *= 2
        self.layers = nn.Sequential(*layers)
        self.fc1 = nn.Linear(self.num_filters * 2 ** (num_layers - 1) * (input_size[1] - num_layers * 2), 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 5)
        self.train_model(features_tensor, labels_tensor)

    def forward(self, x):
        x = self.layers(x)
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        x = torch.softmax(x, dim=1)
        return x

    def train_model(self, x, y, epochs=100, learning_rate=0.001):
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        self.to(device)
        x = x.to(device)
        y = y.to(device)
        for i in range(epochs):
            optimizer.zero_grad()
            outputs = self.forward(x)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            if i % 10 == 0:
                print(f"Epoch {i} - Loss: {loss.item()}")

    def predict_state(self, sensor_data: SensorData) -> np.ndarray:
        features = []
        labels = []
        df = sensor_data.dataframing()
        features.append(torch.Tensor(df.values))
        labels.append(sensor_data.state)
        features_tensor = torch.cat(features)
        features_tensor = features_tensor.view(len(features), 1, -1)
        self.eval()
        with torch.no_grad():
            features_tensor = features_tensor.to(device)
            outputs = self.forward(features_tensor)
            _, predicted = torch.max(outputs.data, 1)
        index_to_label = {index: label for label, index in self.label_to_index.items()}
        predicted = [index_to_label[index.item()] for index in predicted]
        return np.array(predicted)