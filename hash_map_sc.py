# Name: Ryan Clark
# OSU Email:clarkr2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 06/03/22
# Description: Creates a Hash Map utilizing a chaining
# for collision resolution with the following
# methods: put,get, remove, contains_key, clear,
# empty_buckets, resize_table, table_load, get_keys,
# find_mode


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    def put(self, key: str, value: object) -> None:
        """
        Method accepts key and value parameters and
        changes that key/value pair for the Hash Table.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # index set to the hash function output
        # with key parameter, divided by length
        # of the underlying array

        if self._buckets[index].contains(key) is not None:
            self._buckets[index].contains(key).value = value
            return
        # if the underlying dynamic array contains the key, value is updated.
        else:
            self._buckets[index].insert(key, value)
            self._size += 1
        # if the underlying dynamic array does not contain the key,
        # key value pair is inserted with linked list helper function
        # and underlying size is updated.

    def empty_buckets(self) -> int:
        """
        Method returns the amount of empty
        buckets present in hash table.
        """
        bucket_num = 0
        # empty bucket number set to 0
        counter = 0
        # starting index for while loop below initialized to 0

        while counter <= self._buckets.length() - 1:
            if self._buckets[counter].length() == 0:
                bucket_num += 1
            counter += 1
        # While loop iterates through underlying dynamic
        # array and increments bucket number when length
        # of linked list value at tah index is 0

        return bucket_num
        # returns empty linked list numbers

    def table_load(self) -> float:
        """
        Method returns the load factor of the underlying
        hash table.
        """
        m = self._capacity
        # The number of buckets
        n = self._size
        # the total number of elements stored in the table
        load_fac = n/m
        # creates load factor
        return float(load_fac)
        # returns float of load factor

    def clear(self) -> None:
        """
        Method clears/empties the hash map of all values
        without changing the underlying hash table's capacity.
        """
        self._size = 0
        # underlying size set to 0 and starting index
        counter = 0
        # starting index for while loop below initialized to 0

        while counter <= self._buckets.length() - 1:
            if self._buckets[counter].length() >= 1:
                self._buckets[counter] = LinkedList()
            counter += 1
        # while loop sets linked list values to an empty linked list

    def resize_table(self, new_capacity: int) -> None:
        """
        Method accepts new capacity parameter and
        changes the capacity of the underlying hash table.
        """
        if new_capacity < 1:
            return
        # if new capacity is less than 1, table is not resized.

        old_capacity = self._capacity
        old_arr = self._buckets
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        # capacity saved as old capacity, underlying
        # array saved as old array. Then capacity is
        # updated to new capacity and underlying array
        # set to empty dynamic array.

        for i in range(new_capacity):
            self._buckets.append(LinkedList())
        # Creates dynamic array of empty linked list
        # objects that is the size of the new capacity

        self._size = 0
        # underlying dynamic array is set to 0
        for i in range(old_capacity):
            if old_arr[i].length() > 0:
                for node in old_arr[i]:
                    key = node.key
                    value = node.value
                    self.put(key, value)
        # for each value in the old dynamic array,
        # if there is a linked list present, it is
        # iterated through and key value pairs are
        # added through put method.

    def get(self, key: str) -> object:
        """
        Method accepts key parameter and returns the
        value at a particular key in the
        hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # index set to the hash function output
        # with key parameter, divided by length
        # of the underlying array

        if self._buckets[index].contains(key) is not None:
            return self._buckets[index].contains(key).value
        else:
            return
        # if index contains key, by use of the linked list helper
        # function, node is returned, else none is returned

    def contains_key(self, key: str) -> bool:
        """
        Method accepts key parameter and returns
        true if key is in Hash Map and will return
        False if it is not.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # index set to the hash function output
        # with key parameter, divided by length
        # of the underlying array

        if self._buckets[index].contains(key) is not None:
            return True
        else:
            return False
        # if index contains key, by use of the linked list helper
        # function, True is returned, else False is returned

    def remove(self, key: str) -> None:
        """
        Method accepts key parameter and removes
        that key and its value from the hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # index set to the hash function output
        # with key parameter, divided by length
        # of the underlying array

        if self._buckets[index].contains(key) is not None:
            self._buckets[index].remove(key)
            self._size -= 1
        # if index contains key, by use of the linked list helper function,
        # it is removed from the linked list with linked list remove helper
        # function and size is decreased by 1

    def get_keys(self) -> DynamicArray:
        """
        Method returns a new Dynamic Array object
        with all keys in hash map.
        """
        # find way to shorten time complexity
        keys = DynamicArray()
        # Creates empty dynamic array to add keys from hashmap.
        counter = 0
        # initializes starting index in while loop

        while counter <= self._buckets.length() - 1:
            # checks each value in dynamic array
            if self._buckets[counter].length() > 0:
                # If length is great than 0,
                # means there are linked list key/value pairs

                for node in self._buckets[counter]:
                # Iterates through linked list object
                # at that the index of the counter.

                    if node is not None:
                        keys.append(node.key)
                        # Adds all keys from linked list.
            counter += 1
            # increments the index in the while loop
        return keys
        # returns hashmap key dynamic array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Method accepts Dynamic Array object and returns
    a tuple with mode values in Dynamic Array and
    how many instances of that mode occur.
    """
    map = HashMap(da.length() // 3, hash_function_1) # creates hashmap
    mode = DynamicArray() # empty DA object
    frec = 0 # fluxuating temporary frequency value
    mode_frec = 1 # final frequency of the mode(s)
    counter = 0 #starting index for while loop
    while counter <= da.length()-1:
        # iterates through underlying dynamic array
        if map.contains_key(da[counter]):
            frec = map.get(da[counter])+1
            map.put(da[counter], map.get(da[counter])+1)
            # if hash map already has a key, its value
            # is incremented by 1 and frec/temp frequency is set equal
            # to the value incremented by 1.
            if frec == mode_frec:
                mode.append(da[counter])
                #if frec/temp frencquency equals the current
                # mode frec/mode frequency,
                # the mode array has that key appended to it.
            if frec > mode_frec:
                mode_frec = frec
                # if temp frequency surpasses mode frequency,
                # mode frequency is set to temp frequency
                if mode.length() > 0:
                    mode = DynamicArray()
                mode.append(da[counter])
                # Empties mode array if mode frequency is updated to larger value
                # and appends mode frequency with key
        else:
            map.put(da[counter], 1)
        counter += 1
        # otherwise, if key is not in the hashmap,
        # it is added to the hash map with a value of 1
    if mode_frec == 1:
        mode = da
    # if mode frequnecy by the end of the while loop is 1,
    # mode is equal to the dynamic array parameter
    return tuple((mode, mode_frec))
    # tuple of mode dynamic array and mode frequnecy returned

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "grape", "melon", "melon", "peach", "apple"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
