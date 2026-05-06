import os, json
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AtomizerAI:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.0-flash" # Optimized for speed/cost

    async def _determine_scope(self, project_name: str): # 1. ADDED
        prompt = f"Analyze '{project_name}'. Return ONLY JSON: {{'scope': 'SHORT'|'LONG', 'steps': int}}"
        response = self.client.models.generate_content(model=self.model_id, contents=prompt)
        return json.loads(response.text.strip())

    async def generate_roadmap(self, project_name: str, category: str) -> list:
        scope_data = await self._determine_scope(project_name)
        # 2. MODIFIED: Strict ADHD-friendly prompt engineering
        prompt = f"""
        Break '{project_name}' ({category}) into {scope_data['steps']} microscopic steps.
        RULES:
        1. BRAIN-DEAD START: Step 1 must be impossible to fail (e.g., "Open a blank doc").
        2. 15-MINUTE CAP: No step > 15 mins.
        3. VERB-FIRST: Use high-momentum verbs (e.g., "Click", "Draft").
        Return ONLY a JSON array of strings.
        """
        response = self.client.models.generate_content(model=self.model_id, contents=prompt)
        return self._parse_ai_response(response.text)

    async def atomize_subtask(self, parent_task_title: str) -> list: # 3. ADDED
        prompt = f"Break down '{parent_task_title}' into 3 tiny physical actions. JSON array only."
        response = self.client.models.generate_content(model=self.model_id, contents=prompt)
        return self._parse_ai_response(response.text)

    def _parse_ai_response(self, raw_text: str) -> list:
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text) if clean_text else []