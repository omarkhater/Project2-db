class Node:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []
        self.is_leaf = True

    def is_full(self):
        return len(self.keys) >= self.order - 1
    
class LeafNode(Node):
    def __init__(self, order):
        super().__init__(order)
        self.is_leaf = True
        self.next = None # Pointer to the next leaf for easy traversal

class InternalNode(Node):
    def __init__(self, order):
        super().__init__(order)
        self.is_leaf = False

class BPlusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.order = order

    def search(self, key):
        current_node = self.root
        while not current_node.is_leaf:
            i = 0
            while(i < len(current_node.keys) and key >= current_node.keys[i]):
                i+=1
            current_node = current_node.children[i]

        # At leaf level, do a simple scan
        for i, item in enumerate(current_node.keys()):
            if item == key:
                return current_node.children[i] # Return the value or record
        return None # Key not found 

    def insert(self, key, value):
        root = self.root
        if root.is_full():
            # Root is full, need to split
            new_root = InternalNode(self.order)
            # Temporarily set the root as a child of the new root
            new_root.children.append(root)
            self._split_child(new_root, root, 0)
            self.root = new_root  # Update the root
        # Perform the non-full insert operation
        self._insert_non_full(self.root, key, value)

    def delete(self, key):
        pass

    def _split_child(self, parent, child, index):
        """ Split a child node and update the parent node with a new key and child. """
        new_order = self.order
        mid_index = (new_order - 1) // 2

        if child.is_leaf:
            new_node = LeafNode(new_order)
            new_node.keys = child.keys[mid_index:]
            new_node.children = child.children[mid_index:]
            if isinstance(child, LeafNode):
                new_node.next = child.next
            # new_node.next = child.next
            child.next = new_node
            child.keys = child.keys[:mid_index+1]
            child.children = child.children[:mid_index+1]
            # Promotion of the smallest key of the new node to the parent
            if parent:
                parent.keys.insert(index, new_node.keys[0])
                parent.children.insert(index + 1, new_node)
        else:
            new_node = InternalNode(new_order)
            new_node.keys = child.keys[mid_index:]
            new_node.children = child.children[mid_index:]
            child.keys = child.keys[:mid_index+1]
            child.children = child.children[:mid_index+1]
            # Remove the middle key, as it moves up to the parent
            if parent:
                parent.keys.insert(index, child.keys[mid_index])
                parent.children.insert(index + 1, new_node)


    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            # Inserting into a leaf node
            i = 0
            while i < len(node.keys) and node.keys[i] < key:
                i+=1
            node.keys.insert(i, key)
            node.children.insert(i, value)
            if len(node.keys) > self.order - 1:
                # Node need to be split
                self._split_child(None, node, 0) # Handling root split

        else:
            # Inserting into an internal node
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i+=1

            if len(node.children[i].keys) == self.order-1:
                # Child is full, split needed
                self._split_child(node, node.children[i], i)
                if key > node.keys[i]:
                    i+=1
            self._insert_non_full(node.children[i], key, value)


    def visualize(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        G = nx.DiGraph()
        node_queue = [(self.root, None)]

        while node_queue:
            current_node, parent_id = node_queue.pop(0)
            if parent_id is None:
                node_id = "Root: " + str(current_node.keys)
            else:
                node_id = str(current_node.keys)

            G.add_node(node_id)
            
            if parent_id:
                G.add_edge(parent_id, node_id)
            
            if not current_node.is_leaf:
                for child in current_node.children:
                    node_queue.append((child, node_id))

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=5000, edge_color='gray')
        plt.show()



