import random
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Games")
templates = Jinja2Templates(directory="templates")

# Guess the Number
secret_number = random.randint(1, 100)
attempts = 0
message = "Guess a number from 1 to 100."
game_won = False

# Tic Tac Toe
board = [""] * 9
current_player = "X"
winner = None
game_over = False

WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "message": message,
            "attempts": attempts,
            "game_won": game_won,
            "board": board,
            "current_player": current_player,
            "winner": winner,
            "game_over": game_over
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
            "game_won": game_won,
            "board": board,
            "current_player": current_player,
            "winner": winner,
            "game_over": game_over
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
            "game_won": game_won,
            "board": board,
            "current_player": current_player,
            "winner": winner,
            "game_over": game_over
        }
    )

@app.post("/move/{position}")
async def move(request: Request, position: int):
    global current_player, winner, game_over

    if not game_over and board[position] == "":
        board[position] = current_player

        for a, b, c in WINNING_COMBINATIONS:
            if board[a] and board[a] == board[b] == board[c]:
                winner = board[a]
                game_over = True

        if not game_over and "" not in board:
            winner = "Draw"
            game_over = True

        if not game_over:
            current_player = "O" if current_player == "X" else "X"

    return RedirectResponse(url="/", status_code=303)

@app.post("/reset")
async def reset_game():
    global board, current_player, winner, game_over
    board = [""] * 9
    current_player = "X"
    winner = None
    game_over = False
    return RedirectResponse(url="/", status_code=303)