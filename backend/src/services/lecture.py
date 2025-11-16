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


def generate_lecture_script(objectives: List[str]) -> List[List[str]]:
    """
    Take a list of learning objectives and produce a lecture script divided into slide segments.
    Each element in the returned list is [script_text, visualization_description] for that slide.
    """
    client = ChatGPTClient()

    system_prompt = (
    "You are an enthusiastic and friendly YouTube educator inspired by StatQuest, "
    "but you also explain topics with the depth and precision of a university professor. "
    "Your goal is to teach complex technical topics in a way that is spoken, natural, "
    "detailed, and deeply thorough. The final narration should be something a voice-over "
    "could read smoothly and clearly. \n\n"

    "Your style requirements:\n"
    "- Spoken, conversational tone, but still rigorous and precise.\n"
    "- Very detailed explanations — as detailed as a full lecture.\n"
    "- When describing math, convert symbols to spoken form, such as 'theta equals zero'.\n"
    "- Avoid symbols entirely (no latex, no formulas, no symbols like ∇, Σ, etc.).\n"
    "- Avoid bullet lists, markdown formatting, or hyphen-style enumerations.\n"
    "- Use transitions like 'first', 'next', 'now let’s walk through', 'to make this concrete', "
    "'in practice', 'what this really means is'.\n"
    "- Each slide must be long, thorough, and multi-paragraph. Don't shorten anything.\n\n"

    "Slide structure requirements:\n"
    "1. Start with: what the topic is, in spoken explanation.\n"
    "2. Then: why the topic is important, where it is used, and why people should care.\n"
    "3. Then: rich, multi-paragraph technical detail with examples, analogies, and step-by-step reasoning.\n"
    "4. The slides should roughly follow the learning objectives, but in narrative form.\n"
    "5. The narration should be as long and detailed as a real lecture segment.\n"
    "6. Before each slide, include a smooth spoken transition from the previous slide.\n"
    "7. The final slide should end with a warm spoken conclusion.\n\n"

    "Visualization requirement for each slide:\n"
    "Along with the narration, you must produce a clear, specific visualization description that explains exactly "
    "what diagrams, animations, charts, or graphical elements should appear on that slide. "
    "These descriptions must be very detailed so that another teammate can build them without guessing. "
    "Each visualization should match the concepts explained in that slide.\n\n"

    "Output format requirement:\n"
    "You must output valid JSON. Each slide is a JSON object with two fields:\n"
    "  'script': the detailed narration text for that slide\n"
    "  'visualization': a detailed description of what visuals should appear on that slide\n\n"

    "Example output (format only, not content):\n"
    "{\n"
    "  'Slide 1': {\n"
    "      'script': 'Very long spoken narration...',\n"
    "      'visualization': 'Detailed visual description...'\n"
    "  },\n"
    "  'Slide 2': {\n"
    "      'script': 'Transition into next topic followed by detailed narration...',\n"
    "      'visualization': 'Another detailed visual description...'\n"
    "  }\n"
    "}\n\n"

    "Most important instruction: The narration must be long, deeply detailed, and rich — "
    "not brief summaries. Write as if this is a full multi-minute lecture per slide."
    )

    joined_objectives = "\n".join([f"- {obj}" for obj in objectives])

    user_prompt = (
    f"Here are the learning objectives for this lecture:\n{joined_objectives}\n\n"
    "Generate a long, detailed lecture divided into multiple slides. Follow all style, structure, and output "
    "requirements from the system prompt. Each slide must be several paragraphs long, explaining the concept "
    "with clarity, intuition, examples, and step-by-step reasoning.\n\n"
    "Each slide MUST contain:\n"
    "- A 'script' field: the voice-over narration that is long, rich, and highly detailed.\n"
    "- A 'visualization' field: a very detailed description of exactly what visuals should appear on that slide.\n\n"
    "The number of slides is up to you, but you must cover all learning objectives thoroughly. "
    "Ensure extremely smooth transitions between slides, and ensure the entire lecture flows like a full-length class.\n\n"
    "Return ONLY a valid JSON object with 'Slide 1', 'Slide 2', etc. "
    "Each slide's content must follow the format specified in the system prompt."
    )

    raw_output = client.chat(system_prompt, user_prompt)

    import json
    slides_output = []
    try:
        parsed = json.loads(raw_output)
        for key in sorted(parsed.keys()):
            slide_data = parsed[key]
            script = slide_data.get("script", "").strip()
            viz = slide_data.get("visualization", "").strip()
            slides_output.append([script, viz])
    except json.JSONDecodeError:
        # Fallback parsing if GPT fails JSON format
        current_script, current_viz = [], []
        current_mode = None
        for line in raw_output.splitlines():
            line = line.strip()
            if "Slide" in line and ":" in line:
                if current_script or current_viz:
                    slides_output.append([" ".join(current_script).strip(), " ".join(current_viz).strip()])
                    current_script, current_viz = [], []
            elif line.lower().startswith("script"):
                current_mode = "script"
            elif line.lower().startswith("visualization"):
                current_mode = "visualization"
            elif current_mode == "script":
                current_script.append(line)
            elif current_mode == "visualization":
                current_viz.append(line)
        if current_script or current_viz:
            slides_output.append([" ".join(current_script).strip(), " ".join(current_viz).strip()])

    return slides_output


def generate_bulletpoints(slides: List[List[str]]) -> dict:
    """
    Generate concise bullet points for each slide based on its narration script.
    Input slides: List of [script, visualization] for each slide.
    Output: dict mapping slide number -> list of bullet points.
    """

    client = ChatGPTClient()

    system_prompt = (
        "You are an expert in instructional design and summarization. "
        "Your job is to transform each spoken-style slide narration into concise, readable bullet points "
        "that can be displayed on presentation slides. "
        "Bullet points should be short, punchy, visually clean, and easy to read. "
        "Avoid long sentences. Use math symbols only when absolutely needed."
    )

    # Build a readable prompt for GPT
    slides_text = ""
    for idx, (script, visualization) in enumerate(slides, start=1):
        slides_text += f"Slide {idx}:\n"
        slides_text += f"Narration:\n{script}\n"
        slides_text += f"Visualization description:\n{visualization}\n\n"

    user_prompt = (
        f"The following are the narration and visualization descriptions for each slide:\n\n{slides_text}\n"
        "For each slide, summarize the key ideas as bullet points suitable for presentation slides. "
        "Return the result in valid JSON format, where each key is 'Slide 1', 'Slide 2', etc., "
        "and each value is a list of short bullet point strings. Example:\n"
        "{\n"
        "  'Slide 1': ['Definition of SGD', 'How it updates weights'],\n"
        "  'Slide 2': ['Why SGD is useful', 'Where it is applied']\n"
        "}"
    )

    raw_output = client.chat(system_prompt, user_prompt)

    import json
    try:
        bulletpoints = json.loads(raw_output)
    except json.JSONDecodeError:
        # fallback text parser
        bulletpoints = {}
        current_slide = None
        for line in raw_output.splitlines():
            line = line.strip()
            if line.startswith("Slide "):
                current_slide = line.split(":")[0]
                bulletpoints[current_slide] = []
            elif current_slide and line:
                cleaned = line.strip("-•1234567890.) \t")
                if len(cleaned) > 2:
                    bulletpoints[current_slide].append(cleaned)
    return bulletpoints


if __name__ == "__main__":
    topic = "Stochastic Gradient Descent"

    print("\n🎯 LEARNING OBJECTIVES:")
    objectives = generate_learning_objectives(topic)
    print(objectives)

    print("\n---\n🎬 GENERATING LECTURE SCRIPT (SLIDE STRUCTURE)...")
    slides = generate_lecture_script(objectives)
    for i, pair in enumerate(slides, start=1):
        script, viz = pair
        print(f"\n🟩 Slide {i} Script:\n{script}")
        print(f"🖼️ Slide {i} Visualization:\n{viz}")

    print("\n---\n📊 GENERATING BULLET POINTS...")
    bullets = generate_bulletpoints(slides)
    for slide, pts in bullets.items():
        print(f"\n{slide}:")
        for p in pts:
            print(f" - {p}")