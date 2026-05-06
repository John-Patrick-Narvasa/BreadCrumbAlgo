### Finalized API Route List

Following your architecture, here is the complete, production-ready list:

#### **Project Management**

* **`GET /projects`** : List all projects for the top tabs.
* **`POST /projects`** : Create new project + Initial AI Atomization.
* **`GET /projects/{id}`** : Fetch full tree for the Roadmap panel.
* **`PATCH /projects/{id}`** : Edit title, category, or tags.
* **`DELETE /projects/{id}`** : Remove project.

#### **Task & Roadmap Logic**

* **`POST /tasks`** : Manual task addition (supports `parent_id`).
* **`PATCH /tasks/{id}`** : Edit task title or description.
* **`DELETE /tasks/{id}`** : Remove a breadcrumb.
* **`POST /tasks/{id}/complete`** : Mark as done and trigger XP calculation.
* **`POST /tasks/{id}/atomize`** : The "Sub-Atomizer" for specific nodes.

#### **Timer & Rewards (The "Dopamine" Layer)**

* **`GET /dashboard`** : Current streak, total XP, and level progress.
* **`POST /timer/start`** : Record start of a Flowtime session.
* **`POST /timer/stop`** : End session and reward "Flow Bonus" XP.
