import os
class ReportGeneratorAgent:
    def create_report(self, overview, findings, image_paths) -> str:
        report = f'''
        <h2>EDA Report</h2>
        <h3>Overview</h3>
        <div>{overview}</div>
        <h3>Key Findings</h3>
        <div>{findings}</div>
        <h3>Visualizations</h3>
        {''.join([f'<div><img src="{img}" width="600"/><br><em>{os.path.basename(img)}</em></div>' for img in image_paths])}
        <hr>
        <div style="font-size:small;color:gray;">This report provides a comprehensive overview of the dataset. See critic feedback below for improvements.</div>
        '''
        return report 