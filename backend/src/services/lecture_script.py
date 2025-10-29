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

    # Check input type
    if isinstance(input_data, str) and os.path.isfile(input_data):
        # PDF or slide
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
        # Concept only
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

    # Parse objectives list into clean list of strings
    objectives = []
    for line in raw_output.splitlines():
        if line.strip():
            line = line.strip("-•1234567890.) \t")
            if len(line) > 3:
                objectives.append(line)
    return objectives


def generate_lecture_script(objectives: List[str]) -> str:
    """
    Take a list of learning objectives and produce a natural, teacher-like lecture script.
    """
    client = ChatGPTClient()
    system_prompt = (
        "You are a skilled university lecturer who delivers clear, engaging, and pedagogically sound lectures. "
        "You naturally connect topics with smooth transitions and emphasize intuition and step-by-step logic. "
        "Avoid sounding like bullet points; sound like a professor giving a live class."
    )

    joined_objectives = "\n".join([f"- {obj}" for obj in objectives])

    user_prompt = (
        f"Here are the learning objectives for this lecture:\n{joined_objectives}\n\n"
        "Please write a full lecture script that a human teacher could read aloud. "
        "The lecture script should be for video lecture, such as YouTube educational video or an online course. "
        "Include:\n"
        "- Clear topic transitions\n"
        "- Occasional rhetorical questions to keep students engaged\n"
        "- Intuitive explanations and analogies\n"
        "- Smooth conclusion tying all objectives together\n\n"
        "Output should be in multiple paragraphs (not bullet points)."
    )

    lecture_text = client.chat(system_prompt, user_prompt)
    return lecture_text


# Example manual run
if __name__ == "__main__":
    topic = "Stochastic Gradient Descent"
    objectives = generate_learning_objectives(topic)
    print("Learning Objectives:\n", objectives)
    print("\n---\nGenerating lecture script...\n")
    script = generate_lecture_script(objectives)
    print(script)