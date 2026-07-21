import json
import mysql.connector
from mysql.connector import Error
from sqlconn import Mysq1Connection
from state import AgentState
from p_test import documentsclass
from datetime import datetime
import secrets


class MoneyTransfer:
   
   def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306,
            database="multiagent"
        )
        self.Myconn=Mysq1Connection()
        self.flag=0
      
        self.conn= self.Myconn.get_connection()
        self.cursor=self.conn.cursor()


   def owner_check_agent (self,state:AgentState)->AgentState: 
   
      account_no=int(state["sender_account"])

      cust_id=int(state["customer_id"])
    #account_no2=int(input("enter account_nimber2"))
      print("=====================")
      print("Customer_id=",cust_id)
      print("account=",account_no)


      #Myconn=Mysq1Connection()

      ##conn= Myconn.get_connection()
      #cursor=conn.cursor()
      try:
            self.cursor.execute(
            "SELECT  account_number  from accounts  WHERE customer_id =%s",
            (cust_id,)
        )  
            result = self.cursor.fetchone()
            if  result[0] == account_no  :
              print("owner checkeg")
              return{
                 **state,
                 "status":"success",
                 "agent_status":"OwnerCheck",
                 "ownership_verified":True,
                 "message":"ownershipChecked"
            
              }
            elif(result==None):
             return{
                 **state,
                 "status":"Failed",
                 "ownership_verified":False,
                 "agent_status":"OwnerCheck",
                 "message":"Account not Found"
            
              }
            else:
                return{
                 **state,
                  "status":"Failed",
                 "ownership_verified":False,
                 "agent_status":"OwnerCheck",
                 "message":"qwnership Failed"
         }
          
      except  Error as e:
        print(e)
      
   def  account_check_node(self,state:AgentState)->AgentState:
     print("Enter  into account  check node")
     saccount_no=int(state["sender_account"])
     raccount_no=int(state["receiver_account"])
   
     query="""SELECT
    sender.account_number AS sender_account,
    sender.account_status AS sender_status,
    receiver.account_number AS receiver_account,
    receiver.account_status AS receiver_status
    FROM accounts AS receiver
    JOIN accounts AS sender
    ON sender.account_number = %s
   WHERE receiver.account_number = %s;
   """      
    
     self.cursor.execute(query,(saccount_no,raccount_no))
     rows = self.cursor.fetchall()
     s_st=rows[0][1]
     r_st=rows[0][3]
     return{
                 **state,
                 "status":"success",
                 
                 "agent_status":"AccountStatus_checked",
                 "sender_account_status":s_st,
                 "receiver_account_status":r_st
 

                 
            
              } 
   def  fraud_check_node(self,state:AgentState)->AgentState:
         
        
        customer_id=state["customer_id"]
        transaction_time = datetime.now() 
 
        if(int(state["amount"])>=100000):
           risk_score+=30
        query=   """select count(*) AS transaction_count
 from transactions2
 where customer_id = %s
  and transaction_date between
    DATE_SUB(now(), INTERVAL 10 MINUTE)
    and  now();"""
        self.cursor.execute(query,(customer_id,))
        result=self.cursor.fetchone()
        print(result[0])
        if(int(result[0])>=5):
             risk_score+=20
        hr=transaction_time.hour
        if(0<=hr<=5):
            risk_score=risk_score+10
        b_ac=state["receiver_account"]
        query="""select   
           TIMESTAMPDIFF(MINUTE, added_date, NOW()) AS minutes_since_added from beneficiary where customer_id=%s and beneficiary_account=%s """
        self.cursor.execute(query,(customer_id,b_ac)) 
        result=self.cursor.fetchone()
        print("result=",result[0])
        #if result and result[0] is not None:
            
        if int(result[0] )< 720:
            risk_score += 10
        else:
        # Beneficiary not found
         risk_score += 20
        if(risk_score>=60):
             print("Fraud detection")
             message="F"
        print("risk=",risk_score)
        if(risk_score>=60 and  int(state["amount"])>3000):
          return{
           **state,
           "agent_status":"FraudDetection",
           "message" :"Fraud detection  identified",
            "status":"failure"


        } 
        else:
         
         return{
           **state,
           "agent_status":"FraudDetection",
           "message" :"Fraud detection not identified",
            "status":"success"


        } 
   def otp_generate_node(self,state:AgentState)->AgentState:
       print("enter into otp_gen")
       otp = secrets.randbelow(900000) + 100000
       print(otp)
       return {
          **state,
    "status": "otp_required",
    "agent_status":"otpgenerated",
    "message": "OTP has been sent. Please enter the OTP.",
    "generated_otp": otp
    }
   def otp_check_node(self,state:AgentState)->AgentState:
      print("enter into otp_check")
      gen_otp=state["generated_otp"]
      user_otp=state["user_otp"]
      print(gen_otp,user_otp)
      if str(state["generated_otp"]).strip() == str(state["user_otp"]).strip():
       # print("Inside second if")
        return{
           **state,
            "agent_status":"otpcheck",
            "status":"success"
        }
      else:
          return{
           **state,
            "agent_status":"otpcheck",
            "status":"Failure"
        }
     

           
   def transaction_check_node(self,state:AgentState)->AgentState:
       print("transaction completed")

       return{ 
          **state ,
          "message":"Transaction completed sucessfully",
          "status":"success",
          "generated_otp":None
       
       }
