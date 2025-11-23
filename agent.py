# agent.py
import os
from google import genai
from google.genai import types
from PIL import Image
import io

class GeminiAgent:
    def __init__(self, model_name="gemini-3-pro-preview"):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model_name = model_name

    def get_action(self, screenshot_array, instruction, dom_elements):
        """
        Sends screenshot + DOM + instruction to Gemini 3 and returns a structured action.
        """
        # Convert numpy array screenshot to PIL Image for Gemini
        image = Image.fromarray(screenshot_array)
        
        # Simplify DOM for the LLM (token efficiency)
        # We only send interactive elements with their reference IDs
        simplified_dom = [
            f"[ID: {el['ref']}] {el['tag']} text='{el.get('text', '')}'" 
            for el in dom_elements 
            # Safely check for 'hidden', default to False if missing
            if not el.get('hidden', False)
        ]
        dom_context = "\n".join(simplified_dom[:100]) # Limit context size if needed

        prompt = f"""
        You are a web automation agent. Your goal is: "{instruction}"
        
        Here is the list of interactive elements on the screen:
        {dom_context}
        
        Analyze the screenshot and the DOM list. Select the correct element ID to interact with.
        """

        # Define the schema for the model's output
        # This forces Gemini to strictly output action_type and parameters
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[image, prompt],
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "action_type": {"type": "STRING", "enum": ["CLICK", "TYPE"]},
                        "element_id": {"type": "INTEGER"},
                        "text_to_type": {"type": "STRING"}
                    },
                    "required": ["action_type", "element_id"]
                }
            }
        )

        # Return the parsed JSON dict
        import json
        return json.loads(response.text)