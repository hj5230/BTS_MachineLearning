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


if __name__ == "__main":
    # Specifies the range of the predicting dataset
    ranger = Ranger(end=204800, length=204800)

    print("Loading workbooks of 1st machine...\n")

    # Load three workbooks with data from the first worm reducer
    workbooks_of_1st_machine = WBS(
        "sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1"
    )

    print("Workbooks of 1st machine successfully loaded, Now training model...\n")

    # Train the model with "RandormForest" constructor
    model = RandomForest(
        SensorData(workbooks_of_1st_machine, "1"),
        SensorData(workbooks_of_1st_machine, "3"),
        SensorData(workbooks_of_1st_machine, "9"),
        SensorData(workbooks_of_1st_machine, "13"),
        SensorData(workbooks_of_1st_machine, "15"),
    )

    print("Loading workbooks of 2nd machine...\n")

    # Load three workbooks with data from the second worm reducer
    workbooks_of_2nd_machine = WBS(
        "sDataF_P1XYZ_0208_1", "sDataF_P2XYZ_0208_1", "sDataF_P3XYZ_0208_1"
    )

    print("Workbooks of 2nd machine successfully loaded, Now paragraphing...\n")

    # Divide dataset into a training part and a prediction part
    state_normal_test, _ = Utils.paragraphing(
        SensorData(workbooks_of_2nd_machine, "1"), ranger
    )
    state_off_output_test, _ = Utils.paragraphing(
        SensorData(workbooks_of_2nd_machine, "3"), ranger
    )
    state_turbo_jump_test, _ = Utils.paragraphing(
        SensorData(workbooks_of_2nd_machine, "9"), ranger
    )
    state_bearing_scratch_test, _ = Utils.paragraphing(
        SensorData(workbooks_of_2nd_machine, "13"), ranger
    )
    state_turbine_scratch_test, _ = Utils.paragraphing(
        SensorData(workbooks_of_2nd_machine, "15"), ranger
    )

    print("Paragraphing completed, Now predicting state...\n")

    # Predict with trained model and print the prediction result
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

    # Close workbooks
    workbooks_of_1st_machine.wclose()

    print("Workbooks closed, Exiting...")
