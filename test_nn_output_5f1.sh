#!/bin/bash

{
    echo "Executing Advanced Tests: Neural Network Output Shaft Cross Validate"
    python3 -u "./AdvancedTests/neural_network/output_shaft_cross_validate/cross_5fold_1.py"
    python3 -u "./AdvancedTests/neural_network/output_shaft_cross_validate/cross_5fold_2.py"
    python3 -u "./AdvancedTests/neural_network/output_shaft_cross_validate/cross_5fold_1_2.py"
    python3 -u "./AdvancedTests/neural_network/output_shaft_cross_validate/cross_5fold_2_1.py"
} | tee "./TestLogs/test_nn_output_5f1.log"
