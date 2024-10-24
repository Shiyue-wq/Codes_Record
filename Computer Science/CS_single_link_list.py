class Node(object):
    """节点"""
    def __init__(self,elem=None):
        self.elem = elem
        self.next = None


class Link_List(object):
    """单链表"""
    def __init__(self, node):
        self.__head = node

    def __len__(self):
        length = 0
        curr = self.__head
        while curr:
            length += 1
            curr = curr.next
        return length

    def is_empty(self):
        return self.__head == None

    def travel(self):
        """遍历整个列表"""
        cur = self.__head
        while cur != None:
            print(cur)
            cur = cur.next

    def add(self,item):
        """在表头增加元素"""
        pass

    def append(self,item):
        """列表尾部添加元素"""
        node = Node(item)
        if self.is_empty():
            self.__head = node
        else:
            cur = self.head
            while cur.next != None:
                cur = cur.next
            cur.next = node

    def insert(self,pos,item):
        """指定位置插入元素"""
        pass

    def remove(self,item):
        """删除节点"""
        pass

    def search(self,item):
        """搜索节点是否存在"""
        pass



l1 = Link_List(node=None)
print(l1.__len__())

l1.append(1)
l1.append(2)
l1.append(3)
l1.append(4)
l1.travel()




