from lxml import etree


ns = {'fb': "http://www.gribuser.ru/xml/fictionbook/2.0"}

def get_title(t_info):
    title = t_info.find('fb:book-title', namespaces = ns)
    if title is not None:
        return title.text if title.text is not None else ''
    else:
        return ''

def get_authors(t_info):
    authors = t_info.xpath('./fb:author', namespaces = ns)
    authors_result = []
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
            authors_result.append(author_n)
    
    return authors_result

def get_language(t_info):
    lang = t_info.find('fb:lang', namespaces = ns)
    if lang is not None:
        return lang.text if lang.text is not None else ''
    else:
        return ''

def get_sequence(t_info):
    sequence = t_info.find('fb:sequence', namespaces = ns)
    if sequence is not None:
        seq = {}
        if 'name' in sequence.attrib:
            seq['name'] = sequence.get('name')
        
        if 'number' in sequence.attrib:
            seq['number'] = sequence.get('number')
        
        return seq
    return {}


def get_meta(book):
    root = etree.parse(book).getroot()
    t_info = root.find('fb:description/fb:title-info', namespaces = ns)
    s = get_sequence(t_info)
    sequence = ''
    number = ''
    if s:
        if 'name' in s:
            sequence = s['name']
        if 'number' in s:
            number = s['number']
    
    meta = {
        'title': get_title(t_info),
        'authors': get_authors(t_info),
        'language': get_language(t_info),
        'sequence': sequence,
        'number': number
    }
    
    return meta