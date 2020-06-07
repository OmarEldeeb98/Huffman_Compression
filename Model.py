from Compression import compress, compress_folder, compress_binary
from Readfile import decompress, decompress_folder, decompress_binary


indication = True
exec_time = 0

while indication:
    print('=========================================================')
    print('Please pick the number of the operation\n1. Compress file')
    print('2. Decompress file\n3. Compress folder\n4. Decompress folder')
    print('5. Compress binary file\n6. Decompress binary file')
    print('7. Exit\n')
    case = input()

    if case == '1':
        name = input('Please enter file name or full path: ')
        exec_time = compress(name)
    elif case == '2':
        exec_time = decompress()
    elif case == '3':
        name = input('Please enter folder full path: ')
        exec_time = compress_folder(name)
    elif case == '4':
        exec_time = decompress_folder()
    elif case == '5':
        name = input('Please enter binary file name or full path: ')
        exec_time = compress_binary(name)
    elif case == '6':
        exec_time = decompress_binary()
    elif case == '7':
        indication = False
    else:
        print("You didn't choose one of the valid options!")

    print('The execution time is: ' + '{0:.3f}'.format(exec_time) + ' sec')
