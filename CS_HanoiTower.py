"""
You are permitted to write code between Start and End.
Besides, you can write other extra functions or classes outside, 
but don't change the template.
"""

class Stack:
    def __init__(self):
        self.item = []

    def isEmpty(self):
        return self.item == []

    def push(self,data):
        self.item.append(data)

    def pop(self):
        return self.item.pop()

    def peek(self):
        return self.item[0]

    def size(self):
        return len(self.item)


class Disk:
    def __init__(self,num,top,fr,aux,to):
        self.num = num
        self.top = top
        self.fr = fr
        self.aux = aux
        self.to = to

    def move(self):
        return self.fr + ' --> ' + self.to


def HanoiTower(n, from_rod ='A',aux_rod ='B',to_rod ='C'):
    result_list = []
    # Start writing your code.

    def situation(n, i, l, m, r):
        t = Disk(n, i, l, m, r)
        tasks.push(t)

    tasks = Stack()
    situation(n,1,from_rod,aux_rod,to_rod)
    while not tasks.isEmpty():
        task = tasks.pop()

        if task.num == 1:
            str = task.move()
            result_list.append(str)
        else:
            situation(task.num-1,1,task.aux,task.fr,task.to)
            situation(1,task.num,task.fr,task.aux,task.to)
            situation(task.num-1,1,task.fr,task.to,task.aux)
    # End writing your code.
    return result_list


"""
You should store each line your output in result_list defined above.
For example, if the outputs of print() are: 
                A --> C
                A --> B
then please store them in result_list:

strs = "A --> C"
result_list.append(strs)
strs = "A --> B"
result_list.append(strs)

Thus, once you want to print something, please store them in result_list immediately, 
rather than utilizing print() to print it. 
Don't miss the space! For example, don't output:
                A-->C
                A-->B

We will utilize the code similar to the following to check your answer.
"""

if __name__ == '__main__':
    n = 4
    result_list = HanoiTower(n)
    for item in result_list:
        print(item)
