import threading
import os
import time
from queue import Queue

def search_keywords_in_file(file, keywords, results):
    if os.path.isfile(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        results[keyword].append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    else:
        print(f"File not found: {file}")

def worker(files, keywords, results, lock):
    local_results = {keyword: [] for keyword in keywords}
    for file in files:
        search_keywords_in_file(file, keywords, local_results)
    
    with lock:
        for keyword in keywords:
            results[keyword].extend(local_results[keyword])

def main():
    files = ['path/to/your/files/file1.txt', 'path/to/your/files/file2.txt', 'path/to/your/files/file3.txt', 'path/to/your/files/file4.txt']  # Список файлів для обробки
    keywords = ['keyword1', 'keyword2']  # Ключові слова для пошуку
    num_threads = 4  # Кількість потоків
    results = {keyword: [] for keyword in keywords}
    lock = threading.Lock()

    # Розділення файлів між потоками
    chunk_size = len(files) // num_threads
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    threads = []

    start_time = time.time()  # Початок вимірювання часу

    for chunk in chunks:
        t = threading.Thread(target=worker, args=(chunk, keywords, results, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Виведення результатів
    for keyword, files in results.items():
        print(f'Keyword: {keyword}, Files: {files}')

    end_time = time.time()  # Кінець вимірювання часу
    print(f'Time taken: {end_time - start_time:.2f} seconds')

if __name__ == "__main__":
    main()
