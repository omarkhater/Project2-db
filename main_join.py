import os
import random
from datetime import datetime
import pandas as pd
from Join_based_on_hashing import StorageManager, two_pass_join, generate_relation_s, sanity_check

def run_experiment(num_tuples, value_range=None, experiment_name=""):
    """Runs a join experiment with specified parameters, logs results, and includes sanity checks."""
    storage = StorageManager(num_blocks=15, tuples_per_block=8)
    relation_s = generate_relation_s(5000)
    storage.write_to_disk('relation_s', relation_s)

    if value_range:
        relation_r = [(random.choice(['info1', 'info2', 'info3']), random.randint(*value_range)) for _ in range(num_tuples)]
    else:
        relation_r = [(random.choice(['info1', 'info2', 'info3']), b) for b, c in random.sample(relation_s, num_tuples)]
    storage.write_to_disk('relation_r', relation_r)

    base_log_dir = "logs_join_hashing"
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    run_log_dir = os.path.join(base_log_dir, timestamp, experiment_name)
    os.makedirs(run_log_dir, exist_ok=True)

    join_log_path = os.path.join(run_log_dir, "join_experiment_log.txt")
    with open(join_log_path, "w") as log_file:
        log_file.write("Join Experiment Results\n")
        log_file.write("=======================================\n")

        join_result = two_pass_join(storage, join_relation={'relation_r':1, 'relation_s': 0})
        log_file.write(f"Total results: {len(join_result)}\n")

        for result in join_result:
            log_file.write(f"{result}\n")

        is_correct = sanity_check(storage, join_result, relation_r, relation_s)
        log_file.write(f"Sanity check passed: {'Yes' if is_correct else 'No'}\n")
        log_file.write(f"Disk I/O count: {storage.io_count}\n")

    print(f"{experiment_name} completed successfully. Disk I/O count: {storage.io_count}")