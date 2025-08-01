# ♟️ Chess Coach Agent

AI-powered agent that reviews your chess games, detects blunders, and explains them like a personal coach.

Built with:
- `python-chess` for PGN parsing
- `Stockfish` for evaluation
- `Gemini` (or OpenAI) for natural language coaching

---

## Features

✅ Parses `.pgn` files  
✅ Uses Stockfish to find best moves  
✅ Detects blunders based on eval drop  
✅ Uses Gemini to explain the mistake  

---

## Setup

1. Clone the repo:
```bash
git clone https://github.com/your_username/chess-coach-agent
cd chess-coach-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install [Stockfish](https://stockfishchess.org/download/) and ensure it's in your PATH.

4. Add `.env` file with:
```
GEMINI_API_KEY=your-key-here
```

---

## Run

```bash
python analyze_game.py your_game.pgn
```