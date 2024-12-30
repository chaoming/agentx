import ollama
import json
from prompts import get_prompt
from colorama import Fore, Style, init
init(autoreset=True)

def extract_json_content(text):
    """Extract content from JSON string."""
    try:
        data = json.loads(text)
        return data
    except json.JSONDecodeError:
        return None

def main():
    messages = []
    while True:
        # Get user input
        user_prompt = input("\n" + Fore.GREEN + "Enter your prompt (type 'exit' to quit): " + Style.RESET_ALL)
        if user_prompt.lower() == 'exit':
            break

        # Initialize conversation state
        steps = []
        current_prompt = user_prompt
        previous_steps = ""
        first_step = True

        # Process conversation steps
        while True:
            # Get appropriate prompt based on step
            if first_step:
                modified_prompt = get_prompt(current_prompt, version="chain_of_thought_step_1")
                first_step = False
            else:
                modified_prompt = get_prompt(current_prompt, version="chain_of_thought", previous_steps=previous_steps)
            
            # Get LLM response
            messages.append({'role': 'user', 'content': modified_prompt})
            response = ollama.chat(model='llama3.2:latest', messages=messages)
            messages.append(response['message'])
            step = response['message']['content']
            
            # Debug output
            print(Fore.BLUE + f"{step}" + Style.RESET_ALL)
            
            # Track conversation steps - extract content from JSON
            step_content = step
            json_content = extract_json_content(step)
            if json_content:
                if json_content.get("type") == "prompt":
                    step_content = json_content.get("content")
                elif json_content.get("type") == "respond":
                    step_content = json_content.get("content")
                elif json_content.get("type") == "search":
                    step_content = f"Searching for: {json_content.get('query')}"
                
                step_number = len(steps) + 1
                steps.append(f"Step {step_number}: {step_content}")
                previous_steps = "\n".join(steps)

            # Process response for JSON
            if json_content:
                if json_content.get("type") == "respond":
                    print("\n" + Fore.YELLOW + json_content.get("content") + Style.RESET_ALL)
                    if not json_content.get("type") == "prompt" and not json_content.get("type") == "search":
                        break
                elif json_content.get("type") == "search":
                    search_content = json_content.get("query")
                    print(Fore.MAGENTA + f"Searching online for: {search_content}" + Style.RESET_ALL)
                    # In a real implementation, you would perform the actual online search here
                    # For now, we'll simulate a search result
                    search_result = f"Search results for '{search_content}': [This is where actual search results would appear]"
                    current_prompt = search_result
                    continue
                elif json_content.get("type") == "prompt":
                    current_prompt = json_content.get("content")
                    continue
            
            # If no JSON found, use entire response as next prompt
            current_prompt = step


if __name__ == "__main__":
    main()
