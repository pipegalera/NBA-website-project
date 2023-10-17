from sqlmodel import Field, SQLModel, create_engine, Session, select, SQLModel, Table
from datetime import datetime
from mysqlSDK import aws_engine
from typing import Optional,List

engine = aws_engine()

class GameStats(SQLModel, table=True):
    personGameId: Optional[str] = Field(default=None, primary_key=True)
    status: str
    name: str
    personId: int
    teamName: str
    teamId: int
    gameName: str
    gameId: int
    gameTime: datetime
    points: int
    assists: int
    rebounds: int
    blocks: int
    turnovers: int
    top_player: Optional[int] = Field(default=None)

# Load tables into AWS
SQLModel.metadata.clear()
SQLModel.metadata.create_all(engine)