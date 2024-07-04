import multiprocessing
import os
import time

def search_keywords_in_file(file, keywords, queue):
    results = {keyword: [] for keyword in keywords}
    if os.path.isfile(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        results[keyword].append(file)
            queue.put(results)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    else:
        print(f"File not found: {file}")

def worker(files, keywords, queue):
    for file in files:
        search_keywords_in_file(file, keywords, queue)

def main():
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  # Список файлів для обробки
    keywords = ['keyword1', 'keyword2']  # Ключові слова для пошуку
    num_processes = multiprocessing.cpu_count()  # Кількість процесів
    queue = multiprocessing.Queue()

    # Розділення файлів між процесами
    chunk_size = len(files) // num_processes
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    processes = []

    start_time = time.time()  # Початок вимірювання часу

    for chunk in chunks:
        p = multiprocessing.Process(target=worker, args=(chunk, keywords, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Збір результатів
    combined_results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        result = queue.get()
        for keyword in result:
            combined_results[keyword].extend(result[keyword])

    # Виведення результатів
    for keyword, files in combined_results.items():
        print(f'Keyword: {keyword}, Files: {files}')

    end_time = time.time()  # Кінець вимірювання часу
    print(f'Time taken: {end_time - start_time:.2f} seconds')

if __name__ == "__main__":
    main()
