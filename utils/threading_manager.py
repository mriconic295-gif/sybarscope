from concurrent.futures import ThreadPoolExecutor, as_completed

class ThreadingManager:
    def __init__(self, max_workers=5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def run_tasks(self, tasks: list):
        """tasks: list of (function, args) tuples"""
        futures = {self.executor.submit(fn, *args): fn for fn, args in tasks}
        results = {}
        for future in as_completed(futures):
            fn = futures[future]
            try:
                result = future.result()
                results[fn.__name__] = result
            except Exception as e:
                results[fn.__name__] = f"Error: {str(e)}"
        return results
