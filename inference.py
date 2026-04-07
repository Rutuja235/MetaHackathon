import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Environment Variables - STRICTLY matching the Checklist
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-instruct")
# The checklist specifically mentions HF_TOKEN should NOT have a default
HF_TOKEN = os.getenv("HF_TOKEN") 
# Fallback for your local testing
API_KEY = os.getenv("API_KEY") or HF_TOKEN
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

# Safety Check
if not API_KEY:
    print("[ERROR] No API Key or HF_TOKEN found!")
    exit(1)

# 2. Initialize OpenAI Client (Strictly following the checklist)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def log_step(step, action, reward, done, error=None):
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}", flush=True)

def run_inference():
    # START LOG - Exactly as required
    print(f"[START] task=cloud-deploy env=cloudops-v4 model={MODEL_NAME}", flush=True)
    
    rewards = []
    try:
        # Reset Environment
        requests.post(f"{ENV_URL}/reset")
        
        # Mandatory LLM Call via Proxy
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Analyze the cloud task and provide steps."}]
        )
        
        # Mocking actions (Parse these from 'response' in your final logic)
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

        # Final END Log - Matching required structure
        total_score = sum(rewards)
        success = total_score >= 1.0
        print(f"[END] success={str(success).lower()} steps={len(rewards)} score={total_score:.3f} rewards={total_score:.2f}", flush=True)

    except Exception as e:
        print(f"[END] success=false steps=0 score=0.000 rewards=0.00 error={str(e)}", flush=True)

if __name__ == "__main__":
    run_inference()