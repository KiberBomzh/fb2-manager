from lxml import etree


ns = {'fb': "http://www.gribuser.ru/xml/fictionbook/2.0"}

def get_meta(book):
    meta = {
        'title': None,
        'authors': [],
        'annotation': [],
        'language': None,
        'sequence': None
    }
    
    
    root = etree.parse(book).getroot()
    t_info = root.find('fb:description/fb:title-info', namespaces = ns)
    
    title = t_info.find('fb:book-title', namespaces = ns)
    if title is not None:
        meta['title'] = title.text
    
    
    authors = t_info.xpath('./fb:author', namespaces = ns)
    for author in authors:
        first_n = author.find('fb:first-name', namespaces = ns)
        middle_n = author.find('fb:middle-name', namespaces = ns)
        last_n = author.find('fb:last-name', namespaces = ns)
        names = []
        if first_n is not None:
            if first_n.text is not None:
                names.append(first_n.text)
        if middle_n is not None:
            if middle_n.text is not None:
                names.append(middle_n.text)
        if last_n is not None:
            if last_n.text is not None:
                names.append(last_n.text)
        
        author_n = ' '.join(names)
        if author_n:
            meta['authors'].append(author_n)
    
    
    ann_p = t_info.xpath('./fb:annotation/fb:p', namespaces = ns)
    for p in ann_p:
        if p.text is not None:
            meta['annotation'].append(p.text)
    
    
    lang = t_info.find('fb:lang', namespaces = ns)
    if lang is not None:
        meta['language'] = lang.text
    
    
    sequence = t_info.find('fb:sequence', namespaces = ns)
    if sequence is not None:
        seq = {}
        if 'name' in sequence.attrib:
            seq['name'] = sequence.get('name')
        
        if 'number' in sequence.attrib:
            seq['number'] = sequence.get('number')
        
        
        if seq:
            meta['sequence'] = seq
    
    return meta