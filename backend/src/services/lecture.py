import os
import json
from typing import List, Union, Dict, Any, Tuple
from PyPDF2 import PdfReader
from src.LLM.ChatGPT import ChatGPTClient


# -----------------------------------------------------------
# PDF EXTRACTION
# -----------------------------------------------------------

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    text = []
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text.append(content)
    return "\n".join(text)


# -----------------------------------------------------------
# SMALL JSON HELPERS
# -----------------------------------------------------------

def normalize_json_array(raw: str) -> List[Dict[str, Any]]:
    """
    Try to parse a JSON array from raw model output.
    Includes safety checks for truncation / missing brackets.
    """
    if "[" not in raw or "]" not in raw:
        raise ValueError("Model returned no recognizable JSON array.")

    start = raw.find("[")
    end = raw.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError("JSON array not found in model output.")

    cleaned = raw[start:end]
    return json.loads(cleaned)


# -----------------------------------------------------------
# GENERATE LEARNING OBJECTIVES
# -----------------------------------------------------------

def generate_learning_objectives(input_data: Union[str, os.PathLike]) -> List[str]:
    """
    Input can be:
    - A topic string
    - A PDF path

    Output:
    - List[str] of 8–12 very clear, concrete learning objectives
    """

    client = ChatGPTClient()

    system_prompt = (
        "You are an expert curriculum designer. Break topics into extremely specific, "
        "step-by-step learning objectives. Assume the audience has no prior background. "
        "Each objective must be a concrete skill, not a vague theme."
    )

    if isinstance(input_data, str) and os.path.isfile(input_data):
        text_content = extract_text_from_pdf(input_data)
        user_prompt = (
            "Extracted textbook/slide content is provided below.\n"
            "Generate no more than 10 very specific learning objectives. Succinct is better "
            "Each objective must describe one concrete question or subskill.\n\n"
            f"CONTENT:\n{text_content}"
        )
    else:
        concept = str(input_data)
        user_prompt = (
            f"Topic: {concept}\n\n"
            "Generate no more than 10 highly specific, logically ordered learning objectives. Succinct is better"
            "Each objective must be a concrete sub-skill or question.\n"
            "Example: 'Explain how mini-batch gradients are unbiased', "
            "'Derive the SGD update rule', 'Compute SGD steps on a simple function'."
        )

    raw_output = client.chat(system_prompt, user_prompt)

    objectives = []
    for line in raw_output.splitlines():
        if line.strip():
            cleaned = line.strip("-•1234567890.) \t")
            if len(cleaned) > 3:
                objectives.append(cleaned)

    return objectives


# -----------------------------------------------------------
# STAGE 1: GENERATE SLIDE PLAN (TITLES ONLY)
# -----------------------------------------------------------

def generate_slide_plan(objectives: List[str]) -> List[Dict[str, Any]]:
    """
    Produce a globally consistent plan of slides BEFORE generating full scripts.
    """
    client = ChatGPTClient()
    joined_objectives = "\n".join([f"{i+1}. {obj}" for i, obj in enumerate(objectives)])

    system_prompt = (
        """
        You are an enthusiastic and friendly educator who teaches complex academic topics 
        in a clear, structured, and highly engaging way. You combine the clarity of a great 
        YouTube teacher with the rigor of a university lecturer.

        Your job right now is NOT to write the lecture. 
        Your job is ONLY to plan the slide sequence for the full lecture.

        === GLOBAL REQUIREMENTS ===
        - Your planning must be globally consistent across the entire lecture.
        - The tone, pacing, and narrative logic should feel unified.
        - You MUST produce a coherent progression from basic ideas → deeper concepts → applications → examples.
        - You MUST include an explicit Opening Slide at the start and an End Slide at the finish.

        === PLANNING GOALS ===
        - Produce a comprehensive slide plan that covers all objectives.
        - The total slide count MUST be NO MORE THAN 22 slides.
        - Generate necessary content only: be thorough on the core topic but do not expand into tangential areas.
        - Each learning objective should expand into multiple slides as needed.
        - Slides should be atomic: each slide expresses exactly ONE idea.

        === OUTPUT FORMAT ===
        Return ONLY a JSON array of slide plan objects.
        Use double quotes for all keys and values.

        Example:
        [
            {
                "objective_index": 0,
                "objective": "Introduction",
                "slide_index_within_objective": 1,
                "title": "Opening: Lecture Overview"
            },
            {
                "objective_index": 1,
                "objective": "Describe the historical context",
                "slide_index_within_objective": 1,
                "title": "Historical Background (1.1)"
            }
        ]
        """
    )

    user_prompt = (
        "Here are the learning objectives for a full lecture:\n\n"
        f"{joined_objectives}\n\n"
        "Create a globally consistent SLIDE PLAN.\n"
        "Return ONLY the JSON array."
    )

    raw = client.chat(system_prompt, user_prompt)

    try:
        plan = json.loads(raw)
    except json.JSONDecodeError:
        plan = normalize_json_array(raw)

    return plan


# -----------------------------------------------------------
# STAGE 2: GENERATE FULL SLIDE CONTENT FROM PLAN
# -----------------------------------------------------------

def generate_slide_content(slide_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    client = ChatGPTClient()

    plan_json = json.dumps(slide_plan, ensure_ascii=False, indent=2)

    system_prompt = (
        """
        You are an enthusiastic and friendly educator who explains topics clearly, 
        rigorously, and in a spoken-narration style appropriate for a video lecture inspired by
        the style of StatQuest.

        === GLOBAL STYLE REQUIREMENTS ===
        - Entire lecture must feel globally consistent.
        - Spoken, conversational tone but rigorously correct.
        - Very detailed explanations (but no more than 12 sentences per slide).
        - Convert ALL mathematical notation into spoken English.
        - NO latex, NO formulas, NO math symbols.
        - NO markdown inside narration text.
        - Smooth transitions between slides.

        === SLIDE REQUIREMENTS ===
        For EACH slide in the plan, produce a JSON object.
        Return ONLY a JSON array.

        Example:
        [
          {
            "objective_index": 1,
            "slide_index_within_objective": 1,
            "title": "Historical Context",
            "script": "Welcome to the first slide...",
            "visualization": "A timeline showing...",
            "bulletpoints": ["Key event 1", "Key event 2"]
          }
        ]
    """
    )

    user_prompt = (
        "Here is the slide plan JSON:\n\n"
        f"{plan_json}\n\n"
        "Fill in the complete content for EVERY slide.\n"
        "Return ONLY the JSON array."
    )


    raw = client.chat(system_prompt, user_prompt)

    try:
        slides = json.loads(raw)
    except json.JSONDecodeError:
        slides = normalize_json_array(raw)

    return slides

# -----------------------------------------------------------
# EXTRACTION UTILITIES
# -----------------------------------------------------------

def get_scripts(slides: List[Dict[str, Any]]) -> List[str]:
    return [slide.get("script", "") for slide in slides]


def get_visual_descriptions(slides: List[Dict[str, Any]]) -> List[str]:
    return [slide.get("visualization", "") for slide in slides]


def get_bulletpoints(slides: List[Dict[str, Any]]) -> List[List[str]]:
    return [slide.get("bulletpoints", []) for slide in slides]


# -----------------------------------------------------------
# MAIN TESTING
# -----------------------------------------------------------

if __name__ == "__main__":
    topic = "Balance Sheet"

    print("\n🎯 LEARNING OBJECTIVES:")
    objectives = generate_learning_objectives(topic)
    print(objectives)

    print("\n---\n🧩 GENERATING SLIDE PLAN...")
    plan = generate_slide_plan(objectives)
    print(f"Planned slide count: {len(plan)}")

    print("\n---\n🎬 GENERATING FULL LECTURE FROM PLAN...")
    slides = generate_slide_content(plan)
    print(f"Generated slide count: {len(slides)}")

    scripts = get_scripts(slides)
    visuals = get_visual_descriptions(slides)
    bullets = get_bulletpoints(slides)

    for i, slide in enumerate(slides, start=1):
        print(f"\n🟩 Slide {i} — {slide['title']}")
        print("Script:\n", slide["script"])
        print("Visualization:\n", slide["visualization"])
        print("Bulletpoints:")
        for bp in slide["bulletpoints"]:
            print(" -", bp)