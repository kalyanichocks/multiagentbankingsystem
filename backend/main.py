from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Dummy credentials
USERNAME = "kalyani"
PASSWORD = "bank123"


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.post("/login", response_class=HTMLResponse)
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    if username == USERNAME and password == PASSWORD:
                return RedirectResponse(url="/chat", status_code=303)
    else:
    
 
 
        return RedirectResponse(url="/", status_code=303)
    
@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={}
    )   
