import os
import chess.pgn
import chess.engine
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
STOCKFISH_PATH = os.path.join(os.path.dirname(__file__), "stockfish-ubuntu-x86-64-avx2", "stockfish","stockfish-ubuntu-x86-64-avx2")
DEPTH = 15
EVAL_THRESHOLD = 1.0

model = genai.GenerativeModel("gemini-1.5-flash")

def explain_mistake(position_fen, played_move, best_move, eval_diff):
    prompt = f"""
You're a chess coach. The player made the move {played_move} in this position:

FEN: {position_fen}

But Stockfish recommends {best_move}. The eval dropped by {eval_diff:.2f} pawns.

Explain why {played_move} is a mistake and how {best_move} improves the position.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def analyze_pgn(path):
    with open(path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    if game is None:
        print(f"[❌ ERROR] No valid game found in {path}")
        return

    board = game.board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    print(f"\n[🎯 Analyzing {path}]\n")

    move_number = 1
    for move in game.mainline_moves():
        try:
            info_before = engine.analyse(board, chess.engine.Limit(depth=DEPTH))
            score_before = info_before["score"].white().score(mate_score=10000)
        except Exception as e:
            print(f"[⚠️ Engine Error Before Move {move_number}] {e}")
            break

        try:
            played = board.san(move)
            board.push(move)
        except Exception as e:
            print(f"[❌ Illegal Move] {move} at board state: {board.fen()}")
            print(f"[❌ Skipping move {move_number}]")
            continue

        try:
            info_after = engine.analyse(board, chess.engine.Limit(depth=DEPTH))
            score_after = info_after["score"].white().score(mate_score=10000)
        except Exception as e:
            print(f"[⚠️ Engine Error After Move {move_number}] {e}")
            break

        if score_before is None or score_after is None:
            print(f"[⚠️ Missing score data at move {move_number}], skipping")
            continue

        eval_diff = (score_after - score_before) / 100.0

        if abs(eval_diff) >= EVAL_THRESHOLD:
            try:
                best_move = board.san(info_before["pv"][0])
            except Exception:
                best_move = info_before["pv"][0].uci()

            print(f"\n🔍 Move {move_number}: {played}")
            print(f"❗ Eval dropped: {score_before/100:.2f} → {score_after/100:.2f}")
            print(f"💡 Best move was: {best_move}")
            print("🧠 Gemini explains:")
            try:
                fen = board.fen()
                explanation = explain_mistake(fen, played, best_move, abs(eval_diff))
                print(explanation)
            except Exception as e:
                print(f"[Gemini Error] {e}")

        move_number += 1

    engine.quit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python analyze_game.py your_game.pgn")
        sys.exit(1)

    analyze_pgn(sys.argv[1])
