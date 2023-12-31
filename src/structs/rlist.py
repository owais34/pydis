from ..utils.util_classes import synchronized

class RListNode:
    def __init__(self, value) -> None:
        self.value = value
        self.prev = None
        self.next = None


class RList():
    def __init__(self) -> None:
        self.length = 0
        self.head = None
        self.tail = None

    @synchronized
    def push_left(self, value) -> int:
        node = RListNode(value)
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.connect(node,self.head)
            self.head=node
        self.length+=1
        return self.length
    
    @synchronized
    def push_right(self, value) -> int:
        if self.length == 0:
            return self.push_left(value)
        else:
            node = RListNode(value)
            self.connect(self.tail, node)
            self.tail = node
            self.length+=1
            return self.length
    
    def get_length(self)->int:
        return self.length
    
    @synchronized
    def pop_left(self)->any:
        if self.length==0:
            return None
        head_next = self.head.next
        self.disconnect(self.head, head_next)
        value = self.head.value
        self.head = head_next
        if self.head == None:
            self.tail = None
        self.length-=1
        return value

    @synchronized
    def pop_right(self) -> any:
        if self.length == 0:
            return None
        tail_prev = self.tail.prev
        self.disconnect(tail_prev, self.tail)
        value = self.tail.value
        self.tail = tail_prev
        if self.tail == None:
            self.head = None
        self.length-=1
        return value
    
    @synchronized
    def pos_from_left(self, value) -> int | None:
        iterator = self.head
        index = 0
        while iterator!=None:
            if iterator.value == value:
                return index
            iterator=iterator.next
            index+=1
        
        return None
    
    @synchronized
    def get_index(self, index: int):
        if(index<0):
            iterator = self.tail
            if -index>self.length:
                return None
            while(index!=-1):
                iterator=iterator.prev
                index+=1
            return iterator.value
        else:
            iterator = self.head
            if index>=self.length:
                return None
            while(index>0):
                iterator=iterator.next
                index-=1
            return iterator.value

    @synchronized   
    def range(self, start: int, end: int) -> list:
        output_list=[]
        if self.length == 0:
            return output_list
        if(start<0):
            start+=self.length
            if start<0:
                start=0
        elif start>=self.length:
            start=self.length
        if(end<0):
            end+=self.length
            if end<0:
                end=0
        elif end>=self.length:
            end=self.length-1

        escape_index = 0
        iterator = self.head
        while escape_index<start:
            iterator=iterator.next
            escape_index+=1
        while start<=end:
            output_list.append(iterator.value)
            iterator=iterator.next
            start+=1
        
        return output_list
    
    @synchronized
    def remove(self, value, count=0)->int:
        if count==0:
            count=self.length
        deleted_count = 0
        iterator = None
        if count>0:
            iterator = self.head
        else:
            iterator = self.tail

        prev_node = None
        next_node = None

        while count>0 and iterator!=None:
            prev_node = iterator.prev
            next_node = iterator.next
            if iterator.value == value:
                self.disconnect(prev_node, iterator)
                self.disconnect(iterator, next_node)
                self.connect(prev_node, next_node)
                if iterator == self.head:
                    self.head = next_node
                if iterator == self.tail:
                    self.tail = prev_node
                self.length-=1
                count-=1
                deleted_count+=1
            
            iterator = next_node
        
        while count<0 and iterator!=None:
            prev_node = iterator.prev
            next_node = iterator.next
            if iterator.value == value:
                self.disconnect(prev_node, iterator)
                self.disconnect(iterator, next_node)
                self.connect(prev_node, next_node)
                if iterator == self.head:
                    self.head = next_node
                if iterator == self.tail:
                    self.tail = prev_node
                self.length-=1
                count+=1
                deleted_count+=1
            
            iterator = prev_node
        
        return deleted_count


    def connect(self, node1: RListNode, node2: RListNode):
        if node1!=None:
            node1.next = node2
        if node2!=None:
            node2.prev = node1

    def disconnect(self, node1: RListNode, node2: RListNode):
        if node1!=None:
            node1.next=None
        if node2!=None:
            node2.prev=None