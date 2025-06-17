from crewai import Task
from pydantic import BaseModel
from typing import List, Dict
from tools import currency_tool

# Define a Pydantic model to structure the activity list
class ActivityList(BaseModel):
    activities: List[Dict[str, str]]

def create_tasks(destination: str, budget_usd: int, trip_days: int, researcher, activity_planner, budget_analyst, itinerary_writer):
    research_task = Task(
        description=f"Research cultural attractions (e.g., temples, festivals, museums) and travel trends in {destination} for 2025. Provide insights on seasonal events and visitor tips.",
        expected_output="A report with 5 key cultural attractions and 3 travel trends, each with a brief description.",
        agent=researcher,
        output_file="travel/kyoto_research.txt"
    )

    activity_task = Task(
        description=f"Based on the research, curate a list of 5 cultural activities for a {trip_days}-day trip in {destination}, tailored for cultural immersion. Include activity name, description, and estimated duration.",
        expected_output="A JSON object containing 5 cultural activities with name, description, and duration.",
        agent=activity_planner,
        context=[research_task],
        output_pydantic=ActivityList
    )

    budget_task = Task(
        description=f"Create a budget breakdown for a {trip_days}-day {destination} trip within ${budget_usd}, covering accommodation, activities, food, and transport. Convert costs to JPY where relevant.",
        expected_output="A markdown-formatted budget table with categories, USD costs, and JPY equivalents.",
        agent=budget_analyst,
        context=[activity_task],
        tools=[currency_tool],
        output_file="travel/budget.md"
    )

    itinerary_task = Task(
        description=f"Compile a detailed {trip_days}-day travel itinerary for {destination}, incorporating the curated activities and staying within the budget. Include daily schedules with timings and brief descriptions.",
        expected_output=f"A markdown-formatted {trip_days}-day itinerary with daily schedules, activities, and logistics notes.",
        agent=itinerary_writer,
        context=[activity_task, budget_task],
        output_file="travel/itinerary.md"
    )

    return [research_task, activity_task, budget_task, itinerary_task]