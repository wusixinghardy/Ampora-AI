
import os
import sys
# Try to import supabase
try:
    import supabase
    print(f"Supabase version: {supabase.__version__}")
except Exception as e:
    print(f"Could not import supabase: {e}")

try:
    from supabase import create_client, Client
    print("Supabase client imported.")
except ImportError:
    print("Could not import Client/create_client.")

# Mock env vars if needed, but we just want to see if init crashes
os.environ["SUPABASE_URL"] = "https://example.supabase.co"
os.environ["SUPABASE_KEY"] = "some-key"

try:
    print("Attempting initialization...")
    client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    print("Initialization SUCCESS!")
except Exception as e:
    print(f"Initialization FAILED: {e}")
    import traceback
    traceback.print_exc()

# Print pip freeze to see actual versions
import subprocess
print("\n--- Pip Freeze ---")
subprocess.run([sys.executable, "-m", "pip", "freeze"])
