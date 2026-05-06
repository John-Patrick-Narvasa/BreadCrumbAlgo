from fastapi import FastAPI, HTTPException
from models import *
from utils.ai_helper import AtomizerAI
from api.roadmap import RoadmapEngine
from api.rewards import ProgressEngine

app = FastAPI()
ai_boss, map_boss, reward_boss = AtomizerAI(), RoadmapEngine(), ProgressEngine()
db = {"projects": {}} # Simulated DB

@app.post("/projects") # 1. MODIFIED: The "Atomize!" trigger
async def create_project(request: ProjectRequest):
    tasks = await ai_boss.generate_roadmap(request.project_name, request.category)
    nodes = map_boss.construct_tree(tasks)
    project = ProjectRoadmap(project_name=request.project_name, category=request.category, nodes=nodes)
    db["projects"][project.project_id] = project
    return project

@app.patch("/projects/{project_id}") # 2. ADDED: UI Editing
async def edit_project(project_id: str, update: ProjectUpdate):
    project = db["projects"].get(project_id)
    if not project: raise HTTPException(404)
    for key, value in update.dict(exclude_none=True).items():
        setattr(project, key, value)
    return project

@app.post("/tasks/{node_id}/atomize") # 3. ADDED: The Sub-task "+" button
async def atomize_on_the_fly(project_id: str, node_id: str):
    project = db["projects"].get(project_id)
    parent = next(n for n in project.nodes if n.node_id == node_id)
    sub_tasks = await ai_boss.atomize_subtask(parent.title)
    
    new_nodes = []
    for t in sub_tasks:
        new_node = RoadmapNode(title=t, parent_id=node_id, is_locked=False)
        project.nodes.append(new_node)
        new_nodes.append(new_node)
    return new_nodes

@app.get("/dashboard") # 4. ADDED: Populates the Scoreboard
async def get_dashboard():
    return UserDashboard(streak_count=96, total_points=850, level_progress=85.0)