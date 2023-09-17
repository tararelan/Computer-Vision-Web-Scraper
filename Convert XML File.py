import pandas as pd
import xml.etree.ElementTree as ET

df = pd.read_excel('')  # Add filepath

root = ET.Element('annotations')

for index, row in df.iterrows():
    image_elem = ET.SubElement(root, 'image')

    ET.SubElement(image_elem, 'filename').text = str(row['filename'])
    size_elem = ET.SubElement(image_elem, 'size')
    ET.SubElement(size_elem, 'height').text = str(row['height'])
    ET.SubElement(size_elem, 'width').text = str(row['width'])
    ET.SubElement(size_elem, 'depth').text = str(row['depth'])

    object_elem = ET.SubElement(image_elem, 'object')
    ET.SubElement(object_elem, 'name').text = str(row['name'])
    ET.SubElement(object_elem, 'pose').text = str(row['pose'])
    ET.SubElement(object_elem, 'truncated').text = str(row['truncated'])
    ET.SubElement(object_elem, 'difficult').text = str(row['difficult'])

    bndbox_elem = ET.SubElement(object_elem, 'bndbox')
    ET.SubElement(bndbox_elem, 'xmin').text = str(row['xmin'])
    ET.SubElement(bndbox_elem, 'ymin').text = str(row['ymin'])
    ET.SubElement(bndbox_elem, 'xmax').text = str(row['xmax'])
    ET.SubElement(bndbox_elem, 'ymax').text = str(row['ymax'])

tree = ET.ElementTree(root)

tree.write('output.xml', encoding='utf-8', xml_declaration=True)