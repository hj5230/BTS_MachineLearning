from sys import argv as ARGV, path as SYS_PATH
from os import getcwd, path as OS_PATH

SYS_PATH.append(getcwd())

from SourceData import *
from SupportVectorMachines import *
from math import ceil, floor
import csv
import random
from datetime import datetime


ROWS = 204800
HZ = 25600
RPM = 1475
RPS = RPM / 60
ROWS_PER_ROT = ceil(HZ / RPS)
MAX_INT_ROT = floor(ROWS / ROWS_PER_ROT)

# 5-fold cross-validation
TRAIN_ROUNDS = 156
TEST_ROUNDS = 39
REPEAT = 5

FPATH = OS_PATH.basename(ARGV[0])
EXPORT = f"./TestResults/support_vector_machines/input_shaft_cross_validate/{FPATH}.csv"


if __name__ == "__main__":
    print(f"Executing: {FPATH}\nTest start: {datetime.now()}\nLoading workbooks...")

    workbooks = WBS("sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1")
    state_list = ["1", "3", "9", "13", "15"]

    with open(EXPORT, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["rounds\\state", "1", "3", "9", "13", "15"])

        for _ in range(REPEAT):
            all_rounds = list(range(1, MAX_INT_ROT + 1))
            train_rounds = random.sample(all_rounds, TRAIN_ROUNDS)
            test_rounds = [
                round_ for round_ in all_rounds if round_ not in train_rounds
            ]

            print(f"Repeating test {_ + 1}/{REPEAT}: {datetime.now()}\nValidate group: {test_rounds}")

            train_data = []
            for state in state_list:
                for round_ in train_rounds:
                    ranger = Ranger(
                        start=(round_ - 1) * ROWS_PER_ROT, length=ROWS_PER_ROT
                    )
                    segment, rem = Utils.paragraphing(
                        SensorData(workbooks, state), ranger
                    )
                    train_data.append(segment)

            model = SupportVectorMachines(*train_data)

            for round_ in test_rounds:
                test_data = []
                for state in state_list:
                    ranger = Ranger(
                        start=(round_ - 1) * ROWS_PER_ROT, length=ROWS_PER_ROT
                    )
                    test_segment, _ = Utils.paragraphing(
                        SensorData(workbooks, state), ranger
                    )
                    test_data.append(test_segment)

                predicted_states = []
                for test in test_data:
                    predicted_states.append(model.predict_state(test)[0])

                writer.writerow([str(round_)] + predicted_states)

        print("State prediction completed, Now closing workbooks...")

        workbooks.wclose()

        print("Workbooks closed, Exiting...")
