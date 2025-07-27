import google.generativeai as genai

genai.configure(api_key="AIzaSyCvpeCpwNe1auSU0jh_w6JssnlWnHrMc0Y")

# Shared Gemini model wrapper
def call_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# 🔹 User Agent
class UserProxyAgent:
    def receive(self, weight, height, age, gender, dietary):
        return {
            "role": "user",
            "data": {
                "weight": weight,
                "height": height,
                "age": age,
                "gender": gender,
                "dietary": dietary
            },
            "reasoning": "User provides health data to begin analysis."
        }

# 🔹 BMI Agent
class BMIAgent:
    def receive(self, message):
        weight = message["data"]["weight"]
        height = message["data"]["height"]
        bmi = round(weight / ((height / 100) ** 2), 2)
        prompt = (
            f"You are a health expert. Given the BMI: {bmi}, "
            "provide the BMI category (Underweight, Normal, Overweight, Obese) and personalized health advice."
        )
        insights = call_gemini(prompt)
        return {
            "role": "bmi_agent",
            "data": {"bmi": bmi, "bmi_insights": insights},
            "reasoning": f"Calculated BMI as {bmi}. Used BMI to request advice from the Gemini model."
        }

# 🔹 Diet Agent
class DietPlannerAgent:
    def receive(self, message, dietary_preference):
        bmi_insights = message["data"]["bmi_insights"]
        prompt = (
            f"You are a certified dietician. Based on the following BMI insights:\n"
            f"{bmi_insights}\n\n"
            f"and the user's dietary preference: {dietary_preference}, "
            "provide a healthy 1-day meal plan."
        )
        meal_plan = call_gemini(prompt)
        return {
            "role": "diet_planner",
            "data": {"meal_plan": meal_plan},
            "reasoning": "Used BMI insights and dietary preference to generate personalized meals."
        }

# 🔹 Workout Agent
class WorkoutSchedulerAgent:
    def receive(self, message, age, gender):
        meal_plan = message["data"]["meal_plan"]
        prompt = (
            f"You are a fitness coach. Based on this meal plan:\n{meal_plan}\n"
            f"User age: {age}, Gender: {gender}. Design a 7-day workout plan with reasoning for each activity."
        )
        workout_plan = call_gemini(prompt)
        return {
            "role": "workout_scheduler",
            "data": {"workout_plan": workout_plan},
            "reasoning": "Used meal plan, age, and gender to suggest a personalized weekly fitness schedule."
        }

# 🔹 Agent Executor (AutoGen-style controller)
class HealthAgentOrchestrator:
    def __init__(self):
        self.user_agent = UserProxyAgent()
        self.bmi_agent = BMIAgent()
        self.diet_agent = DietPlannerAgent()
        self.workout_agent = WorkoutSchedulerAgent()

    def run(self, weight, height, age, gender, dietary):
        # Step 1: User input
        user_msg = self.user_agent.receive(weight, height, age, gender, dietary)
        
        # Step 2: BMI analysis
        bmi_msg = self.bmi_agent.receive(user_msg)
        
        # Step 3: Diet Planning
        diet_msg = self.diet_agent.receive(bmi_msg, dietary)
        
        # Step 4: Workout Planning
        workout_msg = self.workout_agent.receive(diet_msg, age, gender)

        # Final output
        return {
            "user": user_msg,
            "bmi": bmi_msg,
            "diet": diet_msg,
            "workout": workout_msg
        }
