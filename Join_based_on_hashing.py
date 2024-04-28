import random
import pandas as pd
import matplotlib.pyplot as plt

def generate_relation_s(num_tuples):
    """Generate a sample relation S with random values."""
    return [(random.randint(10000, 50000), random.choice(['data1', 'data2', 'data3'])) for _ in range(num_tuples)]

class StorageManager:
    def __init__(self, num_blocks, tuples_per_block):
        self.num_blocks = num_blocks
        self.tuples_per_block = tuples_per_block
        self.memory = []
        self.disk = {}
        self.io_count = 0

    def write_to_disk(self, key, data):
        # Organize data into blocks before writing to disk
        blocks = [data[i:i + self.tuples_per_block] for i in range(0, len(data), self.tuples_per_block)]
        self.disk[key] = blocks
        self.io_count += len(blocks)

    def read_from_disk(self, key):
        # Return blocks of data
        if key in self.disk:
            for block in self.disk[key]:
                yield block
                self.io_count += 1

    def clear_memory(self):
        self.memory = []

    def hash_and_partition(self, relation_key, hash_function, hash_index = 0):
        # Initialize buffers for each bucket
        buffers = {i: [] for i in range(self.num_blocks - 1)}
        for block in self.read_from_disk(relation_key):
            for record in block:
                key = record[hash_index]  
                bucket_index = hash_function(key, self.num_blocks - 1)
                # Check if buffer is full
                if len(buffers[bucket_index]) >= self.tuples_per_block:
                    self.write_to_disk(f"{relation_key}_bucket_{bucket_index}", buffers[bucket_index])
                    buffers[bucket_index] = []
                buffers[bucket_index].append(record)

        # Write remaining buffers to disk
        for index, buffer in buffers.items():
            if buffer:
                self.write_to_disk(f"{relation_key}_bucket_{index}", buffer)

    def visualize_hashing_results(self, relation_key):
        bucket_sizes = {f"{relation_key}_bucket_{i}": len(sum(self.disk.get(f"{relation_key}_bucket_{i}", []), [])) for i in range(self.num_blocks - 1)}
        plt.bar(bucket_sizes.keys(), bucket_sizes.values())
        plt.xlabel('Buckets')
        plt.ylabel('Number of Records')
        plt.title('Distribution of Records Across Hash Buckets')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Optionally print bucket sizes for more detail
        for bucket, size in bucket_sizes.items():
            print(f"{bucket}: {size} records")

def hash_function(key, num_buckets):
    return key % num_buckets


def two_pass_join(storage, join_relation={'relation_r': 1, 'relation_s':0}):
    """Implements the two-pass join using hashing with explicit block processing."""
    
    
    # First pass: Partitioning phase by reading each block, hashing, and storing hashed blocks
    for relation, hash_index in join_relation.items():
        storage.hash_and_partition(relation, 
                                   hash_function, 
                                   hash_index)

        # Visualize partitioning phase
        storage.visualize_hashing_results(relation)
    # Second pass: Join phase by reading hashed blocks and performing join
    result = []
    for i in range(storage.num_blocks - 1):
        bucket_r = storage.disk.get(f'relation_r_bucket_{i}', [])[0]
        bucket_s = storage.disk.get(f'relation_s_bucket_{i}', [])[0]
        for a, b1 in bucket_r:
            for b2, c in bucket_s:
                if b1 == b2:
                    result.append((a, b1, c))

    return result




def pandas_join(relation_r, relation_s):
    """Uses pandas to perform a natural join as a sanity check."""
    df_r = pd.DataFrame(relation_r, columns=['A', 'B'])
    df_s = pd.DataFrame(relation_s, columns=['B', 'C'])
    joined_df = pd.merge(df_r, df_s, on='B', how='inner')
    return joined_df

def sanity_check(storage, two_pass_results, relation_r, relation_s):
    """Checks the correctness of the join results and compares I/O costs."""

    # Convert two-pass join results to DataFrame for easier comparison
    two_pass_df = pd.DataFrame(two_pass_results, columns=['A', 'B', 'C'])

    # Get pandas join results for correctness verification
    pandas_results = pandas_join(relation_r, relation_s)

    # Compare the results for correctness
    correct_results = two_pass_df.equals(pandas_results.sort_values(['A', 'B', 'C']).reset_index(drop=True))
    print("Sanity Check Passed:" if correct_results else "Sanity Check Failed.")

    # Calculate theoretical I/O costs
    tuples_per_block = storage.tuples_per_block
    B_R = len(relation_r) // tuples_per_block + (1 if len(relation_r) % tuples_per_block != 0 else 0)
    B_S = len(relation_s) // tuples_per_block + (1 if len(relation_s) % tuples_per_block != 0 else 0)
    theoretical_io = 3 * (B_R + B_S)

    # Compare theoretical and actual I/O costs
    actual_io = storage.io_count
    print(f"Expected I/O Operations: {theoretical_io}")
    print(f"Actual I/O Operations: {actual_io}")

    return correct_results, theoretical_io == actual_io
