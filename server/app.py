from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os

# Important: Fix the system path to find the 'env' folder now that we are in 'server'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.main import CloudOpsEnv
from env.models import Action

app = FastAPI()
env = CloudOpsEnv()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>CloudOps Environment v4</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f0f2f5; }
                .button { background-color: #2563eb; color: white; padding: 15px 32px; text-decoration: none; font-size: 18px; border-radius: 8px; display: inline-block; transition: 0.3s; }
                .button:hover { background-color: #1d4ed8; }
            </style>
        </head>
        <body>
            <h1>🚀 CloudOps OpenEnv Simulator</h1>
            <p>The environment is LIVE and ready for evaluation.</p>
            <br>
            <a href="/docs" class="button">Launch Interactive API Docs</a>
            <br><br>
            <p>Click the button above to test <b>/reset</b>, <b>/state</b>, and <b>/step</b>.</p>
        </body>
    </html>
    """

@app.post("/reset")
def reset():
    return env.reset()

@app.get("/state")
def state():
    return env.state()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info,
        "state": env.state()
    }

# --- Validator Fix: Standard Entry Point ---
def main():
    """Explicit main function required by the validator."""
    # We use "server.app:app" string to ensure Uvicorn can find the app in multi-mode
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()
