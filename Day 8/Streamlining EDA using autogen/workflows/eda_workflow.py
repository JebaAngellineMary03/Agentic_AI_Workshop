import os
import pandas as pd
from agents.data_preparation import DataPreparationAgent
from agents.eda_agent import EDAAgent
from agents.report_generator import ReportGeneratorAgent
from agents.critic_agent import CriticAgent
from agents.executor_agent import ExecutorAgent
from agents.admin_agent import AdminAgent

def run_workflow(data_path):
    file_ext = os.path.splitext(data_path)[-1].lower()
    if file_ext == ".csv":
        df = pd.read_csv(data_path)
    elif file_ext in [".xls", ".xlsx"]:
        df = pd.read_excel(data_path)
    else:
        raise ValueError("Unsupported file type")

    dp_agent = DataPreparationAgent()
    eda_agent = EDAAgent()
    report_agent = ReportGeneratorAgent()
    critic_agent = CriticAgent()
    executor = ExecutorAgent()
    admin = AdminAgent()

    df_clean = dp_agent.clean_data(df)
    summary = eda_agent.summarize(df_clean)
    image_paths = eda_agent.generate_visuals(df_clean)
    report = report_agent.create_report("Cleaned data overview.", summary, image_paths)
    with open("outputs/final_report.html", "w", encoding="utf-8") as f:
        f.write(report)
    feedback = critic_agent.review(report)
    validation = executor.validate_report("outputs/final_report.html")
    admin.coordinate([
        lambda: print("Feedback:\n", feedback),
        lambda: print("Validation:\n", validation)
    ])
    return report, feedback, validation, image_paths 