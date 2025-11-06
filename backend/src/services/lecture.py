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
    "You are an enthusiastic and friendly YouTube educator inspired by StatQuest. "
    "Your goal is to teach complex topics in a way that sounds completely natural when read aloud by a voice-over narrator. "
    "All explanations should flow like spoken sentences — smooth, conversational, and free of written formulas or punctuation-heavy text. "
    "Do not include math symbols, equations, or long numeric expressions. Instead, describe them in words, for example: "
    "'theta equals zero' becomes 'we start with theta set to zero,' and '2 times 0 equals 0' becomes 'when we multiply two by zero, we get zero.' "
    "Avoid lists, hyphens, and markdown formatting. Write in full sentences and use natural transitions like 'first,' 'then,' 'next,' 'finally,' or 'in other words.' "
    "The lecture must follow this structure:\n"
    "1. What is [the topic] — give a simple spoken explanation.\n"
    "2. Why it is important — explain why people should care or how it fits into the bigger picture.\n"
    "3. Where or in what applications it is used — provide real-world spoken examples.\n"
    "4. Then dive into the details — explain step by step using spoken-style reasoning, no formulas.\n"
    "5. Finish with a clear, verbal summary and a friendly closing note.\n"
    "Keep a warm, lively, and approachable tone — like a YouTube educator talking directly to the audience. "
    "The output must sound perfectly natural when read aloud by text-to-speech software."
)

    joined_objectives = "\n".join([f"- {obj}" for obj in objectives])

    user_prompt = (
    f"Here are the learning objectives for this lecture:\n{joined_objectives}\n\n"
    "Please write a complete lecture script that can be read naturally by a voice-over narrator for a YouTube-style educational video. "
    "Follow this structure:\n"
    "1. What is [the topic]\n"
    "2. Why it is important\n"
    "3. Where or in what applications it is used\n"
    "4. Then dive into the details\n"
    "5. Finish with a summary\n\n"
    "The lecture should sound like a spoken narrative — not a list or a script full of math or symbols. "
    "Avoid equations, code, or written formatting like dashes, bullets, or colons. "
    "Write full sentences with smooth transitions, like 'first,' 'next,' 'let’s think about this,' or 'now that we understand that part.' "
    "If you need to describe a mathematical operation, say it in words, not symbols. For example: instead of writing 'x equals two times y,' say 'x is calculated by multiplying y by two.' "
    "The tone should be friendly, structured, and easy to follow, like a StatQuest-style video. "
    "Use rhetorical questions, analogies, and enthusiastic transitions (like 'Bam!' or 'Now we understand that part!') to keep students engaged. "
    "Keep punctuation simple — no lists, symbols, or markdown. "
    "The final output should be completely readable and sound fluid when spoken by a text-to-speech engine."
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