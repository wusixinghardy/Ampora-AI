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


def generate_lecture(objectives: List[str]) -> List[List[Union[str, List[str]]]]:
    """
    Take a list of learning objectives and produce a lecture script divided into slide segments.
    Each element in the returned list is [script_text, visualization_description, bulletpoints_list].
    """

    client = ChatGPTClient()

    system_prompt = (
        "You are an enthusiastic and friendly YouTube educator inspired by StatQuest, "
        "but you also explain topics with the depth and precision of a university professor. "
        "Your goal is to teach complex technical topics in a way that is spoken, natural, "
        "detailed, and deeply thorough. The final narration should be something a voice-over "
        "could read smoothly and clearly.\n\n"

        "Your style requirements:\n"
        "- Spoken, conversational tone, but still rigorous and precise.\n"
        "- Very detailed explanations — as detailed as a full lecture.\n"
        "- When describing math, convert symbols to spoken form, such as 'theta equals zero'.\n"
        "- Avoid symbols entirely (no latex, no formulas, no symbols like ∇, Σ, etc.).\n"
        "- Avoid bullet lists, markdown formatting, or hyphen-style enumerations.\n"
        "- Use transitions like 'first', 'next', 'now let’s walk through', 'to make this concrete', "
        "'in practice', 'what this really means is'.\n"
        "- Each slide must be thorough and cover enough background and explanation for the learner. Don't shorten anything.\n\n"

        "Slide structure requirements:\n"
        "1. Start with: what the topic is, in spoken explanation.\n"
        "2. Then: why the topic is important, where it is used, and why people should care.\n"
        "3. Then: rich technical detail with examples, analogies, and step-by-step reasoning.\n"
        "4. The slides should roughly follow the learning objectives, but in narrative form.\n"
        "5. The narration should be as long and detailed as a real lecture segment.\n"
        "6. Before each slide, include a smooth spoken transition from the previous slide.\n"
        "7. The final slide should end with a warm spoken conclusion.\n\n"

        "Visualization requirement for each slide:\n"
        "Along with the narration, you must produce a clear, specific visualization description that explains exactly "
        "what diagrams, animations, charts, or graphical elements should appear on that slide. "
        "These descriptions must be very detailed so that another teammate can build them without guessing. "
        "Each visualization should match the concepts explained in that slide.\n\n"

        "Bulletpoint requirement for each slide:\n"
        "Also include a list of 3–6 concise, punchy bullet points that summarize the key ideas of that slide. "
        "These should be short, readable phrases suitable for PowerPoint text — no long sentences.\n\n"

        "Output format requirement:\n"
        "You must output valid JSON. Each slide is a JSON object with three fields:\n"
        "  'script': the detailed narration text for that slide\n"
        "  'visualization': a detailed description of what visuals should appear on that slide\n"
        "  'bulletpoints': a list of short bullet point strings summarizing the main takeaways\n\n"

        "Example output (format only, not content):\n"
        "{\n"
        "  'Slide 1': {\n"
        "      'script': 'Very long spoken narration...',\n"
        "      'visualization': 'Detailed visual description...',\n"
        "      'bulletpoints': ['Key concept 1', 'Key concept 2', 'Key concept 3']\n"
        "  },\n"
        "  'Slide 2': {\n"
        "      'script': 'Transition into next topic followed by detailed narration...',\n"
        "      'visualization': 'Another detailed visual description...',\n"
        "      'bulletpoints': ['Idea A', 'Idea B']\n"
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
        "- A 'script' field: the long, detailed narration in spoken tone.\n"
        "- A 'visualization' field: a detailed description of visuals for that slide.\n"
        "- A 'bulletpoints' field: a list of short bullet phrases summarizing the slide.\n\n"
        "The number of slides is up to you, but you must cover all learning objectives thoroughly. "
        "Ensure extremely smooth transitions between slides and that the entire lecture flows like a full-length class.\n\n"
        "Return ONLY a valid JSON object with 'Slide 1', 'Slide 2', etc., where each slide has 'script', 'visualization', and 'bulletpoints'."
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
            bullets = slide_data.get("bulletpoints", [])
            slides_output.append([script, viz, bullets])
    except json.JSONDecodeError:
        # Fallback: basic text-based parsing
        current_script, current_viz, current_bullets = [], [], []
        current_mode = None
        for line in raw_output.splitlines():
            line = line.strip()
            if "Slide" in line and ":" in line:
                if current_script or current_viz or current_bullets:
                    slides_output.append([
                        " ".join(current_script).strip(),
                        " ".join(current_viz).strip(),
                        current_bullets
                    ])
                    current_script, current_viz, current_bullets = [], [], []
            elif line.lower().startswith("script"):
                current_mode = "script"
            elif line.lower().startswith("visualization"):
                current_mode = "visualization"
            elif line.lower().startswith("bulletpoints"):
                current_mode = "bulletpoints"
            elif current_mode == "script":
                current_script.append(line)
            elif current_mode == "visualization":
                current_viz.append(line)
            elif current_mode == "bulletpoints":
                cleaned = line.strip("-•1234567890.) \t")
                if len(cleaned) > 2:
                    current_bullets.append(cleaned)
        if current_script or current_viz or current_bullets:
            slides_output.append([
                " ".join(current_script).strip(),
                " ".join(current_viz).strip(),
                current_bullets
            ])

    return slides_output


def get_scripts(lecture_data: List[List[Union[str, List[str]]]]) -> List[str]:
    """
    Extract the script text from each slide in the lecture data.
    
    Args:
        lecture_data: Output from generate_lecture(), where each element is [script, visualization, bulletpoints].
    
    Returns:
        A list of strings, each representing the narration script for a slide.
    """
    return [slide[0] for slide in lecture_data if len(slide) > 0]


def get_visual_descriptions(lecture_data: List[List[Union[str, List[str]]]]) -> List[str]:
    """
    Extract the visualization description from each slide in the lecture data.
    
    Args:
        lecture_data: Output from generate_lecture(), where each element is [script, visualization, bulletpoints].
    
    Returns:
        A list of strings, each representing the visualization description for a slide.
    """
    return [slide[1] for slide in lecture_data if len(slide) > 1]


def get_bulletpoints(lecture_data: List[List[Union[str, List[str]]]]) -> List[List[str]]:
    """
    Extract the bulletpoints from each slide in the lecture data.
    
    Args:
        lecture_data: Output from generate_lecture(), where each element is [script, visualization, bulletpoints].
    
    Returns:
        A list of lists of strings, each inner list representing the bulletpoints for a slide.
    """
    return [slide[2] if len(slide) > 2 and isinstance(slide[2], list) else [] for slide in lecture_data]



if __name__ == "__main__":
    topic = "Stochastic Gradient Descent"

    print("\n🎯 LEARNING OBJECTIVES:")
    objectives = generate_learning_objectives(topic)
    print(objectives)

    print("\n---\n🎬 GENERATING FULL LECTURE (SCRIPT + VISUALS + BULLETPOINTS)...")
    lecture = generate_lecture(objectives)

    # Extract each component using the helper functions
    scripts = get_scripts(lecture)
    visuals = get_visual_descriptions(lecture)
    bullets = get_bulletpoints(lecture)

    # Print results nicely
    for i, (script, viz, bp) in enumerate(zip(scripts, visuals, bullets), start=1):
        print(f"\n🟩 Slide {i} Script:\n{script}")
        print(f"🖼️ Slide {i} Visualization:\n{viz}")
        print("📊 Bulletpoints:")
        for p in bp:
            print(f" - {p}")