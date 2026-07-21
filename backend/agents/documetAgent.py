from mysql.connector import Error
from sqlconn import Mysq1Connection
from state import AgentState
from p_test import documentsclass

class DocumentTransfer:
  def __init__(self):
        self.doccons = documentsclass()
        self.doccons.index_documents()
        
  def document_check_agent(self,state:AgentState):
          state["document_enter"]=True
          print("enter into DocumentTransfer")
         
          return self.doccons.documentsagenttest(state)
      
       
    
