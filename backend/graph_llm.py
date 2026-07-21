from langchain_groq import ChatGroq

import os
from langchain_core.messages import HumanMessage
from state import AgentState
from langgraph.graph import StateGraph, START, END 
from state import AgentState
from balance_agent import BalanceAgent
from money_transfer_agent import MoneyTransfer
from Documenttr import DocumentTransfer
import json





bal_ser=BalanceAgent()
mer_ser=MoneyTransfer()
intent=""
amount=""
s_ac=""
r_ac=""
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def balance_agent_node(state: AgentState) -> AgentState:
    print("state",state)
    return bal_ser.get_balance(state)
    
def document_agent_node(state:AgentState)->AgentState:
    print("doc_state",state)
    return dt_ser.document_check_agent(state)
def orchestrator_node(state: AgentState) -> AgentState:
     print("in_or=",in_str)
     if("loan" in in_str):
         print("loan")
         global  dt_ser
         dt_ser=DocumentTransfer()
         return{
             ** state,
             "intent":"loan"
             
             
         }
     if("account" in in_str):
         print("accountopening")
         return{
             ** state,
             "intent":"account"
             
             
         }
            
     if("balance" in in_str.lower()):
        #print("orchestor",in_str)
        return {
            **state,
            "intent": "balance"
        }
     elif("transfer" in in_str.lower()):
          return {
            **state,
        
            
            "intent": "money_transfer"
        }
     else: 

        return {
        **state,
        "intent": "unknown"
        } 
def  transaction_status_node(state:AgentState):
    return  mer_ser.transaction_check_node(state)

        
def  account_status_node(state:AgentState)->AgentState:  
        print("Enter into account status check node")
        return mer_ser.account_check_node(state)
       
def route_agent_node(state:AgentState)->AgentState:
      intent = state["intent"].strip().lower()
      
      if("balance" in in_str.lower()):
    
        return "balance"
      if(intent=="money_transfer"):
          return "transfer"
      elif(intent=="loan"):
          return "loan"
      elif(intent=="account"):
          return "account" 
      else:
        return "unknown"  
def  otp_agent_node(state:AgentState)->AgentState:
   
  return mer_ser.otp_generate_node(state)
def otp_checkagent_node(state:AgentState):
    return  mer_ser.otp_check_node(state)

def  owner_agent_node(state:AgentState) ->AgentState:
            
          cust_id=int(input("Enter Customer No"))
          state["customer_id"]=cust_id
          return mer_ser.owner_check_agent(state)
def transfer_agent_node (state:AgentState)->AgentState: 
    print("Transfer agent started")
    return{
         **state,
         "status":"success",
         "message" : "Transfer started"
    }  
def fraud_agent_node(state:AgentState)->AgentState:
   return mer_ser.fraud_check_node(state)

def route_check_node(state:AgentState)->str:
   print("agent_status =", state["agent_status"])
   print("status =", state["status"])
   print("message =", state["message"])
   
   if(state["ownership_verified"]==True and state["status"]=="success" and state["agent_status"]=="OwnerCheck" ):
       return "verified"
   elif( state["agent_status"]=="AccountStatus_checked" and state["status"]=="success"):
       return  "verified"
   elif( state["agent_status"]=="FraudDetection" and state["status"]=="success"):
       print ("transactio")
       return  "transaction"
   elif( state["agent_status"]=="FraudDetection" and state["status"]=="failure"):
       return  "verified"
   elif( state["agent_status"]=="otpcheck" and state["status"]=="success"):
       return  "verified"
   
   else:
       return("Failed")
    
def start_router(state:AgentState):
    if state.get("agent_status") == "OTP_Entered":
        return "otp"
    return "normal"
def process_query(state:AgentState)->AgentState:



  global in_str
  print("gop=",state["generated_otp"])
  print("uop=",state["user_otp"])
  
        #return transaction_status_node(state)
        

    
  


  if(state["generated_otp"]is None):
      query=state["user_query"]
      print(query)
      response = llm.invoke([
      HumanMessage(
        content=f"""ba
        You are a banking intent extraction engine.
         skip    account_number from Fields  for MoneyTransfer
        Extract information from the user's query.

        Return ONLY valid JSON.
        Do not use Markdown.
       Do not use ```json or ```.
     intent:
       -loan
       -credit
       -account

         Fields:
          intent:

        if the above intent is available  skip  the below intent and fields

        Allowed intents:
          - balance_inquiry
          - money_transfer
          - transaction_history
          - unknown

         Fields:
         - intent
         - account_number
         - amount
        - count
         -sender_account
        -receiver_account

 


        User Query:
       {query}"""
        
        )
        ])
      print("response=",response.content)
      llm_output=json.loads(response.content)
      in_str=str(llm_output["intent"]).lower()
      print("in_sre=",in_str)
      state["intent"]  = llm_output.get("intent","unknown")
      state["sender_account"]= llm_output.get("sender_account")
      state["receiver_account"]= llm_output.get("receiver_account")
      state["amount"] = llm_output.get("amount")
      state["account_number"] = llm_output.get("account_number")
      state: AgentState = {
    "user_query": query,
    "intent":state["intent"],
    "account_number":state["account_number"],
    "amount": state["amount"],
    "count": None,
    "balance": None,
    "status": "",
    "message": "",
    "ownership_verified": None,
    "sender_account_status": None,
    "receiver_account_status": None,
    "document_enter":None,
     "user_otp":None,
    "generated_otp":None,
    "otp_status":bool,
    "sender_account": state["sender_account"],
    "receiver_account": state["receiver_account"]
}
     

 
  
  #print("\nAgentState before graph:")
  #print(initial_state) 
 
  
  in_str=state["intent"]
  
  builder = StateGraph(AgentState)
  builder.add_node("orchestor", orchestrator_node)
  builder.add_node("BalanceAgent",balance_agent_node)
  builder.add_node("DocumentAgent",document_agent_node)
  builder.add_node("TransferAgent",transfer_agent_node)
  builder.add_node("OwnerCheckAgent",owner_agent_node)
  builder.add_node("AccountStatusCheck",account_status_node)
  builder.add_node("FraudCheck",fraud_agent_node)
  builder.add_node("OtpGenerateAgent",otp_agent_node)
  builder.add_node("OtpCheckAgent",otp_checkagent_node)
  builder.add_node("TransactionAgent" ,transaction_status_node)

  builder.add_conditional_edges(
    START,
    start_router,
    {
        "normal": "orchestor",
        "otp": "OtpCheckAgent"
    }
)
  builder.add_conditional_edges(
    "orchestor",
     route_agent_node,
     {
        "balance": "BalanceAgent",
         "transfer":"TransferAgent",
        "loan":"DocumentAgent",
        "account":"DocumentAgent",
         "unknown":END
     }   

 )       
    
 


#builder.add_edge("orchestor", "BalanceAgent")   
  builder.add_edge("BalanceAgent",END)
  builder.add_edge("DocumentAgent",END)
  builder.add_edge("TransferAgent","OwnerCheckAgent")
  builder.add_conditional_edges(
      "OwnerCheckAgent",
       route_check_node,
       {
         "verified":"AccountStatusCheck",
         "Failed" :END 
       }

 )
 # builder.add_edge("AccountStatusCheck",END)
  builder.add_conditional_edges(
     "AccountStatusCheck",
      route_check_node,
       {
         "verified":"FraudCheck",
         "Failed" :END 
       }
  )
  builder.add_conditional_edges(
  "FraudCheck",
  route_check_node,
   {
       "verified":"OtpGenerateAgent",
      "transaction":"TransactionAgent",
       "Failed" :END       
         
    
   })
  
  builder.add_edge("OtpGenerateAgent",END)
  
  builder.add_conditional_edges(
      "OtpCheckAgent",
       route_check_node,
   {
       "verified":"TransactionAgent",
       "Failed":END
             
    
   })
  

  builder.add_edge("TransactionAgent",END)
  graph = builder.compile()
  final_state=graph.invoke(state)
  
  print(final_state)
  return(final_state)
       
