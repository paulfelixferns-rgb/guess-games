import random
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Guess the Number")
templates = Jinja2Templates(directory="templates")

secret_number = random.randint(1, 100)
attempts = 0
message = ""
game_won = False

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "message": message,
            "attempts": attempts,
            "game_won": game_won
        }
    )

@app.post("/guess", response_class=HTMLResponse)
async def guess(request: Request, number: int = Form(...)):
    global secret_number, attempts, message, game_won

    if game_won:
        message = "Game over. Start a new game."
    else:
        attempts += 1
        if number < secret_number:
            message = "Too low. Try again."
        elif number > secret_number:
            message = "Too high. Try again."
        else:
            message = f"Correct! You guessed it in {attempts} attempts."
            game_won = True

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "message": message,
            "attempts": attempts,
            "game_won": game_won
        }
    )

@app.post("/new", response_class=HTMLResponse)
async def new_game(request: Request):
    global secret_number, attempts, message, game_won
    secret_number = random.randint(1, 100)
    attempts = 0
    message = "New game started. Guess a number from 1 to 100."
    game_won = False

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "message": message,
            "attempts": attempts,
            "game_won": game_won
        }
    )
