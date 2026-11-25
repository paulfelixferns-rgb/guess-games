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

# Rock Paper Scissors
rps_player_choice = ""
rps_computer_choice = ""
rps_result = ""

# Dice Roller
dice_result = 0
dice_message = "Click Roll Dice to play."

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
        context={"request": request}
    )

@app.get("/guess", response_class=HTMLResponse)
async def guess_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="guess.html",
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
        name="guess.html",
        context={
            "request": request,
            "message": message,
            "attempts": attempts,
            "game_won": game_won
        }
    )

@app.post("/guess/new")
async def new_guess_game():
    global secret_number, attempts, message, game_won
    secret_number = random.randint(1, 100)
    attempts = 0
    message = "New game started. Guess a number from 1 to 100."
    game_won = False
    return RedirectResponse(url="/guess", status_code=303)

@app.get("/tic-tac-toe", response_class=HTMLResponse)
async def tic_tac_toe_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tictactoe.html",
        context={
            "request": request,
            "board": board,
            "current_player": current_player,
            "winner": winner,
            "game_over": game_over
        }
    )

@app.post("/tic-tac-toe/move/{position}")
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

    return RedirectResponse(url="/tic-tac-toe", status_code=303)

@app.post("/tic-tac-toe/reset")
async def reset_game():
    global board, current_player, winner, game_over
    board = [""] * 9
    current_player = "X"
    winner = None
    game_over = False
    return RedirectResponse(url="/tic-tac-toe", status_code=303)

@app.get("/rock-paper-scissors", response_class=HTMLResponse)
async def rock_paper_scissors_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="rockpaperscissors.html",
        context={
            "request": request,
            "player_choice": rps_player_choice,
            "computer_choice": rps_computer_choice,
            "result": rps_result
        }
    )

@app.post("/rock-paper-scissors/play")
async def play_rock_paper_scissors(request: Request, choice: str = Form(...)):
    global rps_player_choice, rps_computer_choice, rps_result

    choices = ["Rock", "Paper", "Scissors"]
    rps_player_choice = choice
    rps_computer_choice = random.choice(choices)

    if rps_player_choice == rps_computer_choice:
        rps_result = "It is a draw!"
    elif (
        (rps_player_choice == "Rock" and rps_computer_choice == "Scissors") or
        (rps_player_choice == "Paper" and rps_computer_choice == "Rock") or
        (rps_player_choice == "Scissors" and rps_computer_choice == "Paper")
    ):
        rps_result = "You win!"
    else:
        rps_result = "Computer wins!"

    return RedirectResponse(url="/rock-paper-scissors", status_code=303)

@app.get("/dice", response_class=HTMLResponse)
async def dice_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dice.html",
        context={
            "request": request,
            "dice_result": dice_result,
            "dice_message": dice_message
        }
    )

@app.post("/dice/roll")
async def roll_dice():
    global dice_result, dice_message
    dice_result = random.randint(1, 6)
    dice_message = f"You rolled {dice_result}!"
    return RedirectResponse(url="/dice", status_code=303)
