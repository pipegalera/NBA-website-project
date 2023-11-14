from sqlmodel import Field, SQLModel, Session, SQLModel
from datetime import datetime
from Tests.mysqlSDK import aws_engine
from typing import Optional

engine = aws_engine()

SQLModel.metadata.clear()

class GameStats(SQLModel, table=True):
    player_game_id: Optional[int] = Field(default=None, primary_key=True)
    player_name: str
    player_id: int
    team_name: str
    team_abbreviation: str
    team_id: int 
    team_home: int
    game_id: int
    matchup: str
    game_date: datetime
    game_win: int
    pts: int
    ast: int
    reb: int
    blk: int
    tov: int
    top_player: Optional[int] = Field(default=None)

# Load tables into AWS
SQLModel.metadata.create_all(engine)


