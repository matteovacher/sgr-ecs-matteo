import math 
from pathos.multiprocessing import ProcessPool
import dill
import multiprocess 
import errno 

class ParallelTool :

    def __init__(self, config) : 
        self.cpus = config.cpus


    def run(self, function, chunk) : 
        if self.cpus > 1 : 
            return self._process_parallel(function, chunk)
        else : 
            return [function(*args) for args in chunk]


    def _cut_chunk(self, chunk) : 
        
        chunks = []
        length = len(chunk)
        size_of_chunk = math.ceil(length / self.cpus)
        for i in range(0, length, size_of_chunk) :
            chunks.append(chunk[i:i+size_of_chunk])
        return chunks

    def _worker(self, function, chunk) : 
        results = []
        for arguments in chunk : 
            results.append(function(*arguments))
        return results
    
    # def _process_parallel(self, function, chunk) : 

    #     chunks = self._cut_chunk(chunk)
    #     process_worker = lambda chunk : self._worker(function, chunk)

    #     pool = ProcessPool(nodes = self.cpus)
    #     results = pool.map(
    #             process_worker,
    #             chunks
    #         )
    #     pool.close()
    #     pool.join()
    #     pool.clear()
        
    #     results_formatted = []
    #     for list_of_result in results : 
    #         for result in list_of_result : 
    #             results_formatted.append(result)
        
    #     return results_formatted 


    def _process_parallel(self, function, chunk) : 
        pool = multiprocess.Pool(self.cpus)
        ars = [(args[0], pool.apply_async(function, args)) for args in chunk]
        results = []
        for entity_id, ar in ars : 
            try : 
                results.append(ar.get(timeout=120))     # 120 s max par robot
            except Exception : 
                results.append((entity_id, -1000, True))
        for p in pool._pool :
            p.kill()
        pool.terminate()
        return results