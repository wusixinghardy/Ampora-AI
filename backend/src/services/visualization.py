import os
import json
import concurrent.futures
from typing import List, Union, Tuple
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
# HELPER: PROCESS A SINGLE SLIDE (THREADED)
# ============================================================

def _generate_single_slide(
    idx: int, 
    slide: dict, 
    output_dir: str, 
    client: GeminiClient
) -> Union[str, None]:
    """
    Helper function to generate a single slide. 
    Used by ThreadPoolExecutor.
    """
    prompt = build_gemini_slide_prompt(slide)
    output_path = os.path.abspath(os.path.join(output_dir, f"slide_{idx:02d}.png"))
    
    print(f"   [Started] Slide {idx}: '{slide.get('title', 'Untitled')}'")
    
    try:
        image_bytes = client.generate_image(prompt)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"   [Done] Slide {idx} saved.")
        return output_path
    except Exception as e:
        print(f"   [ERROR] Slide {idx} failed: {e}")
        return None


# ============================================================
# GENERATE ALL SLIDE IMAGES (PARALLEL)
# ============================================================

def generate_visualizations_with_gemini(
    slide_steps: List[dict],
    output_dir: Union[str, os.PathLike] = "generated_visuals",
    model: str = "gemini-3-pro-image-preview",
    max_workers: int = 5  # Adjust based on rate limits (5 is usually safe)
) -> List[str]:
    """
    Generates slide images in parallel using ThreadPoolExecutor.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Initialize Client once (assuming thread-safe or lightweight)
    client = GeminiClient(model=model)
    
    output_paths = [None] * len(slide_steps)  # Pre-allocate list to maintain order
    
    print(f"Starting PARALLEL generation of {len(slide_steps)} slides (Workers: {max_workers})...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Dictionary to map futures back to their index
        future_to_index = {
            executor.submit(_generate_single_slide, idx, slide, output_dir, client): idx
            for idx, slide in enumerate(slide_steps, start=1)
        }

        for future in concurrent.futures.as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                result_path = future.result()
                if result_path:
                    # Store result in correct index (idx-1 because slides start at 1)
                    output_paths[idx-1] = result_path
            except Exception as exc:
                print(f"   [CRITICAL] Thread exception for slide {idx}: {exc}")

    # Filter out any failed (None) paths
    valid_paths = [p for p in output_paths if p is not None]
    
    print(f"Generation complete. {len(valid_paths)}/{len(slide_steps)} slides successful.")
    return valid_paths


# ============================================================
# DEMO MAIN
# ============================================================

if __name__ == "__main__":
    sample_slides = [
        {
            "title": "Slide 1: Intro",
            "bulletpoints": ["Point A", "Point B"],
            "visual_step_description": "A simple start diagram."
        },
        {
            "title": "Slide 2: Middle",
            "bulletpoints": ["Point C", "Point D"],
            "visual_step_description": "A complex middle diagram."
        },
        {
            "title": "Slide 3: End",
            "bulletpoints": ["Point E", "Point F"],
            "visual_step_description": "A final summary diagram."
        }
    ]

    paths = generate_visualizations_with_gemini(sample_slides)
    print("\nGenerated paths:", paths)