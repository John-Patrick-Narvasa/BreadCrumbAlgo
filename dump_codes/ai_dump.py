class ProgressEngine:
    def __init__(self):
        self.xp_multiplier = 10 # 10 XP per 1 minute of flow

    def calculate_xp(self, minutes_worked: int) -> int:
        """Calculate XP based on Flowtime."""
        pass

    def check_streak_status(self, last_login_date: str) -> bool:
        """Logic to see if the user's Duolingo-style streak is maintained."""
        pass

    def generate_certificate_data(self, project_name: str, total_hours: float):
        """Prepares data for the final PDF/Image certificate."""
        # Variables: completion_timestamp, user_rank, total_breadcrumbs_eaten
        pass


class RoadmapEngine:
    def __init__(self):
        # Variables for "Duolingo-style" visual logic
        self.max_breadcrumbs = 10
    
    def construct_visual_path(self, tasks: list) -> list:
        """
        Input: Raw strings from the AI.
        Process: 
            1. Assigns a sequential ID.
            2. Assigns a 'type' (e.g., 'Normal Step', 'Milestone', 'Boss Task').
            3. (Optional) Assigns X/Y coordinates for a zigzag visual path.
        Output: A list of dict objects for the Frontend.
        """
        # Method: _calculate_node_position()
        # Method: _assign_milestones()
        pass

    def get_progress_percentage(self, project_id: str) -> float:
        """
        Calculates: (Completed Tasks / Total Tasks) * 100
        """
        pass



class AtomizerAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "gemini-1.5-flash" # or "gpt-4o"

    def generate_roadmap(self, project_name: str, category: str) -> list:
        """
        Input: Project Name and Category
        Process: Formulates the 'Strict JSON' prompt for the AI
        Output: A raw list of strings (tasks)
        """
        # Method: _build_prompt()
        # Method: _call_ai_api()
        pass

    def _parse_ai_response(self, raw_text: str) -> list:
        """Clean the AI output to ensure it's valid JSON."""
        pass


from pydantic import BaseModel
from typing import List, Optional

class ProjectRequest(BaseModel):
    project_name: str
    category: str
    difficulty: Optional[str] = "beginner"

class BreadcrumbTask(BaseModel):
    id: int
    task_description: str
    estimated_minutes: int = 15
    is_completed: bool = False

class ProjectRoadmap(BaseModel):
    project_id: str
    project_name: str
    category: str
    nodes: List[RoadmapNode]   # Replaces List[BreadcrumbTask]
    current_streak: int        # Fetched from user data for visual encouragement
    total_progress: float      # Percentage (e.g., 20.0 for 2/10 tasks)

class RewardUpdate(BaseModel):
    user_id: str
    task_id: int
    session_minutes: int
    is_pomodoro_complete: bool = True # Bonus XP if they didn't break the timer
    current_xp_total: int             # To return the updated level immediately

class RoadmapNode(BaseModel):
    node_id: int
    title: str
    is_locked: bool = True     # Logic: Locked until the previous node is done
    is_completed: bool = False
    node_type: str = "breadcrumb" # Options: 'start', 'milestone', 'finish'
    position_index: int        # Helps React know where to put it on the zigzag path
    xp_value: int = 150        # Specific dopamine reward for this node


class MilestoneReward(BaseModel):
    milestone_id: int
    reward_type: str = "badge" # e.g., 'Bronze Pen', 'Code Spark'
    message: str               # "You've laid the foundation!"


from fastapi import FastAPI
# Import your models and engines here

app = FastAPI(title="The Breadcrumber API")

@app.post("/atomize", response_model=RoadmapResponse)
async def create_roadmap(request: ProjectRequest):
    """
    Route: Takes a project name and returns the 10 tiny breadcrumbs.
    """
    # Logic: Initialize AtomizerAI -> Get Tasks -> Return RoadmapResponse
    pass

@app.post("/complete-task")
async def complete_task(update: RewardUpdate):
    """
    Route: Updates XP and checks for level-ups when a task is finished.
    """
    # Logic: Initialize ProgressEngine -> Calculate XP -> Update DB
    pass

@app.get("/certificate/{project_id}")
async def get_certificate(project_id: str):
    """
    Route: Returns the data needed to show the 'Big Win' certificate.
    """
    pass

@app.get("/health")
def check_health():
    return {"status": "online", "version": "1.0.0"}