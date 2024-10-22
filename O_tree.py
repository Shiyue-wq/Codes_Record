class Node:

    def __init__(self, element, parent=None, left=None, right=None):
        self.element = element
        self.parent = parent
        self.left = left
        self.right = right


class LBTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def find_root(self):
        return self.root

    def parent(self, p):
        return p.parent

    def left(self, p):
        return p.left

    def right(self, p):
        return p.right

    def num_child(self, p):
        count = 0
        if p.left is not None:
            count += 1
        if p.right is not None:
            count += 1
        return count

    def add_root(self, e):
        if self.root is not None:
            print('Root already exists.')
            return None
        self.size = 1
        self.root = Node(e)
        return self.root

    def add_left(self, p, e):
        if p.left is not None:
            print('Left child already exists.')
            return None
        self.size += 1
        p.left = Node(e, p)
        return p.left

    def add_right(self, p, e):
        if p.right is not None:
            print('Right child already exists.')
            return None
        self.size += 1
        p.right = Node(e, p)
        return p.right

    def replace(self, p, e):
        old = p.element
        p.element = e
        return old

    def delete(self, p):
        old = p.parent
        if p.parent.left is p:
            p.parent.left = None
        if p.parent.right is p:
            p.parent.right = None
        return old

    def DFSearch(self,t):
        if t:
            print(t.element)
        if (t.left is None) and (t.right is None):
            return
        else:
            if t.left is not None:
                self.DFSearch(t.left)
            if t.right is not None:
                self.DFSearch(t.right)

if __name__ == '__main__':
    t = LBTree()
    t.add_root(1)
    t.add_left(t.root,2)
    t.add_left(t.root.left,3)
    t.add_right(t.root.left,5)
    t.add_left(t.root.left.left,4)
    t.add_left(t.root.left.right,6)
    t.DFSearch(t.root)



