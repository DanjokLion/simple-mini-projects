import xml.sax
from xml.sax.saxutils import XMLGenerator
import xml.sax.saxutils
from lxml import etree

def format_large_xml(input_file, output_file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(input_file, parser)
    xml_string = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8')
    output_file.write(xml_string.decode('utf-8'))

list_xml = [
            "0OA_FCH_20240801_0002"
            ]

list_keyCHL = [
    "35685"
]

for i in range(len(list_xml)):
    with open(f'E:\\{list_xml[i]}.xml', 'r', encoding='utf-8') as input_file, open(f'E:\\{list_keyCHL[i]}_{list_xml[i]}.xml', 'w', encoding='utf-8') as output_file:
        format_large_xml(input_file, output_file)


