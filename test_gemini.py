import os
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDjEz8HEpPwe0-0KCiOj4EdYgIP2mHC9CU"
genai.configure(api_key=GEMINI_API_KEY)

def list_gemini_models():
    print("Available Gemini Models:")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)

if __name__ == "__main__":
    list_gemini_models()


