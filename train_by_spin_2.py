"""
1: Normal forward rotation
3: turbine off-output forward rotation (intermediate shaft)
9: Worm moving forward (input shaft)
13: upper bearing rolling body scratch positive rotation (input shaft bearing roller)
15: Turbine scratch forward rotation (intermediate shaft and worm contact part)
"""


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
    ranger = Ranger(start=0, length=ROWS_PER_ROT)

    print("Opening workbooks...\n")

    # Load workbooks of 1st machine for training
    workbooks_of_1st_machine = WBS(
        "sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1"
    )
    # Load workbooks of 2nd machine for testing
    workbooks_of_2nd_machine = WBS(
        "sDataF_P1XYZ_0208_1", "sDataF_P2XYZ_0208_1", "sDataF_P3XYZ_0208_1"
    )
    state_list = ["1", "3", "9", "13", "15"]
    train_data = []

    for state in state_list:
        for _ in range(MAX_INT_ROT):
            segment, rem = Utils.paragraphing(
                SensorData(workbooks_of_1st_machine, state), ranger
            )
            train_data.append(segment)

    print("Training data prepared, Now training model...\n")

    model = RandomForest(*train_data)

    print("Model training completed, Now predicting state...\n")

    for state in state_list:
        test_data, _ = Utils.paragraphing(
            SensorData(workbooks_of_2nd_machine, state), ranger
        )
        predicted_state = model.predict_state(test_data)
        print(f"For state {state}, predicted state: {predicted_state[0]}")

    print("\nState prediction completed, Now closing workbooks...\n")

    workbooks_of_1st_machine.wclose()
    workbooks_of_2nd_machine.wclose()

    print("Workbooks closed, Exiting...")
