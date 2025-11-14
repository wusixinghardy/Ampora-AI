import os
from typing import List, Union
from PyPDF2 import PdfReader
from src.LLM.ChatGPT import ChatGPTClient


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
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


def generate_learning_objectives(input_data: Union[str, os.PathLike]) -> List[str]:
    """
    Process the input (concept or PDF) and generate very specific learning objectives.
    """
    client = ChatGPTClient()
    system_prompt = (
        "You are an expert curriculum designer. Your job is to break down topics into "
        "extremely specific, step-by-step learning objectives for teaching university-level lectures."
    )

    if isinstance(input_data, str) and os.path.isfile(input_data):
        text_content = extract_text_from_pdf(input_data)
        user_prompt = (
            "The following is extracted content from a textbook or slide. "
            "Generate a numbered list of very specific learning objectives that could form a full lecture. "
            "Don't exceed 10 objectives. Each objective should represent a concrete sub-skill or question the learner must master. "
            "Be concrete — not vague topics. Example: 'Understand what stochastic gradient descent is', "
            "'Derive the SGD update rule', 'Explain how SGD relates to backpropagation', "
            "'Compute gradient on a simple quadratic function using SGD'.\n\n"
            f"CONTENT:\n{text_content}"
        )
    else:
        concept = str(input_data)
        user_prompt = (
            f"Topic: {concept}\n\n"
            "Generate a list of highly specific, logically ordered learning objectives to teach this concept in depth. "
            "Each objective should represent a concrete sub-skill or question the learner must master. "
            "Don't exceed 10 objectives. Each objective should represent a concrete sub-skill or question the learner must master. "
            "Be concrete — not vague topics. Example: 'Understand what stochastic gradient descent is', "
            "'Derive the SGD update rule', 'Explain how SGD relates to backpropagation', "
            "'Compute gradient on a simple quadratic function using SGD'."
        )

    raw_output = client.chat(system_prompt, user_prompt)

    objectives = []
    for line in raw_output.splitlines():
        if line.strip():
            line = line.strip("-•1234567890.) \t")
            if len(line) > 3:
                objectives.append(line)
    return objectives


def generate_lecture_script(objectives: List[str]) -> List[str]:
    """
    Take a list of learning objectives and produce a lecture script divided into slide segments.
    Each element in the returned list is the spoken script for one slide.
    """
    client = ChatGPTClient()

    system_prompt = (
        "You are an enthusiastic and friendly YouTube educator inspired by StatQuest. "
        "Your goal is to teach complex topics in a way that sounds completely natural when read aloud by a voice-over narrator. "
        "All explanations should flow like spoken sentences — smooth, conversational, and free of written formulas or punctuation-heavy text. "
        "Do not include math symbols, equations, or long numeric expressions. Instead, describe them in words. "
        "Avoid lists, hyphens, or markdown formatting. Write in full sentences using transitions like "
        "'first,' 'then,' 'next,' 'finally,' or 'in other words.' "
        "Your lecture must follow this logical structure:\n"
        "1. What is [the topic]\n"
        "2. Why it is important (Where or in what applications it is used)\n"
        "3. Details and step-by-step reasoning\n"
        "4. Summary and key takeaway.\n"
        "However, divide your output into multiple slide segments — each slide containing one coherent spoken section. "
        "Each slide should feel like a small chapter explaining different objective in the lecture. "
        "At the start of each new slide, include a natural transition from the previous one, like "
        "'Now that we’ve covered the basics,' or 'Let’s move on to the next part.' "
        "At the end of the last slide, wrap up with a friendly, verbal conclusion. "
        "The final output must be in valid JSON format, where each slide number maps to its script, for example:\n"
        "{\n"
        "  'Slide 1': 'Introduction and explanation...',\n"
        "  'Slide 2': 'Transition and deeper explanation...',\n"
        "  'Slide 3': 'Summary and wrap-up...'\n"
        "}"
    )

    joined_objectives = "\n".join([f"- {obj}" for obj in objectives])

    user_prompt = (
        f"Here are the learning objectives for this lecture:\n{joined_objectives}\n\n"
        "Please generate a full lecture script following the structure and tone described above. "
        "Divide it naturally into slide segments, with smooth transitions between slides. "
        "Each slide should contain the narration text for that section and be labeled clearly as a JSON object "
        "where keys are 'Slide 1', 'Slide 2', etc. "
        "Ensure the speech flows naturally across slides when read aloud by a voice-over."
    )

    raw_output = client.chat(system_prompt, user_prompt)

    import json
    slides = []
    try:
        parsed = json.loads(raw_output)
        for key in sorted(parsed.keys()):
            slides.append(parsed[key].strip())
    except json.JSONDecodeError:
        current_slide = []
        for line in raw_output.splitlines():
            if "Slide" in line and ":" in line:
                if current_slide:
                    slides.append(" ".join(current_slide).strip())
                    current_slide = []
            else:
                current_slide.append(line.strip())
        if current_slide:
            slides.append(" ".join(current_slide).strip())

    return slides



def generate_bulletpoints(slide_scripts: List[str]) -> dict:
    """
    Generate concise bullet points for each slide based on its narration script.
    Each key in the returned dictionary corresponds to 'Slide X',
    and its value is a list of short, clear bullet points summarizing that slide.
    """

    client = ChatGPTClient()

    system_prompt = (
        "You are an expert in instructional design and summarization. "
        "Your job is to transform each spoken-style slide narration into concise, readable bullet points "
        "that can be displayed on PowerPoint or presentation slides. "
        "The goal is to capture the essence of each slide into short, punchy bullet points like in a lecture slide. "
        "Use simple, readable phrases — not full sentences — and avoid punctuation-heavy or academic phrasing. "
        "Use equations, math symbols, or code when necessary. "
        "Keep the wording short and visually clean for slide readability."
    )

    slides_text = "\n\n".join([
        f"Slide {i+1}:\n{script}" for i, script in enumerate(slide_scripts)
    ])

    user_prompt = (
        f"The following are the voice-over narrations for each slide in a lecture:\n\n{slides_text}\n\n"
        "For each slide, summarize the key ideas as bullet points suitable for slides. "
        "Return the result in valid JSON format, where each key is 'Slide 1', 'Slide 2', etc., "
        "and each value is a list of short bullet point strings. Example:\n"
        "{\n"
        "  'Slide 1': ['Definition of SGD', 'Optimization by small updates', 'Uses mini-batches'],\n"
        "  'Slide 2': ['Why SGD matters', 'Efficient for large datasets']\n"
        "}"
    )

    raw_output = client.chat(system_prompt, user_prompt)

    import json
    bulletpoints = {}
    try:
        bulletpoints = json.loads(raw_output)
    except json.JSONDecodeError:
        bulletpoints = {}
        current_slide = None
        for line in raw_output.splitlines():
            line = line.strip()
            if line.startswith("Slide "):
                current_slide = line.split(":")[0]
                bulletpoints[current_slide] = []
            elif current_slide and line:
                cleaned = line.strip("-•1234567890. \t")
                if len(cleaned) > 2:
                    bulletpoints[current_slide].append(cleaned)
    return bulletpoints


if __name__ == "__main__":
    topic = "Stochastic Gradient Descent"
    objectives = generate_learning_objectives(topic)
    print("\n🎯 LEARNING OBJECTIVES:\n", objectives)

    print("\n---\n🎬 GENERATING LECTURE SCRIPT (divided into slides)...\n")
    slides = generate_lecture_script(objectives)
    for i, s in enumerate(slides, 1):
        print(f"\n🟩 Slide {i}:\n{s}\n")

    print("\n---\n📊 GENERATING BULLET POINTS FOR EACH SLIDE...\n")
    bullets = generate_bulletpoints(slides)
    for slide, pts in bullets.items():
        print(f"\n{slide}:")
        for p in pts:
            print(f" - {p}")