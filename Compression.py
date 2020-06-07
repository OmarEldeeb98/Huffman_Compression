import heapq as hq
import time
from Readfile import read_file, write_data, read_file_folder, write_binary_data, read_binary_file


compress_dict = {}
decompress_dict = {}


class Node:
    def __init__(self, freq, letter=None, code=None, parent=None,
                 left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.freq = freq
        self.letter = letter
        self.code = code


class HUFFTree:
    def __init__(self, root=None):
        self.root = root


# recursively traverse the tree and generate a code for each node
def produce_code(node):
    if node is not None:
        if node.parent is None:
            node.code = ''
        elif node.parent.left == node:
            node.code = node.parent.code + '0'
        else:
            node.code = node.parent.code + '1'
        if node.letter is not None:
            compress_dict[node.letter] = node.code
            decompress_dict[node.code] = node.letter
        else:
            compress_dict['parent'] = node.code
        produce_code(node.left)
        produce_code(node.right)


# a method to get a item's key from it's value
def get_key(my_value, my_dict):
    for key, value in my_dict.items():
        if my_value == value:
            return key
    return None


# the core function of the project while the heap has more than 1 entry in it
# in normal cases it pops two frequencies of chars in the file and dictionary
# creates for each a node with appropriate data delete said letters from
# dictionary to handle if two chars with same frequency the get key function
# will get same char twice creates a parent for them pushes frequency of parent
# into the heap then goes back into the top of the loop.
# the other case is if the popped frequency is one of created parent nodes so we
# keep the parent nodes in a dictionary with keys at which iteration it was
# spawned and value its frequency and keep a list of nodes with indexes is the
# key of the dict
def build_tree(my_heap, my_dict):
    aux_nodes_index = {}
    list_aux_nodes = []
    i = 0

    while len(my_heap) > 1:
        freq1 = hq.heappop(my_heap)
        letter1 = get_key(freq1, my_dict)
        if letter1 is not None:
            del my_dict[letter1]
            node1 = Node(freq1, letter1)
        else:
            index_node1 = get_key(freq1, aux_nodes_index)
            del aux_nodes_index[index_node1]
            node1 = list_aux_nodes[index_node1]

        freq2 = hq.heappop(my_heap)
        letter2 = get_key(freq2, my_dict)

        if letter2 is not None:
            del my_dict[letter2]
            node2 = Node(freq2, letter2)
        else:
            index_node2 = get_key(freq2, aux_nodes_index)
            del aux_nodes_index[index_node2]
            node2 = list_aux_nodes[index_node2]

        parent_n = Node(node1.freq+node2.freq)
        parent_n.left = node1
        parent_n.right = node2
        node1.parent = parent_n
        node2.parent = parent_n

        hq.heappush(my_heap, freq1+freq2)
        list_aux_nodes.append(parent_n)
        aux_nodes_index[i] = freq1+freq2
        i += 1
    return HUFFTree(list_aux_nodes[i-1])


# just a function to encapsulate calls of previous functions
def compress(name):
    start = time.time()
    character_num = read_file(name)
    heap = []
    [hq.heappush(heap, x) for x in character_num.values()]
    if character_num:
        huffman = build_tree(heap, character_num)
        produce_code(huffman.root)
        print(compress_dict)
        compression_ratio = write_data(compress_dict, decompress_dict, name)
        print('The compression ratio is: ' + '{0:.2f}'.format(compression_ratio))
    else:
        print('Sorry, file is empty!')
    end = time.time()
    return end - start


def compress_folder(folder_path):
    start = time.time()
    character_num = read_file_folder(folder_path)
    heap = []
    [hq.heappush(heap, x) for x in character_num.values()]
    if character_num:
        huffman = build_tree(heap, character_num)
        produce_code(huffman.root)
        print(compress_dict)
        compression_ratio = write_data(compress_dict, decompress_dict, folder_path)
        print('The compression ratio is: ' + '{0:.2f}'.format(compression_ratio))
    else:
        print('Sorry, file is empty!')
    end = time.time()
    return end - start


def compress_binary(name):
    start = time.time()
    character_num = read_binary_file(name)
    heap = []
    [hq.heappush(heap, x) for x in character_num.values()]
    if character_num:
        huffman = build_tree(heap, character_num)
        produce_code(huffman.root)
        print(compress_dict)
        compression_ratio = write_binary_data(compress_dict)
        print('The compression ratio is: ' + '{0:.2f}'.format(compression_ratio))
    else:
        print('Sorry, file is empty!')
    end = time.time()
    return end - start
