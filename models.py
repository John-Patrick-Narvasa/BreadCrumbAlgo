from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class RoadmapNode(BaseModel):
    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None 
    title: str
    description: Optional[str] = None
    is_locked: bool = True
    is_completed: bool = False
    node_type: str = "breadcrumb" 
    xp_value: int = 150

class ProjectRoadmap(BaseModel):
    project_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str
    category: str
    description: Optional[str] = "No description provided." 
    tags: List[str] = [] 
    nodes: List[RoadmapNode]
    current_streak: int = 0
    total_progress: float = 0.0

class ProjectRequest(BaseModel):
    project_name: str
    category: str

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None

class RewardUpdate(BaseModel):
    project_id: str
    node_id: str
    session_minutes: int
    is_pomodoro_complete: bool = True

class UserDashboard(BaseModel):
    streak_count: int = 5
    total_points: int = 500
    level_progress: float = 45.5