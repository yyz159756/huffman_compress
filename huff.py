import heapq
import six
# copyright@yyz159756


class CompareAble:
    """
    Define a comparable object
    Attributes:
        huffman_node: the Node class instance
    """

    def __init__(self, huffman_node):
        self.huffman_node = huffman_node

    def __cmp__(self, other):

        if self.huffman_node < other:
            return 1
        elif self.huffman_node > other:
            return -1
        else:
            return 0


class Node:
    """
    Huffman tree Node
    Attributes:
        parent: The parent of the node
        left: The left child of the node
        right: The right child of the node
        value: the value of the node
        frequency: the frequency of the value
    """

    def __init__(self, value, frequency, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value
        self.frequency = frequency

    def __lt__(self, other):
        if self.frequency < other.frequency:
            return True
        else:
            return False

    def __gt__(self, other):
        return other.__lt__(self)

    def get_value(self):
        return self.value

    def get_frequency(self):
        return self.frequency

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_root(self):
        return self.parent

    def is_leaf(self):
        if self.left is None and self.right is None:
            return True
        else:
            return False

    def to_string(self):
        print(' self.value = %s \
                self.frequency = %s\
                self.left = %s\
                self.right = %s'
              % (self.get_value(), self.get_frequency(), self.left, self.right))


def build_tree(node_list):
    """
    build a huffman tree
    :param node_list: an array with the Node class instance
    :return: the huffman tree root node
    """
    priority_queue = []

    for i in range(len(node_list)):
        heapq.heappush(priority_queue, node_list[i])

    for i in range(len(node_list) - 1):
        smallest_node1 = heapq.heappop(priority_queue)
        smallest_node2 = heapq.heappop(priority_queue)

        new_node = Node(-1, smallest_node1.frequency + smallest_node2.frequency,
                        None, smallest_node1, smallest_node2)
        smallest_node1.parent = new_node
        smallest_node2.parent = new_node
        heapq.heappush(priority_queue, new_node)

    tree_root = priority_queue[0]
    return tree_root


def traverse_huffman_tree(parent, code, char_freq):
    """
    The huffman_tree is traversed recursively to
    obtain the Huffman encoding for each character and save in the char_freq dictionary
    :param parent: The tree node
    :param code: Huffman coding
    :param char_freq: The dictionary holds the corresponding Huffman encoding for each character
    """
    if parent is None:
        return None
    # If it's a leaf, save the value to the char_freq dictionary
    if parent.is_leaf():
        char_freq[parent.get_value()] = code
        print("it = %c  and  freq = %d  code = %s" % (chr(parent.get_value()), parent.get_frequency(), code))
        return None
    else:
        # The recursion goes down into the left subtree and into the right subtree
        traverse_huffman_tree(parent.get_left(), code + '0', char_freq)
        traverse_huffman_tree(parent.get_right(), code + '1', char_freq)


def compress(input_filename, output_filename):
    """
    compress file
    :param input_filename: The address or name of the compressed file
    :param output_filename: The storage address or name of a compressed file
    """

    # 1. Open the file in binary
    f = open(input_filename, 'rb')
    file_data = f.read()
    # Get the total number of bytes of the file
    file_size = f.tell()

    # 2. Statistics the frequency of each the byte value [0-255]
    # Save in the char_freq dictionary
    char_freq = {}
    for x in range(file_size):
        # Read the XTH byte of the file, read one byte at a time
        tem = file_data[x]
        # frequency count
        if tem in char_freq.keys():
            char_freq[tem] = char_freq[tem] + 1
        else:
            char_freq[tem] = 1

    # Output the statistics
    for tem in char_freq.keys():
        print(tem, ' : ', char_freq[tem])

    # 3. construct the original Huffman coded tree array used to construct the Huffman tree
    list_huffman_trees = []
    for x in char_freq.keys():
        node = Node(x, char_freq[x])
        # Add it to the list_huffman_trees array
        list_huffman_trees.append(node)

    # 4. Write the information about the frequency of each value to the output file
    # 4.1. Write the total number of leaves into the file
    length = len(char_freq.keys())
    output = open(output_filename, 'wb')
    print('length: ', length)
    # An integer has four bytes, so divide the length into four bytes and write it to the output file
    b_str = bin(length).replace('0b', '')

    while len(b_str) < 32:
        b_str = '0' + b_str

    # write bytes to the output file
    while len(b_str) > 0:
        t_str = b_str[0:8]
        t_int = int(t_str, 2)
        output.write(six.int2byte(t_int))
        b_str = b_str[8:]

    # 4.2 Write the information about each value and the frequency of its occurrence
    # Traverse the dictionary
    for x in char_freq.keys():
        output.write(six.int2byte(x))
        # Process the frequency data
        temp = char_freq[x]
        # The frequency is type of int, divided into four bytes and written to the compressed file
        b_str = bin(temp).replace('0b', '')
        while len(b_str) < 32:
            b_str = '0' + b_str

        while len(b_str) > 0:
            t_str = b_str[0:8]
            t_int = int(t_str, 2)
            output.write(six.int2byte(t_int))
            b_str = b_str[8:]

    # 5. Construct the Huffman coding tree and retrieve the corresponding encoding for each character
    huffman_tree_root = build_tree(list_huffman_trees)
    # Traverse the Huffman tree and save the information in char_freq
    traverse_huffman_tree(huffman_tree_root, '', char_freq)
    print(char_freq)
    # 6. start to compress the file
    code = ''
    for i in range(file_size):
        # Read the XTH byte of the file
        key = file_data[i]
        # get the huffman code
        code = code + str(char_freq[key])
        # dealing with 8 bits of code at a time
        while len(code) > 8:
            # Convert binary code to decimal and save it in out variable
            b2int_code = code[0:8]
            out = int(b2int_code, 2)
            # Intercept the code after the eighth
            code = code[8:]
            # Converts the decimal out variable to a binary and write into the file
            output.write(six.int2byte(out))

    # Deal with the remaining code less than 8 bits
    # Write the last code length
    output.write(six.int2byte(len(code)))

    while len(code) < 8:
        code = code + '0'

    out = int(code, 2)
    # Converts decimal out to binary and writes it to a file
    output.write(six.int2byte(out))

    # 7. Close the output file. The file is compressed
    output.close()


def decompress(input_filename, output_filename):
    """
    Unzip file
    :param input_filename：The address or name of the compressed file
    :param output_filename：The location or name of the unzipped file
    """
    # Read the file
    f = open(input_filename, 'rb')
    file_data = f.read()
    # Get the total number of bytes of the file
    file_size = f.tell()
    # 1. Reads the number of leaves of the tree saved in the compressed file
    a1 = file_data[0]
    a2 = file_data[1]
    a3 = file_data[2]
    a4 = file_data[3]

    b_a1 = bin(a1).replace('0b', '')
    while len(b_a1) < 8:
        b_a1 = '0' + b_a1

    b_a2 = bin(a2).replace('0b', '')
    while len(b_a2) < 8:
        b_a2 = '0' + b_a2
    b_a3 = bin(a3).replace('0b', '')
    while len(b_a3) < 8:
        b_a3 = '0' + b_a3
    b_a4 = bin(a4).replace('0b', '')
    while len(b_a4) < 8:
        b_a4 = '0' + b_a4
    b_a = b_a1 + b_a2 + b_a3 + b_a4
    b = int(b_a, 2)

    leaf_node_size = b
    # 2. Read the leaf node information saved in the compressed file and record the frequency of [0-255]
    # Construct a char_freq dictionary and reconstruct the Huffman code tree again
    char_freq = {}
    for i in range(leaf_node_size):
        # Read the value of the node saved in the file
        c = file_data[4 + i * 5 + 0]

        # Read four bytes to compute the frequency to the node
        a1 = file_data[4 + i * 5 + 1]
        a2 = file_data[4 + i * 5 + 2]
        a3 = file_data[4 + i * 5 + 3]
        a4 = file_data[4 + i * 5 + 4]

        b_a1 = bin(a1).replace('0b', '')
        while len(b_a1) < 8:
            b_a1 = '0' + b_a1

        b_a2 = bin(a2).replace('0b', '')
        while len(b_a2) < 8:
            b_a2 = '0' + b_a2
        b_a3 = bin(a3).replace('0b', '')
        while len(b_a3) < 8:
            b_a3 = '0' + b_a3
        b_a4 = bin(a4).replace('0b', '')
        while len(b_a4) < 8:
            b_a4 = '0' + b_a4

        b_a = b_a1 + b_a2 + b_a3 + b_a4
        freq = int(b_a, 2)

        char_freq[c] = freq

    # 3. Reconstructing the Huffman coding tree is the same as creating the Huffman coding tree in a compressed file
    list_huffman_trees = []
    for x in char_freq.keys():
        node = Node(x, char_freq[x])
        # Add it to the list_huffman_trees array
        list_huffman_trees.append(node)

    # Construct Huffman trees
    root = build_tree(list_huffman_trees)
    # Save the Huffman encoding of all nodes in the char_freq dictionary
    traverse_huffman_tree(root, '', char_freq)
    print(char_freq)
    # 4. Extract the compressed file
    output = open(output_filename, 'wb')
    code = ''
    # The current tree node
    curr_node = root
    for x in range(leaf_node_size * 5 + 4, file_size):
        # Read one byte at a time
        c = file_data[x]

        # Process the huffman code. Converts the c(decimal) into a binary (8-bit)
        b_c = bin(c).replace('0b', '')
        while len(b_c) < 8:
            b_c = '0' + b_c
        code = code + b_c
        # The code is processed once every 24 bits
        while len(code) > 24:
            # If if the current node is a leaf
            if curr_node.is_leaf():
                # get the value
                tem_byte = six.int2byte(curr_node.get_value())
                output.write(tem_byte)
                # Back to Huffman tree roots
                curr_node = root

            # retrieve the leaf
            if code[0] == '1':
                curr_node = curr_node.get_right()
            else:
                curr_node = curr_node.get_left()
            # After processing one bit code, intercept it
            code = code[1:]

    # 4.1 Dealing with the last 24 bits
    # sub_code holds the length of the last byte
    sub_code = code[-16:-8]

    # Get the length of the last byte
    last_length = int(sub_code, 2)

    # Get the real code
    code = code[:-16] + code[-8:-8 + last_length]

    # Get the value and write to the text
    while len(code) > 0:
        if curr_node.is_leaf():
            tem_byte = six.int2byte(curr_node.get_value())
            output.write(tem_byte)
            curr_node = root

        if code[0] == '1':
            curr_node = curr_node.get_right()
        else:
            curr_node = curr_node.get_left()
        code = code[1:]

    # 5. Close the file
    output.close()


if __name__ == '__main__':
    """
    eg.
    compress('1.txt', '111')
    decompress('111', 'ttt.txt')    
    """

