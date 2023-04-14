import shutil
import argparse
from pathlib import Path

# Initialize argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-b','--base', help='Root directory from which to start sorting', type=Path, default=Path.home())
parser.add_argument('-d','--destination', help='Directory in which files will be sorted', type=Path, default=Path('Sorter'))
parser.add_argument('-e','--exclude', help='Directory to be excluded from sorter', type=list)
parser.add_argument('-r', '--recursive', help='Wheather or not to sort in subdirectory of base', action='store_true')
output = parser.add_mutually_exclusive_group()
output.add_argument('-p','--print', help='Print files found on their type', action='store_true')
output.add_argument('-c','--copy', help='Copy files found and sort them in destination according to type', action='store_true')
output.add_argument('-m','--move', help='Move files found and sort them in destination according to type', action='store_true')

# Parse arguments
base = parser.parse_args().base
destination = parser.parse_args().destination
display = parser.parse_args().print
copy = parser.parse_args().copy
move = parser.parse_args().move
exclude = parser.parse_args().exclude
recursive = parser.parse_args().recursive

print(parser.parse_args())

# Define global variables
BASE_FOLDER = base
DESTINATION_FOLDER = destination
EXCLUSION_FOLDER = exclude

# Define dictionary of file types and their corresponding extensions
FILE_TYPE = {
  "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
  "Spreadsheets": [".xls", ".xlsx", ".csv"],
  "Presentations": [".ppt", ".pptx"],
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
  "Audio": [".mp3", ".wav", ".aac", ".flac"],
  "Video": [".mp4", ".avi", ".mov", ".wmv"],
  "Code": [".py", ".java", ".c", ".cpp", ".html", ".css", ".js"]
}

def sorter_display(ftype, source):
    '''Prints out result to system stdout'''
    print('\t', end='')
    print(f'{ftype}: {source}')

def sorter_copy(ftype, source):
    '''Copies output to DESINATION_FOLDER'''
    destination = DESTINATION_FOLDER / ftype
    # Create destination directory if it doesn't exist
    destination.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy(source, destination)
        print(f'{source} copied successfully.')
    except shutil.SameFileError:
        print('Source and destination represent the same file')
    except PermissionError:
        print('Permission Denied')
    except Exception as err:
        print(f'{type(err).__name__}: {err}')

def sorter_move(ftype, source):
    '''Moves output to DESINATION_FOLDER'''
    destination = DESTINATION_FOLDER / ftype
    # Create destination directory if it doesn't exist
    destination.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(source, destination)
        print(f'{source} moved successfully.')
    except shutil.SameFileError:
        print('Source and destination represent the same file')
    except PermissionError:
        print('Permission Denied')
    except Exception as err:
        print(f'{type(err).__name__}: {err}')

def sort_files(base_path):
    '''Recursively sorts files in directory and its subdirectories'''
    try:
        print('='*50)
        print(f'{base_path}')
        print('='*50)
        for sub_path in base_path.iterdir():
            if sub_path.is_file():
                file_extension = sub_path.suffix
                directory_list = [x for x in FILE_TYPE.keys()]
                for index, extensions in enumerate(FILE_TYPE.values()):
                    if file_extension in extensions:
                        if copy:
                            sorter_copy(directory_list[index], sub_path)
                        elif move:
                            sorter_move(directory_list[index], sub_path)
                        else:
                            sorter_display(directory_list[index], sub_path)
            else:
                if recursive:
                    if not (sub_path.parts[-1].startswith('.') or 'AppData' in sub_path.parts):
                        sort_files(sub_path)
    except Exception as err:
        print(f'{type(err).__name__}: {err}')
                

print(f'Base directory: {BASE_FOLDER.absolute()}') 
print(f'Destination directory: {DESTINATION_FOLDER.absolute()}')                          
sort_files(BASE_FOLDER)
