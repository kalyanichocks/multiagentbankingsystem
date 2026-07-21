rom pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import TextLoader
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import Docx2txtLoader
from langchain_groq import ChatGroq
import os 
from state import AgentState
from langchain_core.messages import AIMessage



class  documentsclass:

 
  def __init__(self):

   api_key= os.getenv("GROQ_API_KEY")
    self.llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
      
 )
    self.embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
) 
    self.pc = Pinecone(
    api_key=	
"pcsk_***********************************************************"
)
    self.text_splitter= SemanticChunker(
    embeddings=self.embedding_model,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=80   # Try 80, 75, or 70
)
    if "banking-docs" in self.pc.list_indexes().names():
      self.pc.delete_index("banking-docs")

    self.pc.create_index(
    name="banking-docs",
    dimension=384,           # Must match the embedding model
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
    index=self.pc.Index("banking-docs")
    self.vector_store = PineconeVectorStore(
    index=index,
    embedding=self.embedding_model
)
  def index_documents(self):

    document_map={
      "loan":"document/Home Loan.docx",
      "account" :"document/AccountOpen.docx"
    }
    for category,file_path in document_map.items():
       
       
       loader=Docx2txtLoader(file_path)
       documents = loader.load()
       print(file_path,category)
      
       for doc in documents:
          doc.metadata["category"] = category
          doc.metadata["source"] = file_path
   
       #print(documents[0].page_content)
   
       chunks=self.text_splitter.split_documents(documents)
    
      #for  i,chunk in enumerate(chunks):
      #print("chunk_kal",chunks[i].page_content)
       self.vector_store.add_documents(chunks)
    print("chunks")
    

  def documentsagenttest(self,state:AgentState)->AgentState:
     
  


    query =state["user_query"]
    intent=state["intent"]
    print("user",query)
    print("intent=",intent)
    


    results = self.vector_store.similarity_search(
    query,k=5,filter={"category":intent }
    
)

    context=""
    context = "\n\n".join(doc.page_content for doc in results)

    print("++++++++++++++++++++++++++++++context++++++++++++++++++++++++++++++++++++++++++")
#print(context)
#try:
    #print("index=",pc.list_indexes().names())
#except Exception as e:
    #print(e)

    prompt = f"""
You are a banking assistant.
answer shortly  if user ask explain anwer ellaborate
Answer only using the provided context
answer point by point.
If the answer is not in the context, say:
"I couldn't find this information."

 Context:
 {context}


Question:
{query}

Answer:"""

    response=self.llm.invoke(prompt)   
    print(response.content)
   
    return {
         **state,
         "message": response.content
    
    }
    

