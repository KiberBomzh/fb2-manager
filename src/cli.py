from sys import argv
from pathlib import Path

from src.input_handler import get_files


def get_without_forbidden_chars(text):
    forbiddenChars = {'<', '>', ':', '"', '/', '|', '?', '*', '`'}
    
    for char in text:
        if char in forbiddenChars:
            text = text.replace(char, '')
    
    return text


def main():
    path = Path(argv[1])
    try:
        books = get_files(path)
    except Exception as err:
        print(err)
        return 1
    
    for key, value in books.items():
        title = value['title'].replace(' ', '_')
        title = get_without_forbidden_chars(title)
        key.rename(key.parent / (title + key.suffix))

if __name__ == '__main__':
    main()