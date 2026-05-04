import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AtomizerAI:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_roadmap(self, project_name: str, category: str) -> list:
        prompt = f"""
        Break the project '{project_name}' in category '{category}' into 10 tiny, 15-minute steps.
        First step must be brain-dead easy. Use encouraging language.
        Return ONLY a JSON array of strings.
        Example: ["Step 1", "Step 2"]
        """
        try:
            response = self.model.generate_content(prompt)
            return self._parse_ai_response(response.text)
        except Exception:
            return [f"Start {project_name}", "Gather tools", "Draft ideas", "Step 4", "Step 5", "Step 6", "Step 7", "Step 8", "Step 9", "Final Polish"]

    def _parse_ai_response(self, raw_text: str) -> list:
        try:
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)[:10]
        except:
            return ["Initialization", "Research", "Drafting", "Refining", "Finishing"]