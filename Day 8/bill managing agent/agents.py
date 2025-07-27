from gemini_api import gemini_generate

# User Proxy Agent: Initiates the workflow

def user_proxy_agent(image_path, chat):
    chat.append(("User Proxy Agent", f"Received bill image: {image_path}. Forwarding to Group Manager."))
    return group_manager_agent(image_path, chat)

# Group Manager Agent: Orchestrates the workflow

def group_manager_agent(image_path, chat):
    chat.append(("Group Manager Agent", "Passing bill image to Bill Processing Agent for extraction and categorization."))
    return bill_processing_agent(image_path, chat)

# Bill Processing Agent: Extracts and categorizes expenses from image

def bill_processing_agent(image_path, chat):
    chat.append(("Bill Processing Agent", "Extracting and categorizing expenses from bill image..."))
    prompt = f"""
You are a Bill Processing Agent. The user has uploaded a bill image at path: {image_path}.
Extract the list of expenses from the image and categorize them into common groups (e.g., groceries, dining, utilities, shopping, entertainment). Return a JSON list of items with category, item, and amount. If you cannot see the image, simulate a plausible output for testing.
"""
    result = gemini_generate(prompt)
    chat.append(("Bill Processing Agent", result))
    return expense_summarization_agent(result, chat)

# Expense Summarization Agent: Summarizes and analyzes expenses

def expense_summarization_agent(expense_json, chat):
    chat.append(("Expense Summarization Agent", "Analyzing categorized expenses and summarizing spending trends..."))
    prompt = f"""
You are an Expense Summarization Agent. Here is a categorized list of expenses in JSON format:
{expense_json}
Summarize the total spending per category, highlight the highest expenditure category, and note any unusual or high spending trends.
"""
    summary = gemini_generate(prompt)
    chat.append(("Expense Summarization Agent", summary))
    return summary 