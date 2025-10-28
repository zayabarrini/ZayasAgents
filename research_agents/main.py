# main.py
import time
from datetime import datetime

from agents.data_analyst import DataAnalyst
from agents.report_writer import ReportWriter
from agents.research_director import ResearchDirector
from agents.web_researcher import WebResearcher
from config.settings import config
from tools.file_manager import FileManager


class ResearchOrchestrator:
    """Main orchestrator that coordinates all research agents"""

    def __init__(self, topic: str):
        self.topic = topic
        self.director = ResearchDirector(topic)
        self.researcher = WebResearcher()
        self.analyst = DataAnalyst()
        self.writer = ReportWriter()
        self.file_manager = FileManager()

        self.research_data = {}
        self.analysis_results = {}
        self.final_report = ""

    def conduct_research(self) -> Dict[str, Any]:
        """Execute the complete research workflow"""
        print(f"🚀 Starting comprehensive research on: {self.topic}")
        print("=" * 60)

        # Step 1: Planning
        print("📋 Phase 1: Research Planning")
        research_plan = self.director.create_research_plan()
        print(f"   • Created plan with {len(research_plan.get('search_queries', []))} search queries")

        # Step 2: Research
        print("\n🔍 Phase 2: Web Research")
        queries = self.researcher.generate_search_queries(
            self.topic,
            research_plan.get('research_questions', [])
        )

        self.research_data = self.researcher.conduct_research(queries)
        print(f"   • Gathered {self.research_data['total_results']} information sources")

        # Step 3: Analysis
        print("\n📊 Phase 3: Data Analysis")
        pattern_analysis = self.analyst.identify_patterns(self.research_data['flattened_results'])
        quality_assessment = self.analyst.validate_information(self.research_data['flattened_results'])

        synthesis = self.director.analyze_findings(self.research_data['flattened_results'])

        self.analysis_results = {
            "pattern_analysis": pattern_analysis,
            "quality_assessment": quality_assessment,
            "synthesis": synthesis
        }
        print("   • Completed pattern analysis and quality assessment")

        # Step 4: Report Generation
        print("\n📝 Phase 4: Report Generation")
        self.final_report = self.writer.generate_report(
            self.topic, research_plan, self.research_data, self.analysis_results
        )

        executive_summary = self.writer.create_executive_summary(self.final_report)

        print("   • Generated comprehensive report and executive summary")

        # Step 5: Save Results
        print("\n💾 Phase 5: Saving Results")
        report_path = self.file_manager.save_report(self.final_report, self.topic)
        data_path = self.file_manager.save_research_data({
            "topic": self.topic,
            "research_plan": research_plan,
            "research_data": self.research_data,
            "analysis": self.analysis_results,
            "executive_summary": executive_summary
        }, self.topic)

        print(f"   • Report saved: {report_path}")
        print(f"   • Data saved: {data_path}")

        return {
            "report_path": report_path,
            "data_path": data_path,
            "executive_summary": executive_summary,
            "research_metrics": {
                "sources_analyzed": self.research_data['total_results'],
                "queries_executed": len(queries),
                "analysis_completed": True
            }
        }

def main():
    """Main function to run the research system"""

    # Example research topics
    topics = [
        "Artificial Intelligence in Healthcare",
        "Renewable Energy Trends 2024",
        "Quantum Computing Applications",
        "Sustainable Urban Development"
    ]

    print("🤖 Agentic AI Research System")
    print("=" * 50)

    # Get user input
    user_topic = input("Enter research topic (or press Enter for default): ").strip()

    if not user_topic:
        user_topic = "Artificial Intelligence in Healthcare"
        print(f"Using default topic: {user_topic}")

    print(f"\nStarting research on: {user_topic}")

    # Initialize and run research
    orchestrator = ResearchOrchestrator(user_topic)

    try:
        start_time = time.time()
        results = orchestrator.conduct_research()
        end_time = time.time()

        print("\n" + "=" * 60)
        print("✅ Research Completed Successfully!")
        print(f"⏱️  Total time: {end_time - start_time:.2f} seconds")
        print(f"📄 Report location: {results['report_path']}")

        # Print executive summary
        print("\n" + "=" * 60)
        print("📋 EXECUTIVE SUMMARY")
        print("=" * 60)
        print(results['executive_summary'])

    except Exception as e:
        print(f"❌ Research failed with error: {e}")
        # You might want to add retry logic or partial result saving here

if __name__ == "__main__":
    main()
