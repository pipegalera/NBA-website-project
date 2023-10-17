from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sql.mysqlSDK import get_data_aws

############ APP ##############
app = FastAPI()

templates = Jinja2Templates(directory="templates")
players_info = get_data_aws(query = """
                            SELECT name, teamName, gameName,DATE_FORMAT(gameTime, "%a %D (%Y)") AS gameTime
                            FROM gamestats 
                            WHERE top_player = 1
                            ORDER BY gameTime DESC, gameName
                            """)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   return templates.TemplateResponse("home.html", {"request": request, 
                                                   "players": players_info})

@app.get("/about")
def about():
    return "About page with documentation"
