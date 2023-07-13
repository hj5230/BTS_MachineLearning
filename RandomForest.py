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


if __name__ == "__main__":
    """
    1: Normal forward rotation
    3: turbine off-output forward rotation (intermediate shaft)
    9: Worm moving forward (input shaft)
    13: upper bearing rolling body scratch positive rotation (input shaft bearing roller)
    15: Turbine scratch forward rotation (intermediate shaft and worm contact part)
    """

    ranger = Ranger(start=0, length=512)

    workbooks_of_1st_machine = WBS("sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1")
    
    print("Workbooks successfully loaded, Now paragraphing...\n")

    state_normal_test, state_normal_train = Utils.paragraphing(
        SensorData(workbooks_of_1st_machine, "1"), ranger
    )
    state_off_output_test, state_off_output_train = Utils.paragraphing(
        SensorData(workbooks_of_1st_machine, "3"), ranger
    )
    state_turbo_jump_test, state_turbo_jump_train = Utils.paragraphing(
        SensorData(workbooks_of_1st_machine, "9"), ranger
    )
    state_bearing_scratch_test, state_bearing_scratch_train = Utils.paragraphing(
        SensorData(workbooks_of_1st_machine, "13"), ranger
    )
    state_turbine_scratch_test, state_turbine_scratch_train = Utils.paragraphing(
        SensorData(workbooks_of_1st_machine, "15"), ranger
    )

    print("Paragraphing completed, Now training model...\n")

    model = RandomForest(
        state_normal_train,
        state_off_output_train,
        state_turbo_jump_train,
        state_bearing_scratch_train,
        state_turbine_scratch_train,
    )

    print("Model training completed, Now predicting state...\n")

    predicted_state = model.predict_state(state_normal_test)
    print("Predicted state:", predicted_state[0])

    predicted_state = model.predict_state(state_off_output_test)
    print("Predicted state:", predicted_state[0])

    predicted_state = model.predict_state(state_turbo_jump_test)
    print("Predicted state:", predicted_state[0])

    predicted_state = model.predict_state(state_bearing_scratch_test)
    print("Predicted state:", predicted_state[0])

    predicted_state = model.predict_state(state_turbine_scratch_test)
    print("Predicted state:", predicted_state[0])

    print("\nState prediction completed, Now closing workbooks...\n")

    workbooks_of_1st_machine.wclose()

    print("Workbooks closed, Exiting...")
