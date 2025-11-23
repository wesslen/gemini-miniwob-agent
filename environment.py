# environment.py
import gymnasium
import miniwob
from miniwob.action import ActionTypes

class MiniWoBWrapper:
    def __init__(self, env_name, render_mode='human', base_url=None):
        gymnasium.register_envs(miniwob)
        
        # Prepare arguments for the environment
        env_kwargs = {}
        if base_url:
            env_kwargs['base_url'] = base_url

        # Pass the URL explicitly here
        self.env = gymnasium.make(env_name, render_mode=render_mode, **env_kwargs)
    
    def reset(self):
        obs, info = self.env.reset()
        return obs, info

    def step(self, agent_action):
        """
        Translates high-level agent intent to MiniWoB low-level action dict.
        """
        # Default empty action structure
        # action_type 0 is usually NONE/Wait
        raw_action = self.env.unwrapped.create_action(ActionTypes.NONE)

        try:
            ref_id = int(agent_action.get("element_id", 0))
            
            if agent_action["action_type"] == "CLICK":
                raw_action = self.env.unwrapped.create_action(
                    ActionTypes.CLICK_ELEMENT, 
                    ref=ref_id
                )
            
            elif agent_action["action_type"] == "TYPE":
                text = agent_action.get("text_to_type", "")
                raw_action = self.env.unwrapped.create_action(
                    ActionTypes.TYPE_TEXT, 
                    ref=ref_id, 
                    text=text
                )
        except Exception as e:
            print(f"Action translation error: {e}")

        return self.env.step(raw_action)

    def close(self):
        self.env.close()