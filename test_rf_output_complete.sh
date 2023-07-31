#!/bin/bash

{
    echo "Executing Advanced Tests: Output Shaft Complete Spin"
    
    python3 -u "./AdvancedTests/random_forest/output_shaft_complete_spin/complete_spin_1.py"

    python3 -u "./AdvancedTests/random_forest/output_shaft_complete_spin/complete_spin_2.py"

    python3 -u "./AdvancedTests/random_forest/output_shaft_complete_spin/complete_spin_1_2.py"

    python3 -u "./AdvancedTests/random_forest/output_shaft_complete_spin/complete_spin_2_1.py"
} | tee "./TestLogs/test_rf_output_complete.log"
