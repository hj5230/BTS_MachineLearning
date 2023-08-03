#!/bin/bash

{
    echo "Executing Advanced Tests: Gradient Boosting Output Shaft Cross Validate"
    python3 -u "./AdvancedTests/gradient_boosting/output_shaft_cross_validate/cross_5fold_1.py"
    python3 -u "./AdvancedTests/gradient_boosting/output_shaft_cross_validate/cross_5fold_2.py"
    python3 -u "./AdvancedTests/gradient_boosting/output_shaft_cross_validate/cross_5fold_1_2.py"
    python3 -u "./AdvancedTests/gradient_boosting/output_shaft_cross_validate/cross_5fold_2_1.py"
} | tee "./TestLogs/test_gb_output_5f1.log"
