from crewai import Crew, Process

def create_crew(agents, tasks):
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        memory=True,
        verbose=True,
        max_rpm=50,
        share_crew=True
    )

def run_crew(crew):
    return crew.kickoff(), crew.usage_metrics