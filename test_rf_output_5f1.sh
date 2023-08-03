#!/bin/bash
{
    echo "Executing Advanced Tests: Random Forest Output Shaft Cross Validate"
    python3 -u "./AdvancedTests/random_forest/output_shaft_cross_validate/cross_5fold_1.py"
    python3 -u "./AdvancedTests/random_forest/output_shaft_cross_validate/cross_5fold_2.py"
    python3 -u "./AdvancedTests/random_forest/output_shaft_cross_validate/cross_5fold_1_2.py"
    python3 -u "./AdvancedTests/random_forest/output_shaft_cross_validate/cross_5fold_2_1.py"
} | tee "./TestLogs/test_rf_output_5f1.log"
