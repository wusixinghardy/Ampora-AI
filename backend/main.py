from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.llm_client import generate_llm_response
from src import career_logic, resume_parser

app = FastAPI(
    title="AI Career Tutor API",
    description="Backend API for AI Career Tutor (career pathing, resume feedback, mock interviews)",
    version="0.1.0",
)

# --- Allow frontend (Vite dev server, etc.) to call us ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, lock this down to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request / Response Models ----------

class CareerPlanRequest(BaseModel):
    major: str
    skills: list[str]
    target_roles: list[str]

class CareerPlanResponse(BaseModel):
    summary: str
    timeline: list[str]          # ["Next 1-2 months: ...", "This semester: ...", ...]
    projects: list[str]          # recommended portfolio projects
    talking_points: list[str]    # things to say in interviews

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    target_role: str

class ResumeAnalysisResponse(BaseModel):
    strengths: list[str]
    gaps: list[str]
    bullet_fix_suggestions: list[str]

class MockInterviewRequest(BaseModel):
    role: str
    user_answer: str

class MockInterviewResponse(BaseModel):
    follow_up_question: str
    critique: str
    improvement_example: str


# ---------- Routes ----------

@app.post("/generate-career-plan", response_model=CareerPlanResponse)
def generate_career_plan(req: CareerPlanRequest):
    try:
        llm_output = career_logic.create_career_plan(
            major=req.major,
            skills=req.skills,
            target_roles=req.target_roles,
        )
        return llm_output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-resume", response_model=ResumeAnalysisResponse)
def analyze_resume(req: ResumeAnalysisRequest):
    try:
        llm_output = resume_parser.analyze_resume(
            resume_text=req.resume_text,
            target_role=req.target_role,
        )
        return llm_output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mock-interview", response_model=MockInterviewResponse)
def mock_interview(req: MockInterviewRequest):
    try:
        prompt = (
            f"You are an interviewer for {req.role}.\n"
            f"The candidate answered:\n{req.user_answer}\n\n"
            "1. Give one tough follow-up question.\n"
            "2. Critique their answer like a senior hiring manager.\n"
            "3. Rewrite a stronger sample answer in first person.\n"
        )

        result = generate_llm_response(prompt)

        # Extremely dumb parsing to make JSON. Later you can get fancy / structured.
        # For now we just split sections by heuristics.
        return MockInterviewResponse(
            follow_up_question=result.get("follow_up_question", ""),
            critique=result.get("critique", ""),
            improvement_example=result.get("improvement_example", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}
