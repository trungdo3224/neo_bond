import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Function to call the Gemini API
def call_gemini(prompt, api_key):
  print(api_key)
  try:
    client = genai.Client(api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text
  except Exception as e:
    print(f"An error occurred during Gemini API call: {e}")
    return None

# Load the Gemini API key from the environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Read emotion data from JSON file (replace with your actual file path)
try:
  with open('../facial_emotion_detection/emotion_result.json', 'r') as f:
    emotion_data = json.load(f)
    detected_emotion = emotion_data[-1].get('detected_emotion', 'neutral')  # Get the latest detected emotion
    print(f'Detected emotion: {detected_emotion}')
except FileNotFoundError:
    print("Error: emotion_result.json not found. Please provide the correct file path.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON format in emotion_result.json")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)

# Construct Gemini prompt and generate text
try:
    prompt = f'I am {detected_emotion}'
    generated_text = call_gemini(prompt, api_key)
    print(f"Gemini response: {generated_text}")
except Exception as e:
    print(f"An error occurred during Gemini interaction: {e}")
    exit(1)

# Example of additional processing for optimization (replace with your actual optimization logic)
# ... your code to optimize text generation based on user mood and expressions ...

# Print the final result
print(f"Final Response: {generated_text}")

# Write the response to the output file
output_file_path = 'speech_to_text_output.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(generated_text)
