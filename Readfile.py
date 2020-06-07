from string import printable
import collections
import array
import os
import glob
import time

letters = []
compressed_data = array.array('B')
dictionary = array.array('B')
file_byte = array.array('B')
compressed_data_dict = array.array('B')


# read each character, count it and put the character and the count in dict
def read_file(name):
    if os.stat(name).st_size != 0:
        character_num = collections.Counter()
        with open(name, 'r+') as file:
            for line in file:
                for letter in line.lower():
                    if letter in printable:
                        letters.append(letter)
                        character_num.update(letter)
        return character_num
    else:
        return False


def read_file_folder(folder_path):
    assert os.path.exists(folder_path), "Folder is not found" + folder_path
    files_string = ""
    if os.stat(folder_path).st_size != 0:
        for filename in glob.glob(os.path.join(folder_path, '*.txt')):
            with open(filename, "r") as file:
                files_string += file.read() + "end of file"
        strx = files_string.split("end of file")
        print(strx)
        character_num = collections.Counter()
        # with open(name, 'r+') as file:
        for line in files_string:
            for letter in line.lower():
                if letter in printable:
                    letters.append(letter)
                    character_num.update(letter)
        return character_num
    else:
        return False


def read_binary_file(name):
    if os.stat(name).st_size != 0:
        character_num = collections.Counter()
        with open(name, 'rb') as file:
            byte = file.read(1)
            file_byte.append(int.from_bytes(byte, "big"))
            while byte:
                character_num.update(byte)
                byte = file.read(1)
                file_byte.append(int.from_bytes(byte, "big"))
        return character_num
    else:
        return False


# get code of each letter and concatenate it with the sting concatenated add
# zeros to the end of the string to make it multiple of eight, read the file
# byte by byte convert them to integers then write them to the binary file
def write_data(compress_dict, decompress_dict, name):
    decompress_dictionary = {}
    for i in decompress_dict.keys():
        temp = decompress_dict.get(i)
        letter_ascii = ord(temp)
        decompress_dictionary[i] = str(letter_ascii)
    coded_dict = ""
    for i in decompress_dict.keys():
        coded_dict += i + ":" + decompress_dictionary.get(i) + ","
    coded_dict = coded_dict[:-1]
    coded_dict = coded_dict+"\n"
    dictionary.frombytes(coded_dict.encode())
    concatenated = ''
    for letter in letters:
        if letter in printable:
            code = compress_dict.get(letter)
            concatenated += str(code)

    extra_padding = 8 - len(concatenated) % 8
    parent_code = compress_dict.get('parent')
    for i in range(extra_padding):
        j = 0
        if j > len(parent_code):
            j = 0
        concatenated += parent_code[j]
        j += 1

    for i in range(0, (len(concatenated)), 8):
        compressed_data.append(int(concatenated[i:i+8], 2))

    with open("compressed.bin", "wb") as out:
        out.write(bytes(dictionary))
        out.write(bytes(compressed_data))

    if '.txt' in name:
        compression_ratio = os.path.getsize(name) / os.path.getsize("compressed.bin")
    else:
        total_size = 0
        for dirpath, dirname, filename in os.walk(name):
            for f in filename:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        compression_ratio = total_size/os.path.getsize("compressed.bin")
    return compression_ratio


def write_binary_data(compress_dict):
    concatenated = ''
    decompress_binary_dictionary = {}
    for i in compress_dict.keys():
        if i is 'parent':
            continue
        temp = compress_dict.get(i)
        decompress_binary_dictionary[temp] = i
    coded_binary_dict = ""
    for i in decompress_binary_dictionary:
        coded_binary_dict += i + ":" + str(decompress_binary_dictionary.get(i)) + ","
    coded_binary_dict = coded_binary_dict[:-1]
    coded_binary_dict = coded_binary_dict+"\n"
    compressed_data_dict.frombytes(coded_binary_dict.encode())
    for byte in file_byte:
        code = compress_dict.get(byte)
        concatenated += str(code)

    extra_padding = 8 - len(concatenated) % 8
    parent_code = compress_dict.get('parent')
    for i in range(extra_padding):
        j = 0
        if j > len(parent_code):
            j = 0
        concatenated += parent_code[j]
        j += 1

    for i in range(0, (len(concatenated)), 8):
        compressed_data.append(int(concatenated[i:i+8], 2))
    compression_ratio = len(file_byte) / len(compressed_data)
    with open("compressed.bin", "wb") as out:
        out.write(bytes(compressed_data_dict))
        out.write(bytes(compressed_data))
    return compression_ratio


# read the file byte by byte convert them to binary then string read the string
# character by character and check it's a code if it is add the letter and flush
# the seek variable to begin reading code from that point then write that
# decoded string.
def decompress():
    start = time.time()
    decompress_dictionary = {}
    concatenated = ''
    decoded = ''
    seek = ''
    if os.stat('compressed.bin').st_size != 0:
        with open('compressed.bin', 'rb') as file:
            file.seek(0)
            dict_string = file.readline()
            code = file.read()
        dict_string = dict_string.decode()
        parts = dict_string.split(',')
        for k in range(len(parts)):
            dict_element = parts[k].split(":")
            decompress_dictionary[dict_element[0]] = chr(int(dict_element[1]))

        for byte in code:
            concatenated += str("{0:08b}".format(byte))

        for i in range(0, len(concatenated)):
            if concatenated[i] == '0' or concatenated[i] == '1':
                seek += concatenated[i]
                letter = decompress_dictionary.get(seek)
                if letter:
                    decoded += letter
                    seek = ''

        with open('decompressed.txt', "w") as out:
            out.write(decoded)
    else:
        print('Sorry, compressed file is empty!')
    end = time.time()
    return end - start


def decompress_folder():
    start = time.time()
    decompress_dictionary = {}
    concatenated = ''
    decoded = ''
    seek = ''
    if os.stat('compressed.bin').st_size != 0:
        with open('compressed.bin', 'rb') as file:
            file.seek(0)
            dict_string = file.readline()
            code = file.read()
        dict_string = dict_string.decode()
        parts = dict_string.split(',')
        for k in range(len(parts)):
            dict_element = parts[k].split(":")
            decompress_dictionary[dict_element[0]] = chr(int(dict_element[1]))

        for byte in code:
            concatenated += str("{0:08b}".format(byte))

        for i in range(0, len(concatenated)):
            if concatenated[i] == '0' or concatenated[i] == '1':
                seek += concatenated[i]
                letter = decompress_dictionary.get(seek)
                if letter:
                    decoded += letter
                    seek = ''
        decoded = decoded.split("end of file")
        decoded = decoded[:-1]
        for i in range(len(decoded)):
            file_name = "decompresses"+str(i)+".txt"
            with open(file_name, "w") as out:
                out.write(decoded[i])
    else:
        print('Sorry, compressed file is empty!')
    end = time.time()
    return end - start


def decompress_binary():
    start = time.time()
    concatenated = ''
    seek = ''
    decompressed_data = array.array('B')
    decompress_dict = {}
    if os.stat('compressed.bin').st_size != 0:
        with open('compressed.bin', 'rb') as file:
            file.seek(0)
            dict_string = file.readline()
            code = file.read()
        dict_string = dict_string.decode()
        parts = dict_string.split(',')
        for k in range(len(parts)):
            dict_element = parts[k].split(":")
            decompress_dict[dict_element[0]] = int(dict_element[1])

        for byte in code:
            concatenated += str("{0:08b}".format(byte))

        for i in range(0, len(concatenated)):
            if concatenated[i] == '0' or concatenated[i] == '1':
                seek += concatenated[i]
                byte = decompress_dict.get(seek)
                if byte is not None:
                    decompressed_data.append(byte)
                    seek = ''

        with open('decompressed.bin', "wb") as out:
            out.write(bytes(decompressed_data))
    else:
        print('Sorry, compressed file is empty!')
    end = time.time()
    return end - start
