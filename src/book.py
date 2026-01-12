from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil

from src.metadata_reader import get_meta
from src.template_handler import main as get_name


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
            temp_path = Path(temp_dir).resolve()
            with ZipFile(self.path, 'r') as book_read:
                first_file = book_read.namelist()[0]
                book_read.extract(first_file, temp_path)
            
            extracted_file = temp_path / first_file
            shutil.move(extracted_file, book_path)
        
        
        self.path.unlink()
        self.path = book_path
        self.is_zip = False
    
    
    def rename(self, template, number_template):
        name = get_name(self.get_meta(), template, number_template)
        if not name:
            return
        
        if self.is_zip:
            new_path = self.path.parent / (name + '.fb2.zip')
        else:
            new_path = self.path.parent / (name + '.fb2')
        
        if self.path != new_path and not new_path.exists():
            self.path = Path(shutil.move(self.path, new_path))
    
    
    def sort(self, main_path, template, number_template):
        path_parts = get_name(self.get_meta(), template, number_template)
        if not isinstance(path_parts, list):
            path_parts = [path_parts]
        
        
        if self.is_zip:
            new_path = main_path / ('/'.join(path_parts) + '.fb2.zip')
        else:
            new_path = main_path / ('/'.join(path_parts) + '.fb2')
        
        
        if not new_path.parent.exists():
            new_path.parent.mkdir(parents = True)
        
        if self.path != new_path and not new_path.exists():
            self.path = Path(shutil.move(self.path, new_path))
    

    def print(self):
        print(self.path.parent.name, self.path.name, sep = '/')
        
        meta = self.get_meta()
        
        
        if meta['title']:
            print("Title:", meta['title'].strip())
        
        if len(meta['authors']) > 1:
            print("Authors:")
            for aut in meta['authors']:
                print(f"\t{aut.strip()}")
        elif meta['authors']:
            print("Author:", meta['authors'][0].strip())
        
        
        if meta['sequence']:
            print("Sequence:", meta['sequence'].strip(), end = ' ')
            
            if meta['number']:
                print(meta['number'].strip())
            else:
                print()
        
        if meta['language']:
            print("Language:", meta['language'].strip())


    
    
    def get_meta(self):
        if self.is_zip:
            with ZipFile(self.path, 'r') as book_read:
                first_file = book_read.namelist()[0]
                with book_read.open(first_file, 'r') as book:
                    return get_meta(book)
        else:
            return get_meta(self.path)
