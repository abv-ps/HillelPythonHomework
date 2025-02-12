import xml.etree.ElementTree as ET

root = ET.Element('books')

book_1 = ET.SubElement(root, 'book_1')
ET.SubElement(book_1, 'title').text = 'The Hobbit'
ET.SubElement(book_1, 'description').text = 'Some description'

book_2 = ET.SubElement(root, 'book_2')
ET.SubElement(book_1, 'title').text = 'LOTR'
ET.SubElement(book_1, 'description').text = 'Some description 2'

tree = ET.ElementTree(root)
tree.write('books.xml')

tree = ET.parse('../books.xml')
root = tree.getroot()
