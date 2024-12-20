import ollama
from prompts import get_prompt
from colorama import Fore, Style, init
init(autoreset=True)

def extract_tag_content(text, tag):
    """Extract content between XML tags."""
    start_tag = f"<{tag}>"
    end_tag = f"</{tag}>"
    start_index = text.find(start_tag)
    if start_index == -1:
        return None
    start_index += len(start_tag)
    end_index = text.find(end_tag, start_index)
    if end_index == -1:
        return None
    return text[start_index:end_index].strip()

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
                modified_prompt = get_prompt(current_prompt, version="chain_of_thought").format(previous_steps=previous_steps)
            
            # Debug output
            print(Fore.WHITE + f"Prompt: {modified_prompt}" + Style.RESET_ALL)
            
            # Get LLM response
            messages.append({'role': 'user', 'content': modified_prompt})
            response = ollama.chat(model='llama3.2:latest', messages=messages)
            messages.append(response['message'])
            step = response['message']['content']
            
            # Debug output
            print(Fore.BLUE + f"{step}" + Style.RESET_ALL)
            
            # Track conversation steps - extract content from tags
            step_content = step
            if "<PROMPT>" in step:
                step_content = extract_tag_content(step, "PROMPT")
            elif "<RESPOND>" in step:
                step_content = extract_tag_content(step, "RESPOND")
            elif "<SEARCH_ONLINE>" in step:
                step_content = f"Searching for: {extract_tag_content(step, 'SEARCH_ONLINE')}"
            
            # Add step to history if it contains a tag
            if "<PROMPT>" in step or "<RESPOND>" in step or "<SEARCH_ONLINE>" in step:
                step_number = len(steps) + 1
                steps.append(f"Step {step_number}: {step_content}")
                previous_steps = "\n".join(steps)

            # Process response for tags
            response_content = extract_tag_content(step, "RESPOND")
            prompt_content = extract_tag_content(step, "PROMPT")
            search_content = extract_tag_content(step, "SEARCH_ONLINE")

            # Handle search content
            if search_content:
                print(Fore.MAGENTA + f"Searching online for: {search_content}" + Style.RESET_ALL)
                # In a real implementation, you would perform the actual online search here
                # For now, we'll simulate a search result
                search_result = f"Search results for '{search_content}': [This is where actual search results would appear]"
                current_prompt = search_result
                continue

            # Handle response content
            if response_content:
                print("\n" + Fore.YELLOW + response_content + Style.RESET_ALL)
                if not prompt_content and not search_content:
                    break

            # Handle prompt content
            if prompt_content:
                current_prompt = prompt_content
                continue
            
            # If no tags found, use entire response as next prompt
            current_prompt = step


if __name__ == "__main__":
    main()
