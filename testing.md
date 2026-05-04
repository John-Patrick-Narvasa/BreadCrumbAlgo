
### Core Variables to Track

When you move to the "Real Logic" phase, keep these variables in mind:

* **`flow_session_start`** : Timestamp when the user starts the Pomodoro/Flow timer.
* **`breadcrumb_index`** : Where the user currently is on their visual roadmap.
* **`streak_count`** : Integer representing consecutive days of "breadcrumb eating."
* **`xp_total`** : The cumulative "level" of the user.

### Why this structure?

1. **FastAPI** automatically generates documentation for these routes. Once you run this, you can go to `/docs` in your browser and see a functional UI to test your endpoints.
2. **Pydantic Models** prevent the "Garbage In, Garbage Out" problem. If the frontend forgets to send the `category`, the API will send a clear error message instead of crashing.

## 5. Testing Plan

As the Architect, you cannot assume the code works just because it runs. You need to test three specific failure points:

### A. The "AI Hallucination" Test

**Scenario:** You ask the AI for a roadmap for "Building a Time Machine."
**Goal:** Does your code crash if the AI returns weird text instead of JSON?
**Test:** Use a `try-except` block around `json.loads()` to catch formatting errors and return a "Standard Backup Roadmap" if the AI fails.

### B. The Endpoint Test (Using Swagger)

FastAPI has a secret weapon:  **Interactive Docs** .

1. Run your server: `uvicorn main:app --reload`
2. Go to `http://127.0.0.1:8000/docs`
3. You will see a UI where you can click "Try it out" on your `/generate-roadmap` endpoint. This allows you to test the Python logic without having a single line of React code finished.

### C. The ADHD-Check (Logic Validation)

**Scenario:** A user enters "Write a 500-page Novel."
**Test:** Check the AI output. If a task says "Write first 3 chapters," the logic  **failed** . A breadcrumb should be "Write 100 words" or "Outline one character's hair color." You may need to tweak the `prompt` variable in Step 4 until the tasks stay tiny.
