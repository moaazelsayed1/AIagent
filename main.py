import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your prompt>' [--verbose]")
        sys.exit(1)

    # Load API key from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. 
    You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. 
    You do not need to specify the working directory in your function calls 
    as it is automatically injected for security reasons.
    """

    # Register available functions
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    # Prepare user input
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    # Get response from model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config,
    )

    # Check for function calls or plain text
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                print(f"Calling function: {part.function_call.name}({part.function_call.args})")
            elif part.text:
                print(part.text)
    else:
        print("No response from model.")

    # Optional verbose info
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print("User prompt:", sys.argv[1])
        if response.usage_metadata:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
