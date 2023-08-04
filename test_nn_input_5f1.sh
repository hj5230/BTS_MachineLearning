#!/bin/bash
{
    echo "Executing Advanced Tests: Neural Network Input Shaft Cross Validate"
    python3 -u "./AdvancedTests/neural_network/input_shaft_cross_validate/cross_5fold_1.py" 2>&1
    python3 -u "./AdvancedTests/neural_network/input_shaft_cross_validate/cross_5fold_2.py" 2>&1
    python3 -u "./AdvancedTests/neural_network/input_shaft_cross_validate/cross_5fold_1_2.py" 2>&1
    python3 -u "./AdvancedTests/neural_network/input_shaft_cross_validate/cross_5fold_2_1.py" 2>&1
} | tee "./TestLogs/test_nn_input_5f1.log"
