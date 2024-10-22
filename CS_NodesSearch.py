"""
You are permitted to write code between Start and End.
Besides, you can write other extra functions or classes outside, 
but don't change the template.
"""


class Node:
    def __init__(self, element, pointer):
        self.element = element
        self.pointer = pointer


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def insert(self, data):
        # Start writing your code.
        newest = Node(data, None)
        if self.isEmpty():
            self.head = newest
        else:
            self.tail.pointer = newest
        self.tail = newest
        self.size += 1
        # End writing your code.


def QuickSort(low,high):
    if low is None or low == high:
        return
    i = low
    j = low.pointer
    while j != high:
        if j.element < low.element:
            i = i.pointer
            i.element, j.element = j.element, i.element
        j = j.pointer
    low.element, i.element = i.element, low.element
    QuickSort(low,i)
    QuickSort(i.pointer,j)
    return low


def quick_sort(node):
    # Start writing your code.
    if node is None:
        return None
    low = node
    high = getTail(node)
    node = QuickSort(low,high)
    current = node
    while current.pointer.element != 'tut':
        current = current.pointer
    current.pointer = None
    return node
    # End writing your code.


def getTail(node):
    while node.pointer is not None:
        node = node.pointer
    node.pointer = Node('tut',None)
    return node

# We will utilize the code similar to the following to check your answer.
if __name__ == '__main__':
    test_list = SinglyLinkedList()
    nums = [4,2,4,100,0,5,10]  # An example.
    for num in nums:
        test_list.insert(num)
    first_node = test_list.head  # Get the first node of the linked list.
    print('The number of nodes in test_list is:')
    p = quick_sort(first_node)
    while p.pointer != None:
        print(p.element)
        p = p.pointer
    print(p.element)
    
