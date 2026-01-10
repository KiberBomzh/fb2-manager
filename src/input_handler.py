import sys
from zipfile import ZipFile
from pathlib import Path

from src.metadata_extractor import get_meta


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

def read_dir(path, books, recursive = True):
    for file in path.glob("*"):
        if not file.is_file():
            continue
        
        if file.suffix.lower() == '.fb2':
            books[file] = get_meta(file)
        elif file.suffix.lower() == '.zip':
            unpacked_file = unpack_zip(file)
            
            if unpacked_file is None:
                continue
            else:
                books[unpacked_file] = get_meta(unpacked_file)

def get_files(path):
    books = {}
    if path.exists():
        if path.is_dir():
            read_dir(path)
        elif path.is_file():
            if path.suffix.lower() == '.fb2':
                books[path] = get_meta(path)
            else:
                raise ValueError(f"File {path} is not FB2!")
    else:
        raise ValueError(f"Path {path} is not exists!")
    
    return books