from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sql.mysqlSDK import get_data_aws
import uvicorn
import os
from fastapi.middleware.gzip import GZipMiddleware

############ APP ##############
app = FastAPI(debug=True, use_reloader=False)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware)

templates = Jinja2Templates(directory="templates")
players_info = get_data_aws(query = """
                            SELECT personId, name, teamName, gameName, DATE_FORMAT(gameTime, "%a %D (%Y)") AS gameTime
                            FROM gamestats 
                            WHERE top_player = 1
                            ORDER BY gameTime DESC, gameName
                            """)

teams_logos = os.listdir(os.path.join("static/images/", "teams_logos"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   return templates.TemplateResponse("index.html", {"request": request, 
                                                   "players": players_info,
                                                   "teams_logos": teams_logos})

@app.get("/about")
def about():
    return "About page with documentation"

#sudo lsof -iTCP:8080 -sTCP:LISTEN
#kill -9 {{PID}}
