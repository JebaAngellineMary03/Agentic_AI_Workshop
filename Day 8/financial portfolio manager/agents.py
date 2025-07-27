from gemini_api import gemini_generate
import datetime

def user_proxy_agent(user_data, chat):
    chat.append(('User Proxy Agent', 'Initiating investment management workflow.'))
    return group_chat_manager(user_data, chat)

def group_chat_manager(user_data, chat):
    chat.append(('Group Chat Manager', 'Calling Portfolio Analysis Agent for user input.'))
    return portfolio_analysis_agent(user_data, chat)

def portfolio_analysis_agent(user_data, chat):
    chat.append(('Portfolio Analysis Agent', 'Analyzing user portfolio...'))
    prompt = f"""
You are a Portfolio Analysis Agent. The user has the following details:
- Current Salary: {user_data['salary']}
- Portfolio: {user_data['portfolio']}
Summarize the portfolio and recommend whether the user should pursue Growth or Value investments. Reply with 'Growth' or 'Value' and a brief summary.
"""
    result = gemini_generate(prompt)
    chat.append(('Portfolio Analysis Agent', result))
    if 'growth' in result.lower():
        return stateflow('Growth', user_data, chat)
    else:
        return stateflow('Value', user_data, chat)

def stateflow(category, user_data, chat):
    chat.append(('StateFlow', f"Routing to {category} Investment Agent."))
    if category == 'Growth':
        return growth_investment_agent(user_data, chat)
    else:
        return value_investment_agent(user_data, chat)

def growth_investment_agent(user_data, chat):
    chat.append(('Growth Investment Agent', 'Generating high-growth investment recommendations...'))
    prompt = f"""
You are a Growth Investment Agent. The user has the following details:
- Current Salary: {user_data['salary']}
- Portfolio: {user_data['portfolio']}
Suggest high-growth investment options suitable for this user.
"""
    result = gemini_generate(prompt)
    chat.append(('Growth Investment Agent', result))
    return investment_advisor_agent(user_data, result, chat)

def value_investment_agent(user_data, chat):
    chat.append(('Value Investment Agent', 'Generating stable, long-term investment recommendations...'))
    prompt = f"""
You are a Value Investment Agent. The user has the following details:
- Current Salary: {user_data['salary']}
- Portfolio: {user_data['portfolio']}
Suggest stable, long-term investment options suitable for this user.
"""
    result = gemini_generate(prompt)
    chat.append(('Value Investment Agent', result))
    return investment_advisor_agent(user_data, result, chat)

def investment_advisor_agent(user_data, recommendations, chat):
    chat.append(('Investment Advisor Agent', 'Compiling personalized financial report...'))
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    prompt = f"""
You are an Investment Advisor Agent. The user has the following details:
- Current Salary: {user_data['salary']}
- Portfolio: {user_data['portfolio']}
- Recommendations: {recommendations}
- Date: {current_date}
Generate a detailed, personalized financial report for the user, including portfolio analysis and investment suggestions. The report should include the current date.
"""
    report = gemini_generate(prompt)
    chat.append(('Investment Advisor Agent', report))
    return report 