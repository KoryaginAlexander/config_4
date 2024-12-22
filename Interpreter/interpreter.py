import re
from argparse import ArgumentParser
from io import UnsupportedOperation
import xml.etree.ElementTree as ET

debug = False
maxB = {
    2: 134217727,
    3: 1073741823,
    4: 1073741823
}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Файл с заданной программой')
    parser.add_argument('-o', '--output', required=True, help='Файл с результатом работы программы')
    parser.add_argument('-s', '--start', required=True, help='Начал диапазона памяти')
    parser.add_argument('-e', '--end', required=True, help='Конец диапазона памяти')
    return parser.parse_args()


def make_operation(op: list, mregister: str, memory: dict):
    global maxB
    
    new_op = [i for i in op if i != '00']
    new_op.reverse()
    ops = bin(int(''.join(new_op), 16))[2:]
    a = int(ops[-5:], 2)

    if a not in [2, 12, 3, 4]:
        raise UnsupportedOperation()

    if a == 12:
        return memory.get(mregister, '00')

    b = hex(int(ops[:-5], 2))[2:]

    if int(b, 16) < 0 or int(b, 16) > maxB[a]:
        raise ValueError('Недопустимое значение b')

    if a == 2:
        return b
    elif a == 3:
        memory[b] = mregister
        return mregister
    elif a == 4:
        operand = memory.get(b, '00')
        result = int(mregister, 16) <= int(operand, 16)
        return hex(result)[2:].rjust(2, '0')
    
    return mregister

def main():
    global debug
    args = parse_args()
    
    if debug:
        args.input = 'input.bin'
        args.output = 'output.xml'
        args.start = '0x00C9'
        args.end = '0x00CD'
        
    if not re.match(r'0x[0-9A-Fa-f]{1,4}', args.start):
        raise ValueError('Invalid memory address')

    if not re.match(r'0x[0-9A-Fa-f]{1,4}', args.end):
        raise ValueError('Invalid memory address')
        
    begin = args.start[2:].lstrip('0').lower()
    end = args.end[2:].lstrip('0').lower()
    
    if int(begin, 16) > int(end, 16):
        raise ValueError('Конец не может быть раньше начала')

    with open(args.input, 'rb') as f:
        binary_data = f.read()
        
    binary_data = list(binary_data)

    operations = []
    i = 0
    
    while i < len(binary_data):
        byte = f'{binary_data[i]:02x}'
        a = int(bin(int(byte, 16))[2:].rjust(8, '0')[-5:], 2)
        
        if a == 2:
            operation = [byte, f'{binary_data[i + 1]:02x}', f'{binary_data[i + 2]:02x}', f'{binary_data[i + 3]:02x}']
            operations.append(operation)
            i += 4  
        elif a == 12:
            operations.append([byte])
            i += 1
        elif a == 3 or a == 4:
            operation = [byte, f'{binary_data[i + 1]:02x}', f'{binary_data[i + 2]:02x}', f'{binary_data[i + 3]:02x}', f'{binary_data[i + 4]:02x}']
            operations.append(operation)
            i += 5
        else:
            i += 1

    memory = dict()
    mregister = ''

    for op in operations:
        mregister = make_operation(op, mregister, memory)

    root = ET.Element('memory')

    for i in [hex(i)[2:] for i in range(int(begin, 16), int(end, 16) + 1)]:
        sub = ET.SubElement(root, i)
        sub.text = memory.get(i, '00')

    tree = ET.ElementTree(root)
    tree.write(args.output)


if __name__ == '__main__':
    main()