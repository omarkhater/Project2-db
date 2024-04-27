class BPlusTree:
    class Node:
        def __init__(self, is_leaf=False):
            self.is_leaf = is_leaf
            self.keys = []
            self.children = []

    class LeafNode(Node):
        def __init__(self):
            super().__init__(True)
            self.next = None

    def __init__(self, order):
        self.root = None
        self.order = order

    def build_tree(self, collection, dense=True):
        for value in collection:
            self.insert(value, dense)

    def insert(self, value, dense=True):
        if not self.root:
            self.root = self.LeafNode()
        
        node = self._find_node(self.root, value)
        index = self._locate_index(node.keys, value)
        node.keys.insert(index, value)

        if len(node.keys) >= self.order:
            self._split(node, dense)

    def _find_node(self, node, value):
        while not node.is_leaf:
            for i, key in enumerate(node.keys):
                if value < key:
                    node = node.children[i]
                    break
            else:
                node = node.children[-1]
        return node

    def _locate_index(self, keys, value):
        for i, key in enumerate(keys):
            if value < key:
                return i
        return len(keys)

    def _split(self, node, dense):
        mid = self.order // 2 if dense else max(1, len(node.keys) - 1)
        new_node = self.LeafNode() if node.is_leaf else self.Node()
        new_node.keys = node.keys[mid:]
        new_node.children = node.children[mid:] if not node.is_leaf else []

        node.keys = node.keys[:mid]
        node.children = node.children[:mid] if not node.is_leaf else []

        if node == self.root:
            new_root = self.Node()
            new_root.keys = [new_node.keys[0]]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            self._insert_in_parent(node, new_node.keys[0], new_node)

    def _insert_in_parent(self, node, key, new_node):
        parent = self._find_parent(self.root, node)
        if not parent:
            self.root = self.Node()
            self.root.keys = [key]
            self.root.children = [node, new_node]
            return
        
        index = self._locate_index(parent.keys, key)
        parent.keys.insert(index, key)
        parent.children.insert(index + 1, new_node)

        if len(parent.keys) >= self.order:
            self._split(parent, True)

    def _find_parent(self, current, child):
        if current.is_leaf or not current.children:
            return None
        for i, sub_node in enumerate(current.children):
            if sub_node is child:
                return current
            if not sub_node.is_leaf:
                found = self._find_parent(sub_node, child)
                if found:
                    return found
        return None

    def search(self, key):
        node = self._find_node(self.root, key)
        return key in node.keys

    def range_search(self, key_start, key_end):
        results = []
        node = self._find_node(self.root, key_start)
        while node:
            results.extend([key for key in node.keys if key_start <= key <= key_end])
            if node.keys[-1] > key_end:
                break
            node = node.next
        return results

    def delete(self, key):
        node, _ = self._find_leaf(self.root, key)
        if key in node.keys:
            node.keys.remove(key)
            if len(node.keys) < self.order // 2 and node != self.root:
                self._handle_underflow(node)
            return True
        return False

    def _handle_underflow(self, node):
        """Handles underflow in a leaf or internal node by borrowing or merging."""
        parent = self._find_parent(self.root, node)
        if parent is None:
            return  # If there's no parent, node is the root and cannot underflow
        
        index = parent.children.index(node)
        left_sibling = parent.children[index - 1] if index > 0 else None
        right_sibling = parent.children[index + 1] if index + 1 < len(parent.children) else None

        # Try to borrow from siblings
        if left_sibling and len(left_sibling.keys) > self.order // 2:
            # Borrow the last key from the left sibling
            borrowed_key = left_sibling.keys.pop(-1)
            node.keys.insert(0, borrowed_key)
            if not node.is_leaf:
                borrowed_child = left_sibling.children.pop(-1)
                node.children.insert(0, borrowed_child)
            # Update parent's key
            parent.keys[index - 1] = node.keys[0]
        elif right_sibling and len(right_sibling.keys) > self.order // 2:
            # Borrow the first key from the right sibling
            borrowed_key = right_sibling.keys.pop(0)
            node.keys.append(borrowed_key)
            if not node.is_leaf:
                borrowed_child = right_sibling.children.pop(0)
                node.children.append(borrowed_child)
            # Update parent's key
            parent.keys[index] = right_sibling.keys[0]
        else:
            # Merge with a sibling
            if left_sibling:
                # Merge node into left_sibling
                left_sibling.keys.extend(node.keys)
                if not node.is_leaf:
                    left_sibling.children.extend(node.children)
                # Remove node from parent
                parent.keys.pop(index - 1)
                parent.children.pop(index)
            elif right_sibling:
                # Merge right_sibling into node
                node.keys.extend(right_sibling.keys)
                if not node.is_leaf:
                    node.children.extend(right_sibling.children)
                # Remove right_sibling from parent
                parent.keys.pop(index)
                parent.children.pop(index + 1)
            
            if len(parent.keys) < self.order // 2:
                self._handle_underflow(parent)

        if self.root.keys == []:
            # If the root node is empty, make its first child the new root
            if not self.root.is_leaf:
                self.root = self.root.children[0]
                self.root.parent = None

    def _find_leaf(self, node, key):
        """Helper function to find the leaf node containing the key and its parent."""
        parent = None
        while not node.is_leaf:
            parent = node
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            if i == len(node.keys):  # If key is greater than all keys in the node
                i -= 1  # Ensure we use the last available child
            node = node.children[i]
        return node, parent
    
    def display_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        if node.is_leaf:
            print('  ' * level + f"Leaf: {node.keys}")
        else:
            print('  ' * level + f"Internal: {node.keys}")
        for child in node.children:
            self.display_tree(child, level + 1)

    def display_tree_as_string(self, node=None, level=0, result=None):
        if node is None:
            node = self.root
        if result is None:
            result = []

        # Format the node description
        indent = '    ' * level
        if node.is_leaf:
            node_description = f"{indent}Leaf: {node.keys}"
        else:
            node_description = f"{indent}Internal: {node.keys}"

        # Append the node description to the result list
        result.append(node_description)

        # Recursively do this for all children (if any)
        for child in node.children:
            self.display_tree_as_string(child, level + 1, result)

        # Return the joined result if at the root level
        if level == 0:
            return '\n'.join(result)
        
    def visualize(self):
        G = nx.DiGraph()
        node_labels = {}

        def add_nodes_edges(node, graph, node_id=0):
            """ Recursive helper function to add nodes and edges to the graph. """
            if node.is_leaf:
                node_label = f"Leaf: {node.keys}"
            else:
                node_label = f"Internal: {node.keys}"

            graph.add_node(node_id, label=node_label)
            node_labels[node_id] = node_label

            child_id = node_id + 1
            for child in node.children:
                graph.add_edge(node_id, child_id)
                child_id = add_nodes_edges(child, graph, child_id)
            return child_id

        # Start recursion from the root
        add_nodes_edges(self.root, G)

        # Layout the graph
        pos = nx.multipartite_layout(G, subset_key=lambda n: (n // 10) % 3)
        nx.draw(G, pos, labels=node_labels, with_labels=True, arrows=False)
        plt.show()