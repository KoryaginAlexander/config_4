from argparse import ArgumentParser
from logger import Logger
import re


debug = False
maxB = {
    2: 134217727,
    3: 1073741823,
    4: 1073741823
}
opLen = {
    2: 27,
    3: 35,
    4: 35
}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Файл с заданной программой')
    parser.add_argument('-o', '--output', required=True, help='Файл с результатом работы программы')
    parser.add_argument('-l', '--log', required=True, help='Файл с логами работы программы')
    return parser.parse_args()


def is_operation(op: str):
    return re.match(r'^((LOAD)\s+(\d+)|(READ)|(WRITE)\s+(\d+)|(LEQ)\s+(\d+))$', op)


def translate_operation(op: str, logger: Logger) -> str:
    global maxB
    global opLen
    
    if not is_operation(op):
        raise ValueError('Непонятная операция')

    a = 0
    b = -1

    match = re.match(r'^LOAD\s+(\d+)$', op)
    
    if match:
        a = 2
        b = int(match.group(1))

    match = re.match(r'^READ$', op)

    if match:
        a = 12

    match = re.match(r'^WRITE\s+(\d+)$', op)

    if match:
        a = 3
        b = int(match.group(1))

    match = re.match(r'^LEQ\s+(\d+)$', op)

    if match:
        a = 4
        b = int(match.group(1))
        
        

    if a not in [2, 12, 3, 4]:
        raise ValueError('Нет такой операции')

    if a == 12:
        logger.log(12, '0x0c')
        return '0x0c'

    if b < 0 or b > maxB[a]:
        raise ValueError('Недопустимое значение b')

    operation = bin(b)[2:].rjust(opLen[a], '0') + bin(a)[2:].rjust(5, '0')
    operation = hex(int(operation, 2))[2:].rjust((opLen[a] + 5) // 4, '0')
    ops = ['0x' + operation[i] + operation[i + 1] for i in range(0, len(operation), 2)]
    ops.reverse()
    logger.log_full(a, b, ', '.join(ops))
    return ','.join(ops)


def main():
    global debug
    
    args = parse_args()
    
    if debug:
        args.input = 'example.ass'
        args.output = 'input.bin'
        args.log = 'logs.xml'

    logger = Logger(args.log)
    logger.clear()

    with open(args.input, 'r') as f:
        program = f.read()
        
    program = program.split('\n')
    program = [re.sub(r'/s', '', i) for i in program]
    
    i = 0
    
    while i < len(program):
        if program[i].lstrip().startswith('//') or program[i].strip() == '':
            program.pop(i)
            continue
            
        i += 1
        
    result = []
    
    for i in program:
        result.append(translate_operation(i, logger))

    with open(args.output, 'wb') as f:
        for hex_string in result:
            bytes_data = bytes(int(x, 16) for x in hex_string.split(','))
            f.write(bytes_data)


if __name__ == '__main__':
    main()
