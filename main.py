# main.py
import os
# 1. Load env vars BEFORE importing anything else
from dotenv import load_dotenv
load_dotenv()

from phoenix.otel import register

# Configure the Phoenix tracer
tracer_provider = register(
  project_name="miniwob-agent-testing", # Default is 'default'
  auto_instrument=True # Auto-instrument your app based on installed OI dependencies
)


import time
from agent import GeminiAgent
from environment import MiniWoBWrapper

def run_eval(task_name, episodes=5):
    print(f"--- Starting Evaluation for {task_name} ---")
    
    # Get the URL from .env, usually "http://localhost:8000"
    miniwob_url = os.getenv("MINIWOB_URL")
    
    # If the manual check worked at .../miniwob/click-test-2.html, 
    # we might need to append /miniwob to the base URL if it's not already there.
    # But usually, passing the root (http://localhost:8000) is sufficient if 
    # the environment expects the standard structure.
    
    print(f"Using MiniWoB URL: {miniwob_url}")

    agent = GeminiAgent(model_name=os.getenv("MODEL_NAME", "gemini-3-pro-preview"))
    
    # Pass the URL explicitly
    env = MiniWoBWrapper(task_name, render_mode='human', base_url=miniwob_url)

    total_reward = 0

    for episode in range(episodes):
        obs, info = env.reset()
        done = False
        step_count = 0
        
        print(f"Episode {episode + 1}/{episodes} | Goal: {obs['utterance']}")

        while not done and step_count < 10: # Limit steps per episode
            # 1. Get Action from Gemini
            try:
                action_intent = agent.get_action(
                    screenshot_array=obs["screenshot"], 
                    instruction=obs["utterance"],
                    dom_elements=obs["dom_elements"]
                )
                print(f"  Gemini Action: {action_intent}")
            except Exception as e:
                print(f"  Gemini Error: {e}")
                break

            # 2. Execute Action in Environment
            obs, reward, terminated, truncated, info = env.step(action_intent)
            
            # 3. Check Status
            done = terminated or truncated
            step_count += 1

            if reward > 0:
                print("  > SUCCESS!")
                total_reward += reward
                break
        
        time.sleep(1) # Small pause between episodes

    env.close()
    print(f"--- Finished. Success Rate: {total_reward / episodes * 100}% ---")

if __name__ == "__main__":
    # Example tasks: 
    # 'miniwob/click-test-2-v1' (Simple clicking)
    # 'miniwob/email-inbox-v1' (Complex reasoning)
    run_eval('miniwob/click-test-2-v1', episodes=3)