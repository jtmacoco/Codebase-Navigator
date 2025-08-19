from embeddings.pinecone_index import pinecone_retriever
from mongo.mongodb_config import get_code_chunk
from embeddings.embedder import embed
class Retriever:
    '''
    Based on a user's query will retrieve the most relavent embedding vector along with it's
    metadata.

    Args:
        user_query (str): User query string to serach against
        name_space (str): Namespace in pinecoe to search
    
    Returns:
        dict{list[dict],list[dict]}:
            - data_fine: fine grained results
            - data_medium: medium grained results
    '''
    def retrieve(self,user_query:str,name_space:str):
        embeded_query = embed([user_query])
        pine_res1,pine_res2 = pinecone_retriever(name_space,embeded_query[0])

        data_fine = []
        for match in pine_res1['matches']:
            idx = str(match['id'])
            #print(match)
            data_fine.append({
                "file":match['metadata']['file'],
                "type":match['metadata']['type'],
                "repo":match['metadata']['repo'],
                "code":get_code_chunk(idx)['code'],
            })

        data_medium = []
        for match in pine_res2['matches']:
            idx = str(match['id'])
            #print(match)
            data_medium.append({
                "file":match['metadata']['file'],
                "type":match['metadata']['type'],
                "repo":match['metadata']['repo'],
                "code":get_code_chunk(idx)['code'],
            })
        return {"fine":data_fine,"medium":data_medium}