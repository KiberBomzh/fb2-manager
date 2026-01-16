import argparse
from importlib.metadata import version
from pathlib import Path

from yaspin import yaspin


from fb2manager.input_handler import get_books



@yaspin(text = "Sorting...", color = 'green')
def sort_handler(args, books):
    main_path = Path(args.main_path)
    
    if not args.template:
        args.template = [
            '{authors1}',
            '{sequence}',
            '{number/ - }{title}'
        ]
    
    for book in books:
        book.sort(main_path, args.template, args.number_template)
    
    if not args.keep_empty_folders:
        removed_any = True
        while removed_any:
            removed_any = False
            empty_folders = []
            for folder in main_path.rglob('*'):
                if folder.is_dir() and not any(folder.iterdir()):
                    empty_folders.append(folder)
            
            for empty_folder in sorted(empty_folders, key = lambda x: len(x.parts), reverse = True):
                empty_folder.rmdir()
                removed_any = True


@yaspin(text = "Renaming...", color = 'green')
def rename_handler(args, books):
    for book in books:
        book.rename(args.template, args.number_template)


@yaspin(text = "Compression...", color = 'green')
def zip_handler(args, books):
    for book in books:
        book.zip()


@yaspin(text = "Uncompression...", color = 'green')
def unzip_handler(args, books):
    for book in books:
        book.unzip()

@yaspin(text = "Prettifying...", color = 'green')
def pretty_handler(args, books):
    for book in books:
        book.prettify()

def print_handler(args, books):
    for book in books:
        book.print()
        if book != books[-1]:
            print()


def main():
    parser = argparse.ArgumentParser(
        description = "Cli tool for managing fb2 books"
    )
    
    
    parser.add_argument('-i', '--input',
        action = 'append', default = [], 
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
        default = '.',
        help = "Main path for sort")
    sort_parser.add_argument('-t', '--template', 
        action = 'append', default = [], 
        help = "Template for sort")
    sort_parser.add_argument('-n', '--number-template',
        type = str, default = '2|.|1',
        help = "Template for sequence's number")
    sort_parser.add_argument('--keep-empty-folders', 
        action = 'store_true', 
        help = "Do NOT remove empty folders in main path")
    
    rename_parser = subparsers.add_parser('rename', help = "Rename file(s)")
    rename_parser.add_argument('-t', '--template', 
        type = str, default = '{authors&/ - }{sequence/ <number*(|)/, >}{title/}', 
        help = "Template for renaming")
    rename_parser.add_argument('-n', '--number-template',
        type = str, default = '2|.|1',
        help = "Template for sequence's number")
    
    _zip_parser = subparsers.add_parser('zip', help = "Zip books")
    _unzip_parser = subparsers.add_parser('unzip', help = "Unzip books")
    _pretty_parser = subparsers.add_parser('pretty', help = "Prettify books")
    _print_parser = subparsers.add_parser('print', help = "Print metadata")
    
    args = parser.parse_args()

    if not args.input:
        args.input.append('.')
    
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
        case 'pretty':
            pretty_handler(args, books)
        case 'print':
            print_handler(args, books)

    

if __name__ == '__main__':
    main()
