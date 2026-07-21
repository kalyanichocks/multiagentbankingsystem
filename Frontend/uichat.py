import customtkinter as ctk
from datetime import datetime

import groqllm as gl
from state import AgentState


# -----------------------------
# Window
# -----------------------------
class chatbotpr:
  def __init__(self):
    
    self.state:AgentState= {
    "customer_id": 456,
    "user_query": None,
                           
    "intent":None,
                           
    "account_number":None,
    
    "amount": None,
    "count": None,
    "balance": None,
    "status": None,
    "message": None,
    "ownership_verified": None,
    "sender_account_status": None,
    "receiver_account_status": None,
    "document_enter":None,
    "user_otp":None,
    "generated_otp":None,
    "otp_status":False,
    "sender_account": None,
    "receiver_account":None
}
        
    self.message=""
    self.app = ctk.CTk()
    self.app.title("AI Banking Assistant")
    self.app.geometry("1300x750")
    self.app.configure(fg_color="#F8F9FA")
    self.main_frame = ctk.CTkFrame(
    self.app,
    fg_color="#F8F9FA",
    corner_radius=0
     )
    self.chat_frame = ctk.CTkScrollableFrame(self.main_frame,
                                                
    fg_color="#F8F9FA"
     )
    self.bottom_frame = ctk.CTkFrame(
    self.main_frame,
    fg_color="#F8F9FA",
    corner_radius=0
)
  
    self.input_box = ctk.CTkTextbox(
   self.bottom_frame,
    height=45,
    fg_color="white",
    border_width=1,
    border_color="#D1D5DB",
    text_color="black",
    corner_radius=20,
    font=("Arial",14)
)
    self.sidebar(self.app)
    self.bottom_frame_chat()
    
  def run(self):
        self.app.mainloop()

# =============================
# Sidebar
# =============================
  def sidebar(self,app):
    sidebar = ctk.CTkFrame(
       app,
    width=250,
    corner_radius=0,
    fg_color="#0B1F4D"
)
    sidebar.pack(side="left", fill="y")

# Logo
    logo = ctk.CTkLabel(
    sidebar,
    text="🏦 SecureBank\nAI Assistant",
    font=("Arial", 24, "bold"),
    text_color="white",
    justify="left"
   )
    logo.pack(pady=(30,40), padx=20, anchor="w")

# Menu Buttons
    menu_items = [
    "💬  New Chat",
    "💳  Account Summary",
    "💸  Transactions",
    "💰  Cards",
    "🏠  Loan Information",
    "🎧  Support",
    "⚙️  Settings"
]

    for item in menu_items:
      btn = ctk.CTkButton(
        sidebar,
        text=item,
        width=210,
        height=45,
        fg_color="transparent",
        hover_color="#1E3A8A",
        anchor="w",
        font=("Arial",16)
    )
      btn.pack(pady=8, padx=20)

# =============================
# Main Area
# =============================
  


 

# Header
    header = ctk.CTkFrame(
    self.main_frame,
    height=70,
    fg_color="white"
)
    header.pack(fill="x")

    title = ctk.CTkLabel(
    header,
    text="🤖 Banking Assistant",
    font=("Arial",28,"bold"),
    text_color="#0B1F4D"
)
    title.pack(side="left", padx=25, pady=18)

    status = ctk.CTkLabel(
    header,
    text="● Online",
    text_color="green",
    font=("Arial",14)
)
    status.pack(side="left", pady=25)

    self.main_frame.pack(side="left", fill="both", expand=True)
    self.chat_frame.pack(fill="both", expand=True, padx=20, pady=20)

# =============================
   

# -----------------------------
# Bot Message
# -----------------------------
  def bot_message1(self,message):

    row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
    row.pack(fill="x", pady=8)

    bubble = ctk.CTkLabel(
        row,
        text=message,
        justify="left",
        wraplength=500,
        corner_radius=15,
        fg_color="#E8EDF7",
        text_color="black",
        padx=15,
        pady=12,
        font=("Arial", 16)
    )

    bubble.pack(anchor="w")


# -----------------------------
# User Message
# -----------------------------
  def user_message(self,message):

    row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
    row.pack(fill="x", pady=8)

    bubble = ctk.CTkLabel(
        row,
        text=message,
        justify="left",
        wraplength=500,
        corner_radius=15,
        fg_color="#0B1F4D",
        text_color="white",
        padx=15,
        pady=12,
        font=("Arial", 14)
    )

    bubble.pack(anchor="e")
    self.bot_message("👋 Welcome to SecureBank AI Assistant.")

#user_message("I want to check my account balance.")

#bot_message(
    "Sure! Please enter your account number "
    "or login to continue."
#)
  def bottom_frame_chat(self):

   self.bottom_frame.pack(fill="x", padx=20, pady=(0,20))
   self.input_box.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0,10)
)

   send_button = ctk.CTkButton(
      self.bottom_frame,
    text="➤",
    width=55,
    height=55,
    corner_radius=28,
    fg_color="#0B1F4D",
    hover_color="#1E3A8A",
    command=self.send,
    font=("Arial",22)
  )

   send_button.pack(side="right")
   #self.input_box.bind("<KeyRelease>", self.auto_resize)

  def auto_resize(self,event=None):

    lines = int(self.input_box.index("end-1c").split(".")[0])

    if lines < 2:
        lines = 2

    if lines > 6:
        lines = 6

    self.input_box.configure(height=lines * 25)
  def send(self):
    state: AgentState
  
    self.message = self.input_box.get("1.0","end").strip()

    if self.message == "":
        return

    self.user_messagese(self.message)

   
    self.input_box.delete("1.0","end")

    self.input_box.configure(height=45)
    if (self.state["generated_otp"]is None or str(self.state["message"]).strip()=="Transaction completed sucessfully" )  :
       print("otpNone")
       self.state["user_query"]=self.message
    else:
       self.state["user_otp"]=self.message
       self.state["agent_status"] = "OTP_Entered"
       print("intent in new chat",self.state["intent"])
       print(self.message)
       print(self.state["user_otp"])
       self.state["message"]="otp"
    self.state = gl.process_query(self.state)

    print("send=",type(self.state))
    if(self.state["document_enter"]==True):
      print("++++++++++++++document enter+++++++++++++++++++++")
      print(self.state["message"])
      self.message= self.state["message"]
    elif (self.state["status"]=="otp_required"):  
       #self.input_box.insert("enter otp")
       print(self.state["status"])
  
    self.message= self.state["message"]
       
    self.bot_message(self.message)


 

# ----------------------------
# Current Time
# ----------------------------
  def current_time(self):
    return datetime.now().strftime("%I:%M %p")


# ----------------------------
# Improved Bot Message
# ----------------------------
  def bot_message(self,msg):

    row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
    row.pack(fill="x", pady=8)

    bubble = ctk.CTkFrame(
        row,
        fg_color="#E8EDF7",
        corner_radius=15
    )

    bubble.pack(anchor="w", padx=10)

    label = ctk.CTkLabel(
        bubble,
        text=msg,
        justify="left",
        wraplength=500,
        font=("Arial",18,"bold"),
        text_color="black"
    )

    label.pack(padx=15, pady=(12,5))

    time = ctk.CTkLabel(
        bubble,
        text=self.current_time(),
        font=("Arial",18),
        text_color="gray"
    )

    time.pack(anchor="e", padx=10, pady=(0,8))

    self.chat_frame._parent_canvas.yview_moveto(1.0)


# ----------------------------
# Improved User Message
# ----------------------------
  def user_messagese(self,msg):

    row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
    row.pack(fill="x", pady=8)

    bubble = ctk.CTkFrame(
        row,
        fg_color="#0B1F4D",
        corner_radius=15
    )

    bubble.pack(anchor="e", padx=10)

    label = ctk.CTkLabel(
        bubble,
        text=msg,
        justify="left",
        wraplength=500,
        font=("Bahnschrift SemiCondensed",18),
        text_color="white"
    )

    label.pack(padx=15, pady=(12,5))

    time = ctk.CTkLabel(
        bubble,
        text=self.current_time(),
        font=("Arial",10),
        text_color="#DDDDDD"
    )

    time.pack(anchor="e", padx=10, pady=(0,8))

    self.chat_frame._parent_canvas.yview_moveto(1.0)
ui=chatbotpr()
print("ui called")
ui.run()
