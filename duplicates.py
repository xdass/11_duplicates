import os
import sys
import hashlib


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
    dup_files = list(file_path for path_list in file_hashes.values() if len(path_list) > 1 for file_path in path_list)
    return dup_files


def crawling_directory(path):
    processed_files = {}
    for dir_path, dir_names, file_names in os.walk(path):
        if file_names:
            for file_name in file_names:
                full_path = os.path.join(dir_path, file_name)
                file_md5 = get_file_md5(full_path)
                if file_md5 in processed_files.keys():
                    processed_files[file_md5].append(full_path)
                else:
                    processed_files[file_md5] = [full_path]
    return processed_files

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        crawl_results = crawling_directory(directory_path)
        duplicates_files = get_duplicate_files(crawl_results)

        for file in duplicates_files:
            print(file)
    else:
        print('Укажите путь к папке: python duplicates.py <directory_path>')
