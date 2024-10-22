"""
单链表
1、计算长度操作
2、判断是否为空链表
3、头插法
4、尾插法
5、根据位置插入值
6、遍历链表
7、清空链表
8、根据位置删除链表值
9、根据值删除
10、链表逆序遍历
"""
class Node(object):
    def __init__(self, value = None):
        self.value = value
        self.next = None

class LinkList(object):
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

    def add(self, value):
        if value:
            node = Node(value)
            node.next = self.__head
            self.__head = node

    def append(self, value):
        if value:    #判断附加的值是否为空
            node = Node(value)
            curr = self.__head
            if curr:    #判断头部是否为空
                while curr.next:    #当一个节点的下一位不为空，则持续循环
                    curr = curr.next
                curr.next = node
            else:
                self.__head = node

    def insert(self, pos, value):
        if pos <= 0:
            self.add(value)
        elif pos > self.__len__() - 1:
            self.append(value)
        else:
            node = Node(value)
            i = 0
            curr = self.__head
            while curr:
                if i == pos - 1:
                    break
                curr = curr.next
                i += 1
            node.next = curr.next
            curr.next = node

    def trval(self):
        curr = self.__head
        while curr.next:
            print(curr.value, end=" ")
            curr = curr.next
        print(curr.value, end=" ")
        print("\n")

    def clear(self):
        self.__head = None

    def remove(self, pos):
        if pos < 0:
            raise Exception("删除位置异常，必须大于等于0")
        elif pos > self.__len__() - 1:
            raise Exception("此位置无数据，请输入【0,%s】之间的数" % (self.__len__() - 1))
        else:
            curr = self.__head
            if pos == 0: #头节点
                print("删除节点的值为:%s,位置为:%s" % (self.__head.value, pos))
                self.__head = self.__head.next
            else:
                i = 0
                while curr.next:
                    if i == pos - 1: #尾节点/中间节点
                        break
                    curr = curr.next
                    i += 1
                remove_node = curr.next
                print("删除节点的值为:%s,位置为:%s" % (remove_node.value, pos))
                curr.next = curr.next.next

    def remova_value(self, value):
        """
        删除值
        :param value:
        :return:
        """
        curr = self.__head
        if curr is None:
            raise Exception("链表为空，无法删除值")
        i = 0
        while curr:
            if curr.value == value:
                break
            curr = curr.next
            i += 1
        prior = self.__head
        j = 0
        while prior.next:
            if j == i - 1:
                break
            prior = prior.next
            j += 1
        if i == 0:
            self.__head = self.__head.next
        elif i > self.__len__() - 1:
            raise Exception("未查询到此数据")
        elif 0 < i < self.__len__() - 1:
            prior.next = prior.next.next
        else:
            pass
        print("删除的值为:%s 位置为:%s" % (value, i))

    def rever(self):
        """
        逆序遍历
        :return:
        """

        def foo(node):
            if node is None:
                return
            curr = node.next
            foo(curr)
            print(node.value, end=",")

        return foo(self.__head)


if __name__ == '__main__':
    L = LinkList(node=None)
    print(L.__len__())
    L.append(13)
    L.append(14)
    L.trval()
    L.append(15)
    L.add(6)
    L.append(16)
    L.insert(10, 8)
    L.insert(3, 10)
    L.remove(4)
    L.remova_value(10)
    L.trval()
    L.rever()