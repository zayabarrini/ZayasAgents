# tools/file_manager.py
import json
import os
from datetime import datetime

import markdown

from config.settings import config


class FileManager:
    """Tool for managing file operations and report generation"""

    def __init__(self):
        self.output_dir = config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def save_research_data(self, data: Dict, topic: str) -> str:
        """Save raw research data to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_{topic.replace(' ', '_')}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filepath

    def save_report(self, content: str, topic: str, format: str = "markdown") -> str:
        """Save research report in specified format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic.replace(' ', '_')

        if format == "html":
            filename = f"report_{safe_topic}_{timestamp}.html"
            # Convert markdown to HTML
            html_content = markdown.markdown(content)
            full_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Research Report: {topic}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                    h1, h2, h3 {{ color: #333; }}
                    .metadata {{ color: #666; font-size: 0.9em; }}
                </style>
            </head>
            <body>
                <h1>Research Report: {topic}</h1>
                <div class="metadata">Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
                {html_content}
            </body>
            </html>
            """
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

        else:  # markdown
            filename = f"report_{safe_topic}_{timestamp}.md"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Research Report: {topic}\n\n")
                f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                f.write(content)

        return filepath
