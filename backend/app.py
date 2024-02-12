from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from schemas import NewGameRequest, GameTurnRequest
from services import get_game_service, GameService


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def error_exception_handler(request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code, 
        content={'error': exception.detail}
    )


@app.post("/new")
async def create_game(
    game_data: NewGameRequest,
    game_service: GameService = Depends(get_game_service)
):
    async with game_service.session.begin():
        game_id = await game_service.create(game_data=game_data)
        game = await game_service.get_game_field_by_id(game_id=game_id)
    return game

@app.post("/turn")
async def create_game(
    turn_data: GameTurnRequest,
    game_service: GameService = Depends(get_game_service)
):
    async with game_service.session.begin():
        return (await game_service.game_turn(turn_data=turn_data))


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
    )