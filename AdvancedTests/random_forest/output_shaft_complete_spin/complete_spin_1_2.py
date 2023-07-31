from sys import argv as ARGV, path as SYS_PATH
from os import getcwd, path as OS_PATH

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

FPATH = OS_PATH.basename(ARGV[0])
EXPORT = f"./TestResults/{FPATH}.csv"


if __name__ == "__main__":
    print(f"Executing: {FPATH}\nTest start: {datetime.now()}\nLoading workbooks...")

    train_workbooks = WBS(
        "sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1"
    )
    test_workbooks = WBS(
        "sDataF_P1XYZ_0208_1", "sDataF_P2XYZ_0208_1", "sDataF_P3XYZ_0208_1"
    )
    state_list = ["1", "3", "9", "13", "15"]

    print("Workbooks loaded, starting tests...")

    with open(EXPORT, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["rounds\\state", "1", "3", "9", "13", "15"])

        train_data = []

        print("Paragraphing...")

        for state in state_list:
            for i in range(MAX_INT_ROT):
                ranger = Ranger(start=i * ROWS_PER_ROT, length=ROWS_PER_ROT)
                segment, rem = Utils.paragraphing(
                    SensorData(train_workbooks, state), ranger
                )
                train_data.append(segment)

        print("Training...")

        model = RandomForest(*train_data)

        for i in range(1, MAX_INT_ROT + 1):
            print(f"Testing round {i}")

            test_data = []
            for state in state_list:
                ranger = Ranger(start=(i - 1) * ROWS_PER_ROT, length=ROWS_PER_ROT)
                test_segment, _ = Utils.paragraphing(
                    SensorData(test_workbooks, state), ranger
                )
                test_data.append(test_segment)

            predicted_states = []

            for test in test_data:
                predicted_states.append(model.predict_state(test)[0])

            writer.writerow([str(i)] + predicted_states)

        print("State prediction completed, Now closing workbooks...")

        train_workbooks.wclose()
        test_workbooks.wclose()

        print("Workbooks closed, Exiting...")
