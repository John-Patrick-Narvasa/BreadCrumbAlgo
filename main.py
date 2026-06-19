from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import *
from utils.ai_helper import AtomizerAI
from api.roadmap import RoadmapEngine
from api.rewards import ProgressEngine

app = FastAPI(title="The Breadcrumber API")

# 1. ADDED: Essential CORS for React Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_boss = AtomizerAI()
map_boss = RoadmapEngine()
reward_boss = ProgressEngine()

# Simulated Database
db = {
    "projects": {},
    "user_stats": {"streak": 96, "xp": 850}, # Matches photo_2026-05-06_17-25-47.jpg
    "active_timer": None 
}

# ─── PROJECT MANAGEMENT (5 ROUTES) ───

@app.get("/projects")
async def get_projects():
    """Route: List all projects for the top tabs."""
    return [
        {"id": p.project_id, "name": p.project_name, "category": p.category} 
        for p in db["projects"].values()
    ]

@app.post("/projects", response_model=ProjectRoadmap)
async def create_project(request: ProjectRequest):
    """Route: Create new project + Initial AI Atomization."""
    # AI generates the high-level roadmap
    tasks = await ai_boss.generate_roadmap(request.project_name, request.category)
    nodes = map_boss.construct_tree(tasks)
    
    project = ProjectRoadmap(
        project_name=request.project_name, 
        category=request.category, 
        nodes=nodes
    )
    db["projects"][project.project_id] = project
    return project

@app.get("/projects/{project_id}", response_model=ProjectRoadmap)
async def get_project(project_id: str):
    """Route: Fetch full tree for the Roadmap panel."""
    if project_id not in db["projects"]:
        raise HTTPException(status_code=404, detail="Project not found")
    return db["projects"][project_id]

@app.patch("/projects/{project_id}")
async def edit_project(project_id: str, update: ProjectUpdate):
    """Route: Edit title, category, or tags in the UI header."""
    project = db["projects"].get(project_id)
    if not project:
        raise HTTPException(404)
    # Update only provided fields
    for key, value in update.dict(exclude_none=True).items():
        setattr(project, key, value)
    return project

@app.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Route: Remove project."""
    if project_id in db["projects"]:
        del db["projects"][project_id]
        return {"status": "deleted"}
    raise HTTPException(404)

# ─── TASK & ROADMAP LOGIC (5 ROUTES) ───

@app.post("/tasks")
async def add_task(project_id: str, title: str, parent_id: Optional[str] = None):
    """Route: Manual task addition (supports parent_id for nesting)."""
    project = db["projects"].get(project_id)
    new_node = RoadmapNode(title=title, parent_id=parent_id, is_locked=False)
    project.nodes.append(new_node)
    return new_node

@app.patch("/tasks/{node_id}")
async def edit_task(project_id: str, node_id: str, title: Optional[str] = None):
    """Route: Edit task title or description."""
    project = db["projects"].get(project_id)
    node = next((n for n in project.nodes if n.node_id == node_id), None)
    if title: node.title = title
    return node

@app.delete("/tasks/{node_id}")
async def delete_task(project_id: str, node_id: str):
    """Route: Remove a breadcrumb."""
    project = db["projects"].get(project_id)
    project.nodes = [n for n in project.nodes if n.node_id != node_id]
    return {"status": "success"}

@app.post("/tasks/{node_id}/complete")
async def complete_task(project_id: str, node_id: str, update: RewardUpdate):
    """Route: Mark as done and trigger XP calculation."""
    # 1. Update node status
    project = db["projects"].get(project_id)
    node = next((n for n in project.nodes if n.node_id == node_id), None)
    node.is_completed = True
    
    # 2. Calculate Rewards
    xp = reward_boss.calculate_xp(update.session_minutes, update.is_pomodoro_complete)
    db["user_stats"]["xp"] += xp
    return {"gained_xp": xp, "total_xp": db["user_stats"]["xp"]}

@app.post("/tasks/{node_id}/atomize")
async def atomize_on_the_fly(project_id: str, node_id: str):
    """Route: The Sub-task '+' button for specific nodes."""
    project = db["projects"].get(project_id)
    parent = next(n for n in project.nodes if n.node_id == node_id)
    
    # AI breaks the specific parent task down
    sub_tasks = await ai_boss.atomize_subtask(parent.title)
    
    new_nodes = []
    for t in sub_tasks:
        new_node = RoadmapNode(title=t, parent_id=node_id, is_locked=False)
        project.nodes.append(new_node)
        new_nodes.append(new_node)
    return new_nodes

# ─── TIMER & REWARDS (3 ROUTES) ───

@app.get("/dashboard", response_model=UserDashboard)
async def get_dashboard():
    """Route: Current streak, total XP, and level progress for Scoreboard."""
    progress = reward_boss.get_dashboard_state(db["user_stats"]["xp"])
    return UserDashboard(
        streak_count=db["user_stats"]["streak"],
        total_points=db["user_stats"]["xp"],
        level_progress=progress
    )

@app.post("/timer/start")
async def start_timer(project_id: str, node_id: str):
    """Route: Record start of a Flowtime session."""
    db["active_timer"] = {"start": "now", "node": node_id} # Mock timestamp
    return {"status": "Timer started"}

@app.post("/timer/stop")
async def stop_timer():
    """Route: End session and reward 'Flow Bonus' XP."""
    db["active_timer"] = None
    return {"status": "Timer stopped", "bonus_xp": 50}