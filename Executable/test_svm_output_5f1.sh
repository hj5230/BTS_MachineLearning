#!/bin/bash
{
    echo "Executing Advanced Tests: Support Vector Machines Input Shaft Complete Spin"
    python3 -u "../AdvancedTests/support_vector_machines/output_shaft_complete_spin/complete_spin_1.py" 2>&1
    python3 -u "../AdvancedTests/support_vector_machines/output_shaft_complete_spin/complete_spin_2.py" 2>&1
    python3 -u "../AdvancedTests/support_vector_machines/output_shaft_complete_spin/complete_spin_1_2.py" 2>&1
    python3 -u "../AdvancedTests/support_vector_machines/output_shaft_complete_spin/complete_spin_2_1.py" 2>&1
} | tee "../TestLogs/test_svm_output_complete.log"
