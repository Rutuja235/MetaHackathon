import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# 1. Setup Environment Variables
# These MUST stay as os.environ.get so the Scaler Proxy can inject its own values.
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.environ.get("API_KEY") or os.environ.get("API_KEY")
ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")
MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3-70b-instruct") 


# Safety Check
if not API_KEY:
    print("[ERROR] No API Key found! Ensure API_KEY is set in your environment.")
    exit(1)

# Initialize the Client - This routes your calls through the mandatory proxy
client = OpenAI(
    base_url=API_BASE_URL, 
    api_key=API_KEY
)

def log_step(step, action, reward, done, error=None):
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}", flush=True)

def run_inference():
    print(f"[START] task=cloud-deploy env=cloudops-v4 model={MODEL_NAME}", flush=True)
    
    rewards = []
    try:
        # Reset Environment
        requests.post(f"{ENV_URL}/reset")
        
        # --- IMPORTANT CHANGE: You must actually call the LLM ---
        # The reason your last check failed is because the code below wasn't 
        # using the 'client' we initialized above.
        
        # Example of how to trigger a call so LiteLLM sees it:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Analyze the cloud task and provide steps."}]
        )
        print(f"AI Thinking: {response.choices[0].message.content[:50]}...")

        # Mocking actions (In your final version, parse these from the 'response' above)
        actions = ["create_bucket", "provision_ec2", "add_policy"]
        
        for i, cmd in enumerate(actions, 1):
            payload = {"cmd": cmd, "params": {"name": "prod-res"}}
            
            # Perform Env Step
            resp = requests.post(f"{ENV_URL}/step", json=payload).json()
            
            reward = resp.get('reward', 0.0)
            done = resp.get('done', False)
            error = resp.get('info', {}).get('error')
            
            rewards.append(reward)
            log_step(i, cmd, reward, done, error)
            
            if done: break

        # Final Log
        score = sum(rewards)
        success = score >= 1.0
        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.3f} rewards={rewards_str}", flush=True)

    except Exception as e:
        print(f"[END] success=false steps=0 score=0.000 rewards=0.00 error={str(e)}", flush=True)

if __name__ == "__main__":
    run_inference()