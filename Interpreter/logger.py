import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


class Logger:
    __names = {
        2: 'loading_constant',
        12: 'reading_from_memory',
        3: 'save_to_memory',
        4: 'binary_operation'
    }
    
    def __init__(self, log_file):
        self.log_file = log_file
        
    def clear(self):
        file = open(self.log_file, 'w')
        file.close()

    def log(self, value: int, result: str):
        sub = self.__create_operation()
        sub.attrib['name'] = self.__names[int(value)]
        ET.SubElement(sub, 'A').text = str(value)
        ET.SubElement(sub, 'Result').text = result
        self.__save()
            
    def log_full(self, val_a: int, val_b: int, result: str):
        sub = self.__create_operation()
        sub.attrib['name'] = self.__names[val_a]
        ET.SubElement(sub, 'A').text = str(val_a)
        ET.SubElement(sub, 'B').text = str(val_b)
        ET.SubElement(sub, 'Result').text = result

        self.__save()
        
    def __get_root(self) -> None:
        with open(self.log_file, 'r') as f:
            text = f.read()

        if text == '':
            root = ET.Element('logs')
        else:
            root = ET.fromstring(text)

        self.__root = root
    
    def __create_operation(self) -> Element:
        self.__get_root()
        return ET.SubElement(self.__root, 'operation')
    
    def __save(self):
        tree = ET.ElementTree(self.__root)
        tree.write(self.log_file)
        