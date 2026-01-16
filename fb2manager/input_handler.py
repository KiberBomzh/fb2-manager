from zipfile import ZipFile
from pathlib import Path

from fb2manager.book import Book


def is_zip_a_book(path):
    with ZipFile(path, 'r') as book:
        if len(book.namelist()) == 1:
            first_file = book.namelist()[0]
            if first_file.lower().endswith('.fb2'):
                return True
    
    return False

def read_dir(path, books, recursive):
    if recursive:
        p_iter = path.rglob("*")
    else:
        p_iter = path.glob("*")
    
    for file in p_iter:
        if not file.is_file():
            continue
        
        if file.suffix.lower() == '.fb2':
            books.append(Book(file))
        elif file.suffix.lower() == '.zip':
            if is_zip_a_book(file):
                books.append(Book(file, is_zip = True))


def get_files(path, books, recursive):
    if path.is_dir():
        read_dir(path, books, recursive)
    elif path.is_file():
        if path.suffix.lower() == '.fb2':
            books.append(Book(path))
        elif path.suffix.lower() == '.zip':
            if is_zip_a_book(path):
                books.append(Book(path, is_zip = True))
        else:
            print(f"File {path} is not FB2!")
    else:
        print(f"Path {path} is not exists!")
    


def get_books(args):
    books = []
    for i in args.input:
        get_files(Path(i).resolve(), books, args.recursive)
    
    return books