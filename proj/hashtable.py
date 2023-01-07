from collections.abc import MutableMapping


class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):

        """
        Constructor for Markov class

        Parameters: 
        capacity: number of cells to initialize
        default_value: int value to return if key not in table
        load_factor: max capacity of table in percentage terms before rehashing
        growth_factor: factor to grow cells by when rehashing

        additional attributes:
        self.counts: tracks number of tuples inserted in table. Allows for O(1) check of whether table needs to be rehashed.
        Reset to 0 on every rehashing
        """


        self.capacity = capacity
        self._items = [(None, None, None)] * capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self.length = 0
        
        # self.counts keeps track of entries into the hastable. This makes it easy to check
        # whether the table should be rehashed (vs. traversing list every time)
        self.counts = 0

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value
        between 0 and self.capacity.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val % self.capacity

    def __setitem__(self, key, val):
        """
        setter function for linear probing hastable. If empty cell is found at hashed index, new tuple of (key, val, True)
        is created. Otherwise, function "walks" the table until next empty cell is found. After insertion, self.counts is
        incremented and rehash is called.

        parameters:
        key: key to be stored in table
        value: value to be associated with key
        """

        index = self._hash(key)

        if self._items[index][0] == None:
            self._items[index] = (key, val, True)
            self.counts += 1
            self.length +=1
        elif self._items[index][0] == key:
            self._items[index] = (key, val, True)
        else:
            for i in range(1, self.capacity):

                #creating position variable for concision
                position = (index + i) % self.capacity

                if self._items[position][0] == None:
                    self._items[position] = (key, val, True)
                    self.counts += 1
                    self.length +=1
                    break
                elif self._items[position][0] == key:
                    self._items[position] = (key, val, True)
                    break
       
       # increment self.counts every time a tuple is inserted
        
        # check whether rehash needs to occur after every insertion
        self.rehash()


    def __getitem__(self, key):
        """
        Getter function for linear probing hashtable.Logic:
        
            - If item found at hashed index and not logically deleted -> return value
            - If no tuple at hashed index -> return default value
            - Otherwise, linearly probe table:
                - If key is found (and present in table) -> return value
                - If empty cell -> return default value

        parameters:
        key: key to search for in table
        """
        index = self._hash(key)

        if self._items[index][0] == key and self._items[index][2]:
            return self._items[index][1]
        elif self._items[index][0] == None:
            return self.default_value
        else:
            for i in range(1, self.capacity):

                #position variable for concision
                position = (index + i) % self.capacity

                if self._items[position][0] == None:
                    return self.default_value
                elif self._items[position][0] == key and self._items[position][2]:
                    return self._items[position][1]
        
            
        

    def __delitem__(self, key):
        """
        Logical delete function for linear probing hashtable. If the key is in the table and logically present, the key
        is marked as logically deleted. Otherwise, if the key is not logically present or not present at all, raises keyError.

        parameters:
        key: key to delete
        
        """
        index = self._hash(key)

        if self._items[index][0] == key and self._items[index][2]:
            self._items[index] = (self._items[index][0], self._items[index][1], False)
            self.length -= 1
            return
        elif self._items[index][0] == key and not self._items[index][2]:
            raise KeyError(key)
        else:
            for i in range(1, self.capacity):

                #positon variable for concision
                position = (index + i) % self.capacity
                
                if self._items[position][0] == key and self._items[position][2]:
                    self._items[position] = (self._items[position][0], self._items[position][1], False)
                    self.length -=1
                    return
            raise KeyError(key)



    def __len__(self):
        """
        length overload for hashtable. Only counts entries that are logically present in the table.
        """
        # count = 0
        # for elem in self._items:
        #     if elem[2]:
        #         count += 1
        return self.length
    
    def rehash(self):
        """
        Rehashing function for linear probing hashtable.

        Checks if the number of entries (both logicall present and deleted) have exceeded the load factor. If so,
        assigns self._items to a "temp" label, creates a new list for self._items of length self.capacity * self.growth_factor,
        and copies in entries that are logically present in the table.

        """
        #check entries against load factor
        if self.counts >= self.capacity * self.load_factor:
            self.capacity = self.capacity * self.growth_factor
            temp_list = self._items
            self.length = 0
            #point self._items at a new list
            self._items = [(None, None, None)] * self.capacity
            
            #reset self.counts - __setitem__ function will increment as entries are added
            self.counts = 0
            for elem in temp_list:
                if elem[2]:
                    self.__setitem__(elem[0], elem[1])
    
    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")

