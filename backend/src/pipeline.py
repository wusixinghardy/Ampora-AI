import os
import sys
from image_to_script import process_all_images
from script_to_ppt import create_presentation_from_scripts

def run_pipeline(images_folder="images", 
                 scripts_json="scripts/image_scripts.json",
                 output_ppt="output/generated_presentation.pptx",
                 presentation_title="Ampora Generated Presentation"):
    """
    Run the complete pipeline:
    1. Analyze images and generate scripts
    2. Create PowerPoint presentation
    """
    
    print("="*60)
    print("AMPORA AUTOMATED PRESENTATION PIPELINE")
    print("="*60)
    
    # Check if images folder exists
    if not os.path.exists(images_folder):
        print(f"\n✗ Error: '{images_folder}' folder not found!")
        print(f"Please create the folder and add some images.")
        sys.exit(1)
    
    # Check if there are images
    image_files = [f for f in os.listdir(images_folder) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if len(image_files) == 0:
        print(f"\n✗ Error: No images found in '{images_folder}' folder!")
        print(f"Please add some .jpg, .png, or other image files.")
        sys.exit(1)
    
    print(f"\n✓ Found {len(image_files)} images to process\n")
    
    # Step 1: Generate scripts
    print("\n" + "="*60)
    print("STEP 1: ANALYZING IMAGES & GENERATING SCRIPTS")
    print("="*60 + "\n")
    
    try:
        scripts_data = process_all_images(images_folder, scripts_json)
    except Exception as e:
        print(f"\n✗ Error in script generation: {e}")
        sys.exit(1)
    
    # Step 2: Create PowerPoint
    print("\n" + "="*60)
    print("STEP 2: CREATING POWERPOINT PRESENTATION")
    print("="*60 + "\n")
    
    try:
        output_file = create_presentation_from_scripts(scripts_json, output_ppt, presentation_title)
    except Exception as e:
        print(f"\n✗ Error creating PowerPoint: {e}")
        sys.exit(1)
    
    # Success!
    print("\n" + "="*60)
    print("✓ PIPELINE COMPLETE!")
    print("="*60)
    print(f"\nYour presentation is ready: {output_file}")
    print(f"Scripts saved to: {scripts_json}")
    print("\n")

if __name__ == "__main__":
    run_pipeline()