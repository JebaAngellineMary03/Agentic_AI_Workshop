import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re
import os
from dotenv import load_dotenv

# ------------ LOAD API KEYS FROM .env ------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Ensure keys are present
if not GEMINI_API_KEY or not TAVILY_API_KEY:
    raise ValueError("API keys are not set in the environment variables.")


genai.configure(api_key=GEMINI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ------------ AGENT CLASS ------------
class WebResearchAgent:
    def __init__(self, topic):
        self.topic = topic
        self.questions = []
        self.key_points = {}

    def generate_questions(self):
        prompt = f"""
        Generate 6 well-structured research questions about the topic "{self.topic}".
        Cover background, challenges, opportunities, technology, policy, and future trends.
        """
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")

        for line in lines:
            if line.strip():
                question = line.strip("-•1234567890. ").strip()
                self.questions.append(question)

    def search_web_and_extract_key_points(self, question):
        safe_query = question.strip()[:400]
        response = tavily_client.search(query=safe_query, max_results=5)
        combined_content = ""
        for result in response.get("results", []):
            content = result.get("content", "")
            if content:
                combined_content += content + "\n"

        # If no content found, skip summarization
        if not combined_content.strip():
            self.key_points[question] = "⚠️ Could not retrieve sufficient data from the web to summarize this question."
            return

        # Summarize using Gemini
        summary_prompt = f"""
        Extract 5 concise bullet points from the text below that answer the following question:

        "{question}"

        Text:
        {combined_content}
        """
        model = genai.GenerativeModel("gemini-2.0-flash")
        summary_response = model.generate_content(summary_prompt)

        # Additional fallback if Gemini returns a bad response
        if "Please provide the text" in summary_response.text:
            self.key_points[question] = "⚠️ Gemini could not generate bullet points due to limited input content."
        else:
            self.key_points[question] = summary_response.text.strip()

    def compile_report(self):
        report = f"# Research Report on: {self.topic}\n\n"
        report += f"## Introduction\nThis report investigates various aspects of **{self.topic}** using AI-assisted reasoning and web research.\n\n"

        for i, question in enumerate(self.questions, 1):
            report += f"## {i}. {question}\n"
            report += f"{self.key_points.get(question, 'No key points found.')}\n\n"

        report += "## Conclusion\nThe findings above summarize key insights about the topic using automated research techniques.\n"
        return report

    def create_pdf(self, report_md):
        """Create PDF using ReportLab"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            doc = SimpleDocTemplate(tmp_pdf.name, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                alignment=1  # Center alignment
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=12,
                spaceBefore=12,
                spaceAfter=6
            )
            
            story = []
            
            # Split markdown into sections
            sections = report_md.split('\n')
            
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                    
                if section.startswith('# '):
                    # Main title
                    title_text = section[2:]
                    story.append(Paragraph(title_text, title_style))
                    story.append(Spacer(1, 12))
                    
                elif section.startswith('## '):
                    # Section heading
                    heading_text = section[3:]
                    story.append(Paragraph(heading_text, heading_style))
                    story.append(Spacer(1, 6))
                    
                else:
                    # Regular text - clean up markdown formatting properly
                    text = self.clean_markdown_for_pdf(section)
                    if text:  # Only add non-empty paragraphs
                        story.append(Paragraph(text, styles['Normal']))
                        story.append(Spacer(1, 6))
            
            doc.build(story)
            return tmp_pdf.name
    
    def clean_markdown_for_pdf(self, text):
        """Clean markdown formatting for PDF generation"""
        # Remove or escape problematic characters
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        
        # Handle bold text properly - find **text** patterns
        import re
        
        # Replace **text** with <b>text</b>
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
        
        # Replace *text* with <i>text</i>
        text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
        
        # Clean up bullet points
        text = re.sub(r'^[-•]\s*', '• ', text)
        
        # Remove empty lines and extra spaces
        text = text.strip()
        
        return text

# ------------ STREAMLIT UI ------------
st.set_page_config(page_title="Web Research Agent", layout="wide")

st.title("🧠 Web Research Agent using Gemini + Tavily")
st.markdown("This tool generates structured research reports using AI and real-time web search.")

topic = st.text_input("Enter a research topic:", "")

if st.button("Run Research Agent") and topic:
    with st.spinner("Running the agent... this may take a minute."):
        agent = WebResearchAgent(topic)
        agent.generate_questions()

        for question in agent.questions:
            agent.search_web_and_extract_key_points(question)

        report_md = agent.compile_report()

    st.success("✅ Research complete!")
    st.markdown(report_md)

    # Markdown download
    st.download_button(
        label="📥 Download Report as Markdown",
        data=report_md,
        file_name="research_report.md",
        mime="text/markdown"
    )

    # PDF download using ReportLab
    try:
        pdf_file_path = agent.create_pdf(report_md)
        with open(pdf_file_path, "rb") as f:
            st.download_button(
                label="📥 Download Report as PDF",
                data=f,
                file_name="research_report.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"PDF generation failed: {str(e)}")
        st.info("You can still download the Markdown version above.")