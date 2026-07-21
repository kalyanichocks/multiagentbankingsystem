from typing import TypedDict
import mysql.connector
from state import AgentState
from sqlconn import Mysq1Connection



class BalanceAgent:
     def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306,
            database="multiagent"
        )
        print("init")
     def get_balance(self,state:AgentState) -> AgentState :
         Myconn=Mysq1Connection()

         conn= Myconn.get_connection()
         cursor=conn.cursor()
         print("get_balance")
         print(state["account_number"])
        #cursor = self.conn.cursor()
         cursor.execute(
            "SELECT balance FROM accounts WHERE account_number=%s",
            (state["account_number"],)
        )

         result = cursor.fetchone()
         print("value",result[0])
       
         conn.close()

         return {
            "intent": "balance_agent",
            "status": "success",
            "account_number": state["account_number"],
          
            "balance": float(result[0]),
            "message":f"ypur account balance is rupees {float(result[0]) }"
        
        } 
   

     
