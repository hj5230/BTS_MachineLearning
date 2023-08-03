from sys import argv as ARGV, path as SYS_PATH
from os import getcwd, path as OS_PATH

SYS_PATH.append(getcwd())

from SourceData import *
from NeuralNetwork import *
from math import ceil, floor
import csv
import random
from datetime import datetime


ROWS = 204800
HZ = 25600
RPM = 305
RPS = RPM / 60
ROWS_PER_ROT = ceil(HZ / RPS)
MAX_INT_ROT = floor(ROWS / ROWS_PER_ROT)

# Cross-validation across machines
TRAIN_ROUNDS = 32
TEST_ROUNDS = 8
REPEAT = 10

FPATH = OS_PATH.basename(ARGV[0])
EXPORT = f"./TestResults/random_forest/output_shaft_cross_validate/{FPATH}.csv"


if __name__ == "__main__":
    print(f"Executing: {FPATH}\nTest start: {datetime.now()}\nLoading workbooks...")

    train_workbooks = WBS(
        "sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1"
    )
    test_workbooks = WBS(
        "sDataF_P1XYZ_0208_1", "sDataF_P2XYZ_0208_1", "sDataF_P3XYZ_0208_1"
    )
    state_list = ["1", "3", "9", "13", "15"]

    with open(EXPORT, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["rounds\\state", "1", "3", "9", "13", "15"])

        for _ in range(REPEAT):
            all_rounds = list(range(1, MAX_INT_ROT + 1))
            train_rounds = random.sample(all_rounds, TRAIN_ROUNDS)
            test_rounds = random.sample(all_rounds, TEST_ROUNDS)

            print(f"Repeating test {_ + 1}/{REPEAT}: {datetime.now()}\nValidate group: {test_rounds}")

            train_data = []
            for state in state_list:
                for round_ in train_rounds:
                    ranger = Ranger(
                        start=(round_ - 1) * ROWS_PER_ROT, length=ROWS_PER_ROT
                    )
                    segment, rem = Utils.paragraphing(
                        SensorData(train_workbooks, state), ranger
                    )
                    train_data.append(segment)

            model = NeuralNetwork(*train_data)

            for round_ in test_rounds:
                test_data = []
                for state in state_list:
                    ranger = Ranger(
                        start=(round_ - 1) * ROWS_PER_ROT, length=ROWS_PER_ROT
                    )
                    test_segment, _ = Utils.paragraphing(
                        SensorData(test_workbooks, state), ranger
                    )
                    test_data.append(test_segment)

                predicted_states = []
                for test in test_data:
                    predicted_states.append(model.predict_state(test)[0])

                writer.writerow([str(round_)] + predicted_states)

        print("State prediction completed, Now closing workbooks...")

        train_workbooks.wclose()
        test_workbooks.wclose()

        print("Workbooks closed, Exiting...")
