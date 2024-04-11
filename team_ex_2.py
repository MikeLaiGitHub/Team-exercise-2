import time
import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# Convert objects produced by wikipedia package to a string var for saving to text file
def convert_to_str(obj):
 if type(obj) == list:
   mystr = '\n'.join(obj)
   return mystr
 elif type(obj) in [str, int, float]:
   return str(obj)


# IMPLEMENTATION 1: sequential example
def wiki_sequentially(results):
 t_start = time.perf_counter()
  def dl_and_save(item):
   page = wikipedia.page(item, auto_suggest=False)
   title = page.title
   references = convert_to_str(page.references)
   out_filename = title + ".txt"
   with open(out_filename, 'wt') as fileobj:
     fileobj.write(references)


 for item in results:
   dl_and_save(item)


 print('\nsequential function:')
 t_end = time.perf_counter()
 print(f'code executed in {t_end - t_start} seconds')


# IMPLEMENTATION 2: concurrent example w/ threads
def concurrent_threads(results):
 t_start = time.perf_counter()
  def dl_and_save_thread(item):
   page = wikipedia.page(item, auto_suggest=False)
   title = page.title
   references = convert_to_str(page.references)
   out_filename = title + ".txt"
   with open(out_filename, 'wt') as fileobj:
     fileobj.write(references)


 with ThreadPoolExecutor() as executor:


   executor.map(dl_and_save_thread, results)
  
 print('\nthread pool function:')
 t_end = time.perf_counter()
 print(f'code executed in {t_end - t_start} seconds')


# IMPLEMENTATION 3: concurrent example w/ processes
def concurrent_process(results):
 t_start = time.perf_counter()
  def dl_and_save_process(item):
   page = wikipedia.page(item, auto_suggest=False)
   title = page.title
   references = convert_to_str(page.references)
   out_filename = title + ".txt"
   with open(out_filename, 'wt') as fileobj:
     fileobj.write(references)


 with ProcessPoolExecutor() as executor:
   executor.map(dl_and_save_process, results)
 print('\nprocess pool function:')
 t_end = time.perf_counter()
 print(f'code executed in {t_end - t_start} seconds')


if __name__ == "__main__":
 search_results = wikipedia.search("general artificial intelligence")
 wiki_sequentially(search_results)
 concurrent_threads(search_results)
 concurrent_process(search_results)
