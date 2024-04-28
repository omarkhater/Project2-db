# B+ Tree and Hashing-Based Join Algorithms

## Overview
This repository implements two critical data structures and algorithms used extensively in database operations: B+ trees and a two-pass hashing-based join algorithm. These implementations are essential for understanding and optimizing data retrieval and join operations in database systems.

## Structure
- `B_plus_tree_refactored.py`: Implements B+ trees with functionalities like insertion, deletion, search, and visualization.
- `Join_based_on_hashing.py`: Implements a two-pass join algorithm using virtual memory and disk simulation for efficient data handling.
- `main_join.py`: Main script to run join experiments, recording performance metrics and results.
- `Helpers.py`: Auxiliary functions supporting B+ tree and join algorithm operations.
- `requirements.txt`: Dependencies required to run the modules.

## Testing
- `Test_B_trees_refactored.ipynb`: Test notebook for B+ trees, demonstrating various operations and their effects.
- `Test_join_based_on_hashing.ipynb`: Test notebook for the hashing-based join algorithm, showcasing the algorithm's execution and efficiency.

## Installation
Clone this repository and install required dependencies:
```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
pip install -r requirements.txt
```

## Usage
Run the test notebooks to perform experiments and see the algorithms in action. Each test execution will generate logs in a new timestamped directory, allowing for performance tracking and detailed analysis of operations.

## Contributing
Feel free to fork the repository, make improvements, or tailor the algorithms to specific needs. Pull requests and improvements are welcome.

## License
This project is copywrighted. See the LICENSE file for more details
