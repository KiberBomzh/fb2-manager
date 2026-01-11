import argparse
from importlib.metadata import version

from src.input_handler import get_books


def get_without_forbidden_chars(text):
    forbiddenChars = {'<', '>', ':', '"', '/', '|', '?', '*', '`'}
    
    for char in text:
        if char in forbiddenChars:
            text = text.replace(char, '')
    
    return text


def sort_handler(args, books):
    pass

def rename_handler(args, books):
    pass

def zip_handler(args, books):
    for book in books:
        book.zip()

def unzip_handler(args, books):
    for book in books:
        book.unzip()


def main():
    parser = argparse.ArgumentParser(
        description = "Cli tool for managing fb2 books"
    )
    
    
    parser.add_argument('-i', '--input',
        action = 'append', default = [], required = True, 
        help = "Input files (books) or directories with books")
    
    parser.add_argument('-r', '--recursive',
        action = 'store_true',
        help = "Search books in subdirectories")
    
    parser.add_argument('-V', '--version', 
        action = 'version',
        version = f'%(prog)s {version('fb2-manager')}', 
        help = "Show version")
    
    
    subparsers = parser.add_subparsers(dest = 'command', help = "Commands")
    
    sort_parser = subparsers.add_parser('sort', help = "Sort books in folders structure")
    sort_parser.add_argument('-p', '--main-path',
        type = str, help = "Main path for sort")
    sort_parser.add_argument('-t', '--template', 
        action = 'append', default = [], 
        help = "Template for sort")
    sort_parser.add_argument('--keep-empty-folders', 
        action = 'store_true', 
        help = "Do NOT remove epty folders in main path")
    
    rename_parser = subparsers.add_parser('rename', help = "Rename file(s)")
    rename_parser.add_argument('-t', '--template', 
        type = str, default = '', 
        help = "Template for renaming")
    
    zip_parser = subparsers.add_parser('zip', help = "Zip books")
    unzip_parser = subparsers.add_parser('unzip', help = "Unzip books")
    
    args = parser.parse_args()
    
    try:
        books = get_books(args)
    except Exception as err:
        print(f"Error: {err}")
        return 1
    
    match args.command:
        case 'sort':
            sort_handler(args, books)
        case 'rename':
            rename_handler(args, books)
        case 'zip':
            zip_handler(args, books)
        case 'unzip':
            unzip_handler(args, books)
    
    

if __name__ == '__main__':
    main()