import time
import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

# Function to convert objects produced by Wikipedia package to a string for saving to text file
def convert_to_str(obj):
    if isinstance(obj, list):
        return '\n'.join(obj)
    elif isinstance(obj, (str, int, float)):
        return str(obj)

# Function to download page and save references to a text file
def dl_and_save(item, executor_type):
    try:
        page = wikipedia.page(item, auto_suggest=False)
        title = page.title
        references = convert_to_str(page.references)
        out_filename = os.path.join("wiki_dl", title + ".txt")
        with open(out_filename, 'wt') as fileobj:
            fileobj.write(references)
        print(f'{executor_type} - {item}: Downloaded and saved successfully.')
    except Exception as e:
        print(f'{executor_type} - {item}: Error occurred - {str(e)}')

# Function to execute tasks sequentially
def wiki_sequentially(search_term):
    t_start = time.perf_counter()
    results = wikipedia.search(search_term)
    for item in results:
        dl_and_save(item, 'Sequential')

    t_end = time.perf_counter()
    t_lapse = t_end - t_start
    print(f'Sequential execution completed in {t_lapse} seconds')

# Function to execute tasks concurrently
def concurrent_execution(executor_type, max_workers, search_term):
    t_start = time.perf_counter()
    results = wikipedia.search(search_term)
    with executor_type(max_workers=max_workers) as executor:
        executor.map(dl_and_save, results, [executor_type.__name__] * len(results))

    t_end = time.perf_counter()
    t_lapse = t_end - t_start
    print(f'{executor_type.__name__} execution completed in {t_lapse} seconds')

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure output directory exists
    output_dir = os.path.join(script_dir, "wiki_dl")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prompt user for search term
    search_term = input("Enter search term (minimum 4 characters): ").strip()
    if len(search_term) < 4:
        search_term = "generative artificial intelligence"

    # Execute tasks sequentially
    wiki_sequentially(search_term)

    # Execute tasks concurrently using ThreadPoolExecutor
    concurrent_execution(ThreadPoolExecutor, max_workers=5, search_term=search_term)

    # Execute tasks concurrently using ProcessPoolExecutor
    concurrent_execution(ProcessPoolExecutor, max_workers=5, search_term=search_term)
