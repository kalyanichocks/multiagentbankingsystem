import  mysql.connector
from mysql.connector import Error

class  Mysq1Connection:
      
      def __init__(self):
        self.conn=None
        try:
          
            self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306,
            database="multiagent"
        )
            if(self.conn.is_connected):
             print("Connected successfully")
        except Error as e :
           print("MySqlError", e)
      def get_connection(self):  
         return self.conn  
      def close_connection(self):
          if self.conn and self.conn.is_connected():
             self.conn.close()
             print("MySqlConnection")
