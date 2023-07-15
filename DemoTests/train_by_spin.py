"""
1: Normal forward rotation
3: turbine off-output forward rotation (intermediate shaft)
9: Worm moving forward (input shaft)
13: upper bearing rolling body scratch positive rotation (input shaft bearing roller)
15: Turbine scratch forward rotation (intermediate shaft and worm contact part)
"""
from sys import path as SYS_PATH
from os import getcwd

SYS_PATH.append(getcwd())

from SourceData import *
from RandomForest import *
from math import ceil, floor


ROWS = 204800
HZ = 25600
RPM = 305
RPS = RPM / 60
ROWS_PER_ROT = ceil(HZ / RPS)
MAX_INT_ROT = floor(ROWS / ROWS_PER_ROT)


if __name__ == "__main__":
    print("Opening workbooks...\n")

    workbooks_of_1st_machine = WBS(
        "sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1"
    )

    states = ["1", "3", "9", "13", "15"]
    trained_models = {}

    print("Workbooks successfully loaded, Now paragraphing...\n")

    # Training the models for each state
    for state in states:
        sensor_data_state = SensorData(workbooks_of_1st_machine, state)
        training_data = []

        for i in range(MAX_INT_ROT - 1):  # We leave one rotation for testing
            start = i * ROWS_PER_ROT
            end = (i + 1) * ROWS_PER_ROT
            ranger = Ranger(start=start, end=end)
            train_data, _ = Utils.paragraphing(sensor_data_state, ranger)
            training_data.append(train_data)

        print(f"Training model for state {state}...\n")

        model = RandomForest(*training_data)
        trained_models[state] = model

    print("Model training completed, Now predicting state...\n")

    # Testing the models with the last rotation data
    for state in states:
        ranger = Ranger(
            start=(MAX_INT_ROT - 1) * ROWS_PER_ROT, end=MAX_INT_ROT * ROWS_PER_ROT
        )
        test_data, _ = Utils.paragraphing(
            SensorData(workbooks_of_1st_machine, state), ranger
        )

        predicted_state = trained_models[state].predict_state(test_data)
        print(f"State {state} - Predicted state: {predicted_state[0]}")

    print("\nState prediction completed, Now closing workbooks...\n")

    workbooks_of_1st_machine.wclose()

    print("Workbooks closed, Exiting...")
