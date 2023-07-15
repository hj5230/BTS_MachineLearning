from sys import path as SYS_PATH
from os import getcwd

SYS_PATH.append(getcwd())

from SourceData import *
from RandomForest import *
from math import ceil, floor
import csv
from datetime import datetime


ROWS = 204800
HZ = 25600
RPM = 305
RPS = RPM / 60
ROWS_PER_ROT = ceil(HZ / RPS)
MAX_INT_ROT = floor(ROWS / ROWS_PER_ROT)
EXPORT = "./TestResults/complete_1.csv"


if __name__ == "__main__":
    print(f"Test start: {datetime.now()}\nLoading workbooks...")

    workbooks = WBS("sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1")
    state_list = ["1", "3", "9", "13", "15"]

    print("Workbooks loaded, starting tests...")

    with open(EXPORT, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["rounds\\state", "1", "3", "9", "13", "15"])
        for i in range(0, MAX_INT_ROT):
            print(f"Testing round {i}...")

            train_data = []
            test_data = []

            for state in state_list:
                for j in range(i):
                    ranger = Ranger(start=j * ROWS_PER_ROT, length=ROWS_PER_ROT)
                    segment, rem = Utils.paragraphing(
                        SensorData(workbooks, state), ranger
                    )
                    train_data.append(segment)
                ranger = Ranger(start=i * ROWS_PER_ROT, length=ROWS_PER_ROT)
                test_segment, _ = Utils.paragraphing(
                    SensorData(workbooks, state), ranger
                )
                test_data.append(test_segment)

            model = RandomForest(*train_data)
            predicted_states = []

            for test in test_data:
                predicted_states.append(model.predict_state(test)[0])

            writer.writerow([str(i)] + predicted_states)

        print("State prediction completed, Now closing workbooks...")

        workbooks.wclose()

        print("Workbooks closed, Exiting...")