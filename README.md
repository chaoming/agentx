# AgentX

## Purpose
AgentX is a project focused on developing tools that enhance Large Language Models' (LLM) capabilities through self-improvement. The project aims to empower LLMs with the ability to extend their own functionality by creating and managing tools they need.

## Vision
The vision of AgentX is to develop tools for LLMs to use, enabling them to self-enhance their capabilities. The first step in this direction is providing LLMs with control over the file system and command execution. This foundational capability allows LLMs to create additional tools they need, such as online search functionality, effectively expanding their own capabilities.

## System Overview

The system implements a controlled interaction flow between:
- The LLM (which processes and generates responses)
- A Python script (which handles the communication)
- The user (who provides input and receives responses)

## Response Formats

The system uses two main XML-style formats for communication:

### 1. Response Format
```xml
<RESPOND>content goes here</RESPOND>
```
- Used when the LLM wants to display information to the user
- The Python script extracts and shows the content between the tags
- Can contain any text, including explanations, answers, or results

### 2. Prompt Format
```xml
<PROMPT>prompt content goes here</PROMPT>
```
- Used when the LLM needs to process the next step
- Helps maintain the chain of thought
- Contains internal prompting for the LLM's next action

## Chain of Thought Process

The LLM follows these steps when processing user input:

1. **Initial Analysis**
   - Receives user input
   - Analyzes the request or question
   - Forms initial thoughts about the response

2. **Response Formation**
   - Structures the response based on analysis
   - May include multiple steps or considerations
   - Uses internal prompting for complex responses

3. **Output Generation**
   - Wraps user-facing content in <RESPOND> tags
   - Uses <PROMPT> tags for next steps if needed

## Implementation Notes

For Python implementation:
1. Parse incoming LLM responses for XML tags
2. Display <RESPOND> content to users
3. Process <PROMPT> content for LLM's next step
4. Maintain conversation context as needed

## Benefits

- **Structured Communication**: Clear separation between user-facing responses and internal processing
- **Chain of Thought**: Enables complex reasoning through internal prompting
- **Flexibility**: Can handle simple responses and multi-step interactions
- **Maintainability**: Easy to modify or extend the format for new features
