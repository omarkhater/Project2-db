class Node:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []  # children are instances of Node or LeafNode
        self.is_leaf = False

    def insert_in_node(self, index, key, child):
        self.keys.insert(index, key)
        self.children.insert(index + 1, child)

    def split(self):
        mid_index = self.order // 2
        split_key = self.keys[mid_index]
        new_node = Node(self.order)
        new_node.is_leaf = self.is_leaf
        new_node.keys = self.keys[mid_index + 1:]
        new_node.children = self.children[mid_index + 1:]
        self.keys = self.keys[:mid_index]
        self.children = self.children[:mid_index + 1]
        return new_node, split_key


class LeafNode(Node):
    def __init__(self, order):
        super().__init__(order)
        self.is_leaf = True
        self.next = None  # Sequence pointer

    def insert_in_leaf(self, key, pointer):
        index = self.find_insertion_index(key)
        self.keys.insert(index, key)
        self.children.insert(index, pointer)

    def find_insertion_index(self, key):
        for i, item in enumerate(self.keys):
            if key < item:
                return i
        return len(self.keys)

    def split(self):
        mid_index = (self.order + 1) // 2  # Ceiling of n/2
        new_leaf = LeafNode(self.order)
        new_leaf.keys = self.keys[mid_index:]
        new_leaf.children = self.children[mid_index:]
        new_leaf.next = self.next
        self.keys = self.keys[:mid_index]
        self.children = self.children[:mid_index]
        self.next = new_leaf
        return new_leaf, new_leaf.keys[0]


class BTree:
    def __init__(self, order):
        self.root = LeafNode(order)
        self.order = order

    def insert(self, key, pointer):
        p, k = pointer, key
        p_prime, k_prime = self._insert(self.root, (p, k))
        
        # If the root was split, create a new root
        if p_prime:
            new_root = Node(self.order)
            new_root.keys.append(k_prime)
            new_root.children.append(self.root)
            new_root.children.append(p_prime)
            self.root = new_root

    def _insert(self, pt, pair):
        if pt.is_leaf:
            # Insert the pair in the leaf
            pt.insert_in_leaf(pair[1], pair[0])
            
            if len(pt.keys) > self.order - 1:
                # Leaf node split
                p_prime = pt.split()
                k_prime = p_prime[1]
                
                # If pt is the root, create a new root
                if pt == self.root:
                    self.root = Node(self.order)
                    self.root.keys.append(k_prime)
                    self.root.children.append(pt)
                    self.root.children.append(p_prime[0])
                return p_prime[0], k_prime
            
            return None, None
        else:
            # Insert in an internal node
            i = 0
            while i < len(pt.keys) and pair[1] >= pt.keys[i]:
                i += 1
            p_prime, k_prime = self._insert(pt.children[i], pair)
            
            if p_prime:
                if len(pt.keys) < self.order - 1:
                    pt.insert_in_node(i, k_prime, p_prime)
                    return None, None
                else:
                    pt.insert_in_node(i, k_prime, p_prime)
                    new_pt, new_k = pt.split()
                    if pt == self.root:
                        self.root = Node(self.order)
                        self.root.keys.append(new_k)
                        self.root.children.append(pt)
                        self.root.children.append(new_pt)
                    return new_pt, new_k
            return None, None


