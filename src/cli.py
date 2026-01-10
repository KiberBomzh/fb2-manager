from sys import argv, exit
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from rich import print


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
    
    
    annotation = []
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

def get_without_forbidden_chars(text):
    forbiddenChars = {'<', '>', ':', '"', '/', '|', '?', '*', '`'}
    
    for char in text:
        if char in forbiddenChars:
            text = text.replace(char, '')
    
    return text

def unpack_zip(file_zip):
    with ZipFile(file_zip, 'r') as b_r:
        n_list = b_r.namelist()
        if len(n_list) != 1:
            return None
        
        book_name = n_list[0]
        if Path(book_name).suffix.lower() != '.fb2':
            return None
        
        b_r.extract(book_name, file_zip.parent)
    
    book = file_zip.parent / book_name
    file_zip.unlink()
    return book


def main():
    path = Path(argv[1])
    books = {}
    if path.exists():
        if path.is_dir():
            for file in path.glob("*"):
                if file.is_file() :
                    if file.suffix.lower() == '.fb2':
                        books[file] = get_meta(file)
                    elif file.suffix.lower() == '.zip':
                        unpacked_file = unpack_zip(file)
                        
                        if unpacked_file is None:
                            continue
                        else:
                            books[unpacked_file] = get_meta(unpacked_file)
        elif path.is_file():
            if path.suffix.lower() == '.fb2':
                books[path] = get_meta(path)
            else:
                print(f"[red]File {path} is not FB2![/]")
                exit(1)
    else:
        print(f"[red]Path {path} is not exists![/]")
        exit(1)
    
    for key, value in books.items():
        title = value['title'].replace(' ', '_')
        title = get_without_forbidden_chars(title)
        key.rename(key.parent / (title + key.suffix))

if __name__ == '__main__':
    main()