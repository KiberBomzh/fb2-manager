from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from tempfile import TemporaryDirectory

from src.metadata_reader import get_meta


def get_free_path(path):
    counter = 1
    name = path.stem
    while (path / (name + path.suffix)).exists():
        name = f'{path.stem}-{counter}'
        counter += 1
    
    return (path.parent / (name + path.suffix))

class Book():
    def __init__(self, path, is_zip = False):
        self.path = path
        self.is_zip = is_zip
    
    
    
    def zip(self):
        if self.is_zip:
            return
        
        zipped_book = get_free_path(self.path.parent / (self.path.name + '.zip'))
        with ZipFile(zipped_book, 'w', compression = ZIP_DEFLATED) as book:
            book.write(self.path, arcname = self.path.name)
        
        self.path.unlink()
        self.path = zipped_book
        self.is_zip = True
    
    
    def unzip(self):
        if not self.is_zip:
            return
        
        name = self.path.stem
        if name.lower().endswith('.fb2'):
            index = name.rfind('.')
            name = name[:index]
        
        book_path = get_free_path(self.path.parent / (name + '.fb2'))
        
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with ZipFile(self.path, 'r') as book_read:
                first_file = book_read.namelist()[0]
                book_read.extract(first_file, temp_path)
            
            extracted_file = temp_path / first_file
            extracted_file.replace(book_path)
        
        
        self.path.unlink()
        self.path = book_path
        self.is_zip = False
    
    
    def get_meta(self):
        if self.is_zip:
            with ZipFile(self.path, 'r') as book_read:
                first_file = book_read.namelist()[0]
                with book_read.open(first_file, 'r') as book:
                    return get_meta(book)
        else:
            return get_meta(self.path)