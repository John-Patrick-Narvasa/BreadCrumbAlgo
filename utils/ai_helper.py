import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AtomizerAI:
    def __init__(self):
        # The new SDK automatically looks for GOOGLE_API_KEY in env
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.5-flash"

    async def _determine_scope(self, project_name: str) -> str:
        prompt = f"Categorize the project '{project_name}' as 'SHORT' or 'LONG'. Return only the word."
        try:
            # New SDK syntax: models.generate_content
            response = self.client.models.generate_content(
                model=self.model_id, 
                contents=prompt
            )
            return response.text.strip().upper()
        except Exception as e:
            print(f"Scope Error: {e}")
            return "LONG"

    async def generate_roadmap(self, project_name: str, category: str) -> list:
        scope = await self._determine_scope(project_name)
        scope_instruction = "the entire project" if scope == "SHORT" else "only the FIRST PHASE"

        prompt = f"""
        Break '{project_name}' ({category}) into tiny, 15-minute steps.
        Focus on {scope_instruction}.
        Return ONLY a JSON array of strings. 
        Example: ["Step 1", "Step 2"]
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id, 
                contents=prompt
            )
            return self._parse_ai_response(response.text)
        except Exception as e:
            print(f"Generation Error: {e}")
            # Dynamic fallback that at least uses the project name
            return [f"Plan {project_name}", "Gather materials", "Setup workspace", "Step 4", "Step 5", "Step 6", "Step 7", "Step 8", "Step 9", "Final Review"]

    def _parse_ai_response(self, raw_text: str) -> list:
        try:
            # The new SDK is better at stripping markdown, but we'll be safe
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
            tasks = json.loads(clean_text)
            return tasks[:10]
        except Exception as e:
            print(f"Parsing Error: {e}")
            return ["Start", "Research", "Draft", "Refine", "Complete"]