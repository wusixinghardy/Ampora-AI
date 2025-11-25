import os
import json
from typing import List, Union
from src.LLM.Gemini import GeminiClient


# ============================================================
# BUILD THE GEMINI PROMPT FOR ONE SLIDE
# ============================================================

def build_gemini_slide_prompt(slide: dict) -> str:
    """
    Build the full prompt for generating a single slide image using Gemini.
    """

    title = slide.get("title", "").strip()
    bulletpoints = slide.get("bulletpoints", [])
    visual_step = slide.get("visual_step_description", "").strip()

    bullet_text = "\n".join([f"- {bp}" for bp in bulletpoints])

    # ----------------------
    # THE FULL PROFESSIONAL PROMPT
    # ----------------------
    return f"""
        You are a professional presentation designer who creates clean, modern,
        university-level lecture slides in the style of MIT, Stanford, and DeepMind,
        combined with the step-by-step educational storytelling style of StatQuest.

        Your job is to generate ONE slide image (PNG).

        ===============================
        GENERAL DESIGN REQUIREMENTS
        ===============================
        - Clean academic aesthetic (MIT / Stanford / DeepMind style)
        - Simple, minimal layout — no cartoonish elements
        - White background with dark text and subtle highlight colors
        - One clean sans-serif font (Inter / Helvetica / Calibri)
        - Consistent alignment, spacing, and heading hierarchy
        - Diagrams must be sharp, vector-like, and professional
        - No unnecessary decoration, shading, or 3D effects

        ==========================================
        STYLE REQUIREMENTS (STATQUEST TEACHING)
        ==========================================
        - Build visuals incrementally
        - This is *one step* of a multi-step conceptual progression
        - Do NOT merge or remove steps
        - Bulletpoints may repeat across steps, but visuals must evolve

        ======================================
        VISUALIZATION REQUIREMENTS
        ======================================
        - Every slide must include:
            1. Slide Title (short, descriptive, academic)
            2. Bulletpoints (3–6 concise items)
            3. Diagram/Visualization (strictly based on the description)
            4. Optional small “speaker notes” section

        - Diagrams must be clear and professional:
            • labeled arrows  
            • vector lines  
            • clean plots  
            • boxes, matrices, nodes, arrows, step-by-step overlays  
            • Absolutely NO cartoon characters, emojis, clip art, or playful graphics

        ======================================
        SLIDE CONTENT TO RENDER
        ======================================
        Slide Title:
        {title}

        Bulletpoints:
        {bullet_text}

        Diagram/Visualization:
        {visual_step}

        ======================================
        OUTPUT REQUIREMENT
        ======================================
        - GENERATE EXACTLY ONE IMAGE
        - Professional academic slides
        - StatQuest-style incremental visuals
        - NO commentary, NO explanation
        - The output must be a clean slide image following all rules above
    """.strip()


# ============================================================
# GENERATE ALL SLIDE IMAGES USING GEMINI
# ============================================================

def generate_visualizations_with_gemini(
    slide_steps: List[dict],
    output_dir: Union[str, os.PathLike] = "generated_visuals",
    # Using Gemini 3 Pro Image (Nano Banana) by default as it handles complex prompts well
    model: str = "gemini-3-pro-image-preview" 
) -> List[str]:
    """
    Given a list of slide objects each containing:
        title
        bulletpoints
        visual_step_description

    This function generates one slide image per object using Gemini API.
    """

    os.makedirs(output_dir, exist_ok=True)

    # Initialize Client with the specific image generation model
    client = GeminiClient(model=model)
    output_paths = []

    print(f"Starting generation of {len(slide_steps)} slides using model: {model}")

    for idx, slide in enumerate(slide_steps, start=1):
        prompt = build_gemini_slide_prompt(slide)
        
        # Filename: slide_01.png, slide_02.png...
        output_path = os.path.abspath(os.path.join(output_dir, f"slide_{idx:02d}.png"))

        print(f"Generating slide {idx}/{len(slide_steps)}: '{slide.get('title', 'Untitled')}'...")

        # ============================
        # CALL GEMINI IMAGE GENERATION
        # ============================
        try:
            # This calls the new method we added to Gemini.py
            image_bytes = client.generate_image(prompt)
            
            # Save to file
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            
            print(f" -> Saved to {output_path}")
            output_paths.append(output_path)

        except Exception as e:
            print(f" [ERROR] Failed to generate slide {idx}: {e}")
            # Optional: continue to next slide instead of crashing entire batch
            continue

    return output_paths


# ============================================================
# DEMO MAIN
# ============================================================

if __name__ == "__main__":

    sample_slides = [
        {
            "title": "Later Passes: Gradually Sorting (4.1)",
            "bulletpoints": [
                "Each pass sorts one more item",
                "Unsorted region shrinks"
            ],
            "visual_step_description": "[3, 4, 2, 5, 8]. Gray out 5 and 8. Highlight (3, 4)."
        },
        {
            "title": "Time Complexity Overview (6.1)",
            "bulletpoints": [
                "Worst: O(n²)",
                "Average: O(n²)",
                "Best: O(n) when nearly sorted"
            ],
            "visual_step_description": "Simple plot showing comparisons growing quadratically with n."
        }
    ]

    paths = generate_visualizations_with_gemini(sample_slides)
    print("\nAll generated slide images:", paths)