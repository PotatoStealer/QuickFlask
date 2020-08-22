class MoveHistory:
    '''
    An implementation of the so-called circular buffer. 
    Don't associate each move to a player, just [un]do it
    '''
    def __init__(self, size):
        if type(self.size) != int:
            raise TypeError("MoveHistory size must be a positive integer")
        elif self.size <= 0:
            raise ValueError("MoveHistory size must be a positive integer")
        self.size = size
        self.__data = [None] * size
        self.head = None
    
    def recentmove(self):
        pass
    
    def empty(self):
        return self.head is None

    def push(self, move):
        if self.head is None:
            self.head = 0
        else:
          self.head = (self.head + 1) % self.size
        self.__data[self.head] = move

    def pop(self):
        if self.empty():
            raise ValueError("MoveHistory is empty")
        move = self.__data[self.head]
        self.__data[self.head] = None
        if self.head == 0:
            self.head = self.size - 1
        else:
            self.head -= 1
        
        if self.__data[self.head] == None:
            self.head = None

        return move