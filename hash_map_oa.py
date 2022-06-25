# Name: Ryan Clark
# OSU Email:clarkr2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 06/03/22
# Description: Implements a Hash Map with Quadratic
# Probing with the following methods: put, get, remove,
# contains_key, clear, empty_buckets, resize_table,
# table_load, get_keys


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        Method accepts key value pair and adds
        them to hash map at the appropriate index.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)

        hash = self._hash_function(key)
        index = hash % self._capacity
        # Index created from hash function,
        # divided by capacity of underlying array

        if self._buckets[index] is not None:
        # Checks if index is a Hash Entry
            if self._buckets[index].key == key:
                if self._buckets[index].is_tombstone == True:
                    self._buckets.set_at_index(index, HashEntry(key, value))
                    self._size +=1
                # If key in bucket is equal to key parameter at index but it is a tombstone,
                # Hash Entry set at that index
                # and underlying size increased by 1

                else:
                    self._buckets.set_at_index(index, HashEntry(key, value))
                # if index is None, Hash Entry set at that index
                return
            else:
                index = self.quadratic_probe(key)
                if self._buckets[index] is None:
                    self._buckets.set_at_index(index, HashEntry(key, value))
                    self._size += 1
                    return
                else:
                    self._buckets.set_at_index(index, HashEntry(key, value))
                # Otherwise, if hashed index does not contain key parameter,
                # quadratic probe helper function used to find index.
                # If the value is not None, this means the key was found
                # and Hash Entry is set at that index in underlying array
                # with helper method. If index is None, Hash Entry set at that index

        if self._buckets[index] is None:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1
        # Otherwise, if initially calculated index is None, Hash Entry set at that index

    def quadratic_probe(self, key):
        """
        Helper Method takes a key parameter
        and performs a quadratic probe and returns
        the desired index if it exists in the hash table.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # Index created from hash function,
        # divided by capacity of underlying array

        org_index = index
        # Index saved as original index
        value = self._buckets[index]
        # Initialized value is set to value found at index
        counter = 1
        # counter initialized to 1 for while loop

        while value is not None:
            if self._buckets[index].key == key:
                return index
            index = (org_index + counter ** 2) % self._capacity
            value = self._buckets[index]
            counter += 1
        return index
    # While loop created to run while value is not None.
    # If index is equal to key parameter,
    # index is found and returned.
    # If key is not found at that index,
    # new index calculated based on a quadratic probe.
    # New value is calculated at that index.
    # Counter incremented by 1.
    # If value is equal to None during while loop, indexed returned

    def table_load(self) -> float:
        """
        Method returns load factor of hash table.
        """
        m = self._capacity
        # The number of buckets
        n = self._size
        # the total number of elements stored in the table
        load_fac = n / m
        return float(load_fac)
        # float of load factor returned

    def empty_buckets(self) -> int:
        """
        Method returns the amount of empty buckets in hash table.
        """
        num_buckets = 0
        # number of empty buckets initialized to 0
        counter = 0
        # counter initialized to 1 for while loop
        while counter <= self._buckets.length() - 1:
            if self._buckets[counter] is None:
                num_buckets += 1
            if self._buckets[counter] is not None:
                if self._buckets[counter].is_tombstone is True:
                    num_buckets += 1
            counter += 1
        return num_buckets
        # While loop iterates through underlying dynamic
        # array and increments bucket number when value at
        # index is None. If value is found to be not None,
        # it is a Hash Entry. If it is a Hash entry but also
        # a tombstone, bucket number is incremented.
        # The number of empty buckets is then returned.

    def resize_table(self, new_capacity: int) -> None:
        """
        Method accepts new capacity parameter and
        resizes capacity of underlying hash table.
        """
        if new_capacity < 1 or new_capacity < self._size:
            return
        # If new capacity is less than 1
        # or less than size of underlying
        # array, underlying array is not resized.

        else:
            old_table = self._buckets
            self._capacity = new_capacity
            self._buckets = DynamicArray()
            self._size = 0
            # Otherwise, underlying array saved as old table.
            # Then capacity is updated to new capacity and
            # underlying array set to empty dynamic array.
            # Underlying size set to 0

            counter = 0
            # counter initialized to 0
            while counter <= self._capacity - 1:
                self._buckets.append(None)
                counter += 1
            # Newly created empty underlying array is appended with None.
            # Iteration goes from 0 to newly assigned capacity minus 1
            counter = 0
            while counter <= old_table.length() - 1:
                if old_table[counter] is not None:
                    self.put(old_table[counter].key, old_table[counter].value)
                counter += 1
            # For each value in old table put method is used add each
            # key value pair from old table to new table. Because put method is
            # used, if value is not None, it is a Hash Entry, and  will be rehashed
            # to the appropriate index.

    def get(self, key: str) -> object:
        """
        Method accepts key parameter and returns
        value at that key.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # Index created from hash function,
        # divided by capacity of underlying array

        if self._buckets[index] is not None:
        # If value at index is not None it is a Hash Entry
            if self._buckets[index].key == key:
                if self._buckets[index].is_tombstone is False:
                    return self._buckets[index].value
            # If Hash Entry at index contains the key parameter
            # and tombstone is false, value at index returned.

            else:
                index = self.quadratic_probe(key)
            # Otherwise index is set the returned index
            # calculated from quadratic probe helper function.
                if self._buckets[index] is not None:
                    if self._buckets[index].is_tombstone is False:
                        return self._buckets[index].value
                # If the newly created index is not None, it is a Hash Entry.
                # If it is not a tombstone, that value is returned.


    def contains_key(self, key: str) -> bool:
        """
        Method accepts key parameter.
        If key is found in hash map, returns true,
        if not returns false.
        """
        if self.get(key) is not None:
            return True
        # If get method does not return None,
        # this means key is present in underlying
        # array and True is returned.
        else:
            return False
        # Otherwise, False is returned

    def remove(self, key: str) -> None:
        """
        Method accepts key parameter and
        removes key and its value if it
        exists in the hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # Index created from hash function,
        # divided by capacity of underlying array

        if self._buckets[index] is not None:
        # If value is present at index, it is a Hash Entry.
            if self._buckets[index].key == key:
                if self._buckets[index].is_tombstone is False:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                    return
            # If Hash entry object at index contains the key parameter
            # and is not a tombstone, value at index, tombstone
            # is set to True for that node and size of underlying
            # array decreased by 1

            else:
                index = self.quadratic_probe(key)
                # Otherwise, index is set the returned index
                # calculated from quadratic probe helper function.

                if self._buckets[index] is not None:
                    if self._buckets[index].is_tombstone is False:
                        self._buckets[index].is_tombstone = True
                        self._size -= 1
                # If value at index contains the key parameter it is a Hash Entry.
                # If Hash Entry is not a tombstone, tombstone
                # is set to True for that node and size of underlying
                # array decreased by 1

    def clear(self) -> None:
        """
        Method empties hash map of all key value pairs.
        """
        self._buckets = DynamicArray()
        # Underlying array set to empty dynamic array
        counter = 0
        # counter initialized to 0 for while loop
        while counter <= self._capacity - 1:
            self._buckets.append(None)
            counter += 1
        # None appended to empty array during
        # iteration sequence equal to underlying capacity, minus 1.
        self._size = 0
        # Underlying size of underlying array set to 0.


    def get_keys(self) -> DynamicArray:
        """
        Method returns all keys stored in
        Hash Map in the form of a Dynamic Array.
        """
        keys = DynamicArray()
        # Empty dynamic array created for keys to be entered into
        counter = 0
        # counter initialized to 0 for while loop

        while counter <= self._buckets.length() - 1:
            if self._buckets[counter] is not None:
                if self._buckets[counter].is_tombstone is False:
                    new_node = self._buckets[counter].key
                    keys.append(new_node)
            counter += 1
        # For length of underlying dynamic array, a while loop is created.
        # If indexed value during iteration is not None, this means it is a Hash Entry.
        # If Hash Entry is not a tombstone, its key is added to the key array.
        return keys
        # Key array returned.

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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
