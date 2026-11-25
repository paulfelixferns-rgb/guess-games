import chess
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
tic_tac_toe_difficulty = "easy"

# Rock Paper Scissors
rps_player_choice = ""
rps_computer_choice = ""
rps_result = ""

# Dice Roller
dice_result = 0
dice_message = "Click Roll Dice to play."

# Coin Toss
coin_result = ""
coin_message = "Click Toss Coin to play."

# Quiz Game
quiz_questions = [
    {
        "question": "What is 7 + 8?",
        "options": ["13", "14", "15", "16"],
        "answer": "15"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Venus", "Jupiter"],
        "answer": "Mars"
    },
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "Kolkata", "New Delhi", "Chennai"],
        "answer": "New Delhi"
    },
    {
        "question": "How many days are there in a week?",
        "options": ["5", "6", "7", "8"],
        "answer": "7"
    }
]

quiz_index = 0
quiz_score = 0
quiz_message = "Choose the correct answer."
quiz_finished = False

WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

# Chess
chess_board = chess.Board()
chess_difficulty = "easy"
chess_message = "You are White. Select a piece, then select a square."
chess_game_over = False

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
            "game_over": game_over,
            "difficulty": tic_tac_toe_difficulty
        }
    )

@app.post("/tic-tac-toe/difficulty")
async def set_difficulty(request: Request, difficulty: str = Form(...)):
    global tic_tac_toe_difficulty
    tic_tac_toe_difficulty = difficulty
    return RedirectResponse(url="/tic-tac-toe", status_code=303)

@app.post("/tic-tac-toe/move/{position}")
async def move(request: Request, position: int):
    global current_player, winner, game_over, tic_tac_toe_difficulty

    if not game_over and board[position] == "":
        board[position] = "X"
        check_tic_tac_toe_winner()

        if not game_over:
            computer_move()

        if not game_over:
            current_player = "X"

    return RedirectResponse(url="/tic-tac-toe", status_code=303)

@app.post("/tic-tac-toe/reset")
async def reset_game():
    global board, current_player, winner, game_over
    board = [""] * 9
    current_player = "X"
    winner = None
    game_over = False
    return RedirectResponse(url="/tic-tac-toe", status_code=303)


def check_tic_tac_toe_winner():
    global winner, game_over

    for a, b, c in WINNING_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            winner = board[a]
            game_over = True
            return

    if "" not in board:
        winner = "Draw"
        game_over = True


def available_moves():
    return [i for i, cell in enumerate(board) if cell == ""]


def find_winning_move(player):
    for position in available_moves():
        board[position] = player

        for a, b, c in WINNING_COMBINATIONS:
            if board[a] == board[b] == board[c] == player:
                board[position] = ""
                return position

        board[position] = ""

    return None


def minimax(current_player):
    winner_result = get_winner_without_changing_state()

    if winner_result == "O":
        return 1
    if winner_result == "X":
        return -1

    moves = available_moves()

    if not moves:
        return 0

    if current_player == "O":
        best_score = -2

        for position in moves:
            board[position] = "O"
            score = minimax("X")
            board[position] = ""

            best_score = max(best_score, score)

        return best_score

    best_score = 2

    for position in moves:
        board[position] = "X"
        score = minimax("O")
        board[position] = ""

        best_score = min(best_score, score)

    return best_score


def get_winner_without_changing_state():
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def computer_move():
    global winner, game_over

    if game_over:
        return

    moves = available_moves()

    if not moves:
        return

    if tic_tac_toe_difficulty == "easy":
        position = random.choice(moves)

    elif tic_tac_toe_difficulty == "medium":
        winning_move = find_winning_move("O")

        if winning_move is not None:
            position = winning_move
        else:
            blocking_move = find_winning_move("X")

            if blocking_move is not None:
                position = blocking_move
            elif random.random() < 0.3:
                position = random.choice(moves)
            else:
                position = random.choice(moves)

    else:
        winning_move = find_winning_move("O")

        if winning_move is not None:
            position = winning_move
        else:
            blocking_move = find_winning_move("X")

            if blocking_move is not None:
                position = blocking_move
            else:
                best_score = -2
                position = moves[0]

                for move_position in moves:
                    board[move_position] = "O"
                    score = minimax("X")
                    board[move_position] = ""

                    if score > best_score:
                        best_score = score
                        position = move_position

    board[position] = "O"
    check_tic_tac_toe_winner()
    
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
@app.get("/coin-toss", response_class=HTMLResponse)
async def coin_toss_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cointoss.html",
        context={
            "request": request,
            "coin_result": coin_result,
            "coin_message": coin_message
        }
    )

@app.post("/coin-toss/flip")
async def flip_coin():
    global coin_result, coin_message
    coin_result = random.choice(["Heads", "Tails"])
    coin_message = f"The coin landed on {coin_result}!"
    return RedirectResponse(url="/coin-toss", status_code=303)

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    question = quiz_questions[quiz_index]

    return templates.TemplateResponse(
        request=request,
        name="quiz.html",
        context={
            "request": request,
            "question": question,
            "quiz_index": quiz_index,
            "quiz_score": quiz_score,
            "quiz_message": quiz_message,
            "quiz_finished": quiz_finished,
            "total_questions": len(quiz_questions)
        }
    )

@app.post("/quiz/answer")
async def quiz_answer(request: Request, answer: str = Form(...)):
    global quiz_index, quiz_score, quiz_message, quiz_finished

    if not quiz_finished:
        correct_answer = quiz_questions[quiz_index]["answer"]

        if answer == correct_answer:
            quiz_score += 1
            quiz_message = "Correct!"
        else:
            quiz_message = f"Wrong! The correct answer was {correct_answer}."

        quiz_index += 1

        if quiz_index >= len(quiz_questions):
            quiz_finished = True
            quiz_message = f"Quiz finished! Your score is {quiz_score} out of {len(quiz_questions)}."

    return RedirectResponse(url="/quiz", status_code=303)

@app.post("/quiz/reset")
async def quiz_reset():
    global quiz_index, quiz_score, quiz_message, quiz_finished
    quiz_index = 0
    quiz_score = 0
    quiz_message = "Choose the correct answer."
    quiz_finished = False
    return RedirectResponse(url="/quiz", status_code=303)

@app.get("/memory-match", response_class=HTMLResponse)
async def memory_match_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="memory.html",
        context={"request": request}
    )

@app.get("/maze", response_class=HTMLResponse)
async def maze_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="maze.html",
        context={"request": request}
    )
@app.get("/chess", response_class=HTMLResponse)
async def chess_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chess.html",
        context={
            "request": request,
            "board": chess_board,
            "message": chess_message,
            "difficulty": chess_difficulty,
            "game_over": chess_game_over
        }
    )

@app.post("/chess/difficulty")
async def set_chess_difficulty(request: Request, difficulty: str = Form(...)):
    global chess_difficulty
    chess_difficulty = difficulty
    return RedirectResponse(url="/chess", status_code=303)

@app.post("/chess/reset")
async def reset_chess():
    global chess_board, chess_message, chess_game_over
    chess_board = chess.Board()
    chess_message = "New chess game started. You are White."
    chess_game_over = False
    return RedirectResponse(url="/chess", status_code=303)
