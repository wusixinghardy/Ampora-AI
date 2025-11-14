import os
import json
import base64
from openai import OpenAI
from dotenv import load_dotenv

def encode_image(image_path):
    """Convert image to base64 for OpenAI API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_and_generate_script(image_path, client):
    """
    Use OpenAI Vision API to analyze image and generate StatQuest-style script
    """
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o",  # GPT-4 with vision
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """You are Josh Starmer from StatQuest, creating a narration script for an educational video.

Analyze this image and write a script that explains what's happening in a clear, step-by-step, conversational way.

Guidelines:
- Start with a friendly hook
- Break down the concept progressively: "Let's start with...", "Now let's look at...", "And finally..."
- Use analogies or simple explanations when helpful
- Be enthusiastic but clear
- If the image shows a process or decision tree, explain it step-by-step
- End with a recap: "So, to summarize..."

The script should be 150-300 words, written as if you're speaking directly to the camera.

Write the complete narration script now:"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content

def process_all_images(images_folder="images", output_json="scripts/image_scripts.json"):
    """
    Process all images in folder and generate scripts
    """
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Get all image files
    image_files = [f for f in os.listdir(images_folder) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    scripts_data = {}
    
    print(f"Found {len(image_files)} images to process...\n")
    
    for idx, image_file in enumerate(image_files, 1):
        image_path = os.path.join(images_folder, image_file)
        print(f"[{idx}/{len(image_files)}] Analyzing {image_file}...")
        
        try:
            script = analyze_image_and_generate_script(image_path, client)
            scripts_data[image_file] = {
                "path": image_path,
                "script": script
            }
            print(f"✓ Generated script ({len(script)} chars)\n")
        except Exception as e:
            print(f"✗ Error processing {image_file}: {e}\n")
            scripts_data[image_file] = {
                "path": image_path,
                "script": "Error generating script",
                "error": str(e)
            }
    
    # Save to JSON
    os.makedirs("scripts", exist_ok=True)
    with open(output_json, 'w') as f:
        json.dump(scripts_data, f, indent=2)
    
    print(f"✓ All scripts saved to {output_json}")
    return scripts_data

if __name__ == "__main__":
    scripts = process_all_images()