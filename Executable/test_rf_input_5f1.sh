#!/bin/bash
{
    echo "Executing Advanced Tests: Random Forest Input Shaft Cross Validate"
    python3 -u "../AdvancedTests/random_forest/input_shaft_cross_validate/cross_5fold_1.py" 2>&1
    python3 -u "../AdvancedTests/random_forest/input_shaft_cross_validate/cross_5fold_2.py" 2>&1
    python3 -u "../AdvancedTests/random_forest/input_shaft_cross_validate/cross_5fold_1_2.py" 2>&1
    python3 -u "../AdvancedTests/random_forest/input_shaft_cross_validate/cross_5fold_2_1.py" 2>&1
} | tee "../TestLogs/test_rf_input_5f1_2.log"
