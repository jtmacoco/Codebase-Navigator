from rag.retriever import Retriever
from rag.generator import Generator
import time

class RAGPipeline:
    def __init__(self):
        self.retriever=Retriever()
        self.generator=Generator()
        self.chat_history = []
    
    def add_item_limit(self,item,cur_list,max_limit=2):
        cur_list.append(item)
        if len(cur_list) > max_limit:
            cur_list[:] = cur_list[-max_limit:]
    
    def query(self,user_query:str, name_space:str):
        data = self.retriever.retrieve(user_query,name_space)
        if self.chat_history:
            history_context = "\n".join([f"User:{u}\n Assistant:{a}" for u, a in self.chat_history])
            user_query = f"Chat History:{history_context}\n User Query:{user_query}"

        start_time = time.perf_counter()
        response = self.generator.generate_response(user_query,data['fine'],data['medium'])
        end_time = time.perf_counter()
        elapsed_time = end_time-start_time
        try:
            self.add_item_limit((user_query,response),self.chat_history)
        except Exception as e:
            print(e)
        print(f"Elapsed time:{elapsed_time:.6f}seconds")
        return response