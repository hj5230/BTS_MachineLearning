#!/bin/bash
{
    echo "Executing Advanced Tests: Support Vector Machines Output Shaft Complete Spin"
    python3 -u "./AdvancedTests/support_vector_machines/output_shaft_cross_validate/cross_5fold_1.py" 2>&1
    python3 -u "./AdvancedTests/support_vector_machines/output_shaft_cross_validate/cross_5fold_2.py" 2>&1
    python3 -u "./AdvancedTests/support_vector_machines/output_shaft_cross_validate/cross_5fold_1_2.py" 2>&1
    python3 -u "./AdvancedTests/support_vector_machines/output_shaft_cross_validate/cross_5fold_2_1.py" 2>&1
} | tee "./TestLogs/test_svm_output_complete.log"
