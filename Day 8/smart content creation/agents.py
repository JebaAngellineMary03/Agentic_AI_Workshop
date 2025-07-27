import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCvpeCpwNe1auSU0jh_w6JssnlWnHrMc0Y"
genai.configure(api_key="AIzaSyCvpeCpwNe1auSU0jh_w6JssnlWnHrMc0Y")

class ContentCreatorAgent:
    system_message = (
        "You are the Content Creator Agent. Your role is to draft content on topics involving Generative AI. "
        "Ensure the content is clear, concise, and technically accurate."
    )
    def run(self, topic, previous_content=None, feedback=None):
        model = genai.GenerativeModel("gemini-1.5-flash")
        if previous_content is None:
            prompt = f"{self.system_message}\n\nTopic: {topic}\n\nDraft the initial content."
        else:
            prompt = (
                f"{self.system_message}\n\nHere is the previous content:\n\n{previous_content}\n\n"
                f"Here is the feedback from the Critic Agent:\n\n{feedback}\n\nRevise the content to address the feedback."
            )
        return model.generate_content(prompt).text

class ContentCriticAgent:
    system_message = (
        "You are the Content Critic Agent. Your role is to evaluate the content drafted by the Content Creator Agent. "
        "Provide feedback on language and technical correctness, and suggest improvements."
    )
    def run(self, content):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"{self.system_message}\n\nHere is the content to evaluate:\n\n{content}\n\nProvide feedback and suggestions."
        )
        return model.generate_content(prompt).text 