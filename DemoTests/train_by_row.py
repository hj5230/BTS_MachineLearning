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


if __name__ == "__main__":
    # Specifies the range of the predicting dataset
    ranger = Ranger(start=0, length=512)

    print("Loading workbooks...\n")

    # Load three workbooks with data from the worm reducer
    workbooks_of_1st_machine = WBS(
        "sDataF_P1XYZ_0222_1", "sDataF_P2XYZ_0222_1", "sDataF_P3XYZ_0222_1"
    )

    print("Workbooks successfully loaded, Now paragraphing...\n")

    # Divide dataset into a training part and a prediction part
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

    # Train the model with "RandormForest" constructor
    model = RandomForest(
        state_normal_train,
        state_off_output_train,
        state_turbo_jump_train,
        state_bearing_scratch_train,
        state_turbine_scratch_train,
    )

    print("Model training completed, Now predicting state...\n")

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
