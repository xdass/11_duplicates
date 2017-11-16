import os
import sys
import hashlib
from collections import defaultdict


def get_file_md5(path):
    hasher = hashlib.md5()
    filename = os.path.basename(path).encode()
    block_size = 128 * hasher.block_size
    hasher.update(filename)
    try:
        with open(path, 'rb') as file:
            for chunk in iter(lambda: file.read(block_size), b''):
                hasher.update(chunk)
            file_hash = hasher.hexdigest()
        return file_hash
    except FileNotFoundError:
        return None


def get_duplicate_files(file_hashes):
    dup_files = {key: value for key, value in file_hashes.items() if len(value) > 1}
    return dup_files


def crawling_directory(path):
    processed_files = defaultdict(list)
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            full_path = os.path.join(dir_path, file_name)
            file_md5 = get_file_md5(full_path)
            processed_files[file_md5].append(full_path)
    return processed_files

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        crawl_results = crawling_directory(directory_path)
        duplicates_files = get_duplicate_files(crawl_results)

        for files in duplicates_files.values():
            print("Файлы дубли: ")
            print(*files, sep='\n')
            print("---------------------------------")
    else:
        print('Укажите путь к папке: python duplicates.py <directory_path>')
