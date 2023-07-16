#!/bin/bash

{
    echo "Executing Advanced Tests: Output Shaft Cross Validate"
    
    python3 -u "./AdvancedTests/output_shaft_cross_validate/cross_5fold_1.py"

    python3 -u "./AdvancedTests/output_shaft_cross_validate/ross_5fold_2.py"

    python3 -u "./AdvancedTests/output_shaft_cross_validate/cross_5fold_1_2.py"

    python3 -u "./AdvancedTests/output_shaft_cross_validate/cross_5fold_2_1.py"
} | tee "./TestLogs/complete_spin.log"
