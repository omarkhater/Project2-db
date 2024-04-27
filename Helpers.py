import os
import random
from datetime import datetime
from B_plus_tree_refactored import BPlusTree

def generate_records(num_records, min_key, max_key):
    return random.sample(range(min_key, max_key), num_records)

def test_operations(num_records=10000, tree_orders=[13, 24], num_test_keys=100, 
                    start_record = 100000, end_record = 200000):
    # Setting up directories for logs
    base_log_dir = "logs"
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    run_log_dir = os.path.join(base_log_dir, timestamp)
    os.makedirs(run_log_dir, exist_ok=True)
    
    print("***" * 20)
    print("Starting test operations script...")
    # input("Press Enter to start testing...")

    records = generate_records(num_records, start_record, end_record)

    trees = {}
    for order in tree_orders:
        trees[f'dense_order_{order}'] = BPlusTree(order)
        trees[f'sparse_order_{order}'] = BPlusTree(order)
        trees[f'dense_order_{order}'].build_tree(records, dense=True)
        trees[f'sparse_order_{order}'].build_tree(records, dense=False)

    test_keys = random.sample(range(start_record, end_record), num_test_keys)  # Ensure there are enough keys

    for name, tree in trees.items():
        print(f"\nTesting {name}:")
        operations = ['insertion', 'deletion', 'additional operations', 'search operations']
        for operation in operations:
            # input(f"Press Enter to start {operation} on {name}...")
            operation_file_path = os.path.join(run_log_dir, f"{name}_{operation}.txt")
            with open(operation_file_path, "w") as file:
                tree.display = lambda: display_tree(tree.root, file)  # Redirect display to file
                try:
                    if 'insertion' in operation:
                        for i in range(2):
                            key = test_keys.pop()
                            file.write(f"Before insertion of {key}:\n")
                            tree.display()
                            tree.insert(key)
                            file.write(f"After insertion of {key}:\n")
                            tree.display()

                    elif 'deletion' in operation:
                        for i in range(2):
                            key = test_keys.pop()
                            file.write(f"Before deletion of {key}:\n")
                            tree.display()
                            tree.delete(key)
                            file.write(f"After deletion of {key}:\n")
                            tree.display()

                    elif 'additional operations' in operation:
                        for i in range(5):
                            key = test_keys.pop()
                            if i % 2 == 0:
                                file.write(f"Before insertion of {key}:\n")
                                tree.display()
                                tree.insert(key)
                                file.write(f"After insertion of {key}:\n")
                                tree.display()
                            else:
                                file.write(f"Before deletion of {key}:\n")
                                tree.display()
                                tree.delete(key)
                                file.write(f"After deletion of {key}:\n")
                                tree.display()

                    elif 'search operations' in operation:
                        for i in range(5):
                            key = test_keys.pop()
                            result = tree.search(key)
                            file.write(f"Search for {key}: {result}\n")
                    print(f"Success: {operation} completed and logged.")
                except Exception as e:
                    print(f"Error during {operation} on {name}: {e}")

    print("***" * 20)
    print("Test operations done successfully.")

def display_tree(node, file, level=0):
    if node.is_leaf:
        file.write('  ' * level + f"Leaf: {node.keys}\n")
    else:
        file.write('  ' * level + f"Internal: {node.keys}\n")
    for child in node.children:
        display_tree(child, file, level + 1)