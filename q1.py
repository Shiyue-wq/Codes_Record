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
        newest = Node(data,None)
        if self.isEmpty():
            self.head = newest
        else:
            cur = self.head
            while cur.pointer != None:
                cur = cur.pointer
            cur.pointer = newest
        self.size += 1
        # End writing your code.


def count_node(node):
    # start writing your code.
    count = 0
    if node is None:
        return 0
    count += 1
    return count_node(node.pointer) + count
    # end writing your code.


# We will utilize the code similar to the following to check your answer.
if __name__ == '__main__':
    test_list = SinglyLinkedList()
    nums = [4,2,10,9,1,0,-1]  # An example.
    for num in nums:
        test_list.insert(num)
    first_node = test_list.head  # Get the first node of the linked list.
    print(test_list.head)
    print('The number of nodes in test_list is:')
    print(count_node(first_node))

