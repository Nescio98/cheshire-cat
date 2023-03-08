import time
from .utils import log

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

import langchain
from langchain.vectorstores import Qdrant


def get_vector_store(collection_name, embedder):

    qd_client = QdrantClient(host="vector-memory", port=6333) # TODO: should be configurable

    # create collection if it does not exist
    try:
        qd_client.get_collection(collection_name)
        tabula_rasa = False
        log(f'Collection "{collection_name}" already present in vector store')
    except:
        log(f'Creating collection {collection_name} ...')
        qd_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE), # TODO: if we change the embedder, how do we know the dimensionality?
        )
        tabula_rasa = True
        

    vector_memory = Qdrant(
        qd_client,
        collection_name,
        embedding_function=embedder.embed_query
    )

    if tabula_rasa:
        vector_memory.add_texts(
            ['I am the Cheshire Cat'],
            [{
                'who' : 'cheshire-cat',
                'when': time.time(),
                'text': 'I am the Cheshire Cat', 
            }]
        )
        
    log( dict(qd_client.get_collection(collection_name)) )

    return vector_memory