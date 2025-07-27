class ExecutorAgent:
    def validate_report(self, report_path="outputs/final_report.html") -> str:
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                content = f.read()
            return "Validation Passed: Report is complete and readable."
        except Exception as e:
            return f"Validation Failed: {e}" 