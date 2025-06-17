import os
import streamlit as st
import json
from agents import create_agents
from tasks import create_tasks
from crew import create_crew, run_crew

# Ensure travel directory exists
if not os.path.exists("travel"):
    os.makedirs("travel")

# Streamlit App
st.title("Travel Planner 2025")
st.write("Plan a cultural trip with AI-powered research and budgeting.")

# User Inputs
st.subheader("Customize Your Trip")
destination = st.text_input("Destination", value="Kyoto, Japan")
budget_usd = st.slider("Budget (USD)", min_value=500, max_value=3000, value=1500)
trip_days = st.slider("Trip Duration (Days)", min_value=3, max_value=7, value=5)

# Create Agents and Tasks
researcher, activity_planner, budget_analyst, itinerary_writer = create_agents(destination, budget_usd, trip_days)
tasks = create_tasks(destination, budget_usd, trip_days, researcher, activity_planner, budget_analyst, itinerary_writer)

# Create Crew
crew = create_crew([researcher, activity_planner, budget_analyst, itinerary_writer], tasks)

# Run CrewAI Workflow
if st.button("Plan My Trip"):
    with st.spinner("Planning your trip... This may take a moment."):
        try:
            result, usage_metrics = run_crew(crew)

            # Display Research Output
            st.subheader("Research Report")
            if os.path.exists("travel/kyoto_research.txt"):
                with open("travel/kyoto_research.txt", "r") as f:
                    st.text_area("Cultural Attractions and Trends", f.read(), height=200)
                with open("travel/kyoto_research.txt", "rb") as f:
                    st.download_button("Download Research", f, file_name="kyoto_research.txt")

            # Display Activity List
            st.subheader("Curated Activities")
            if hasattr(tasks[1].output, "pydantic"):
                activities = tasks[1].output.pydantic.dict()
                st.json(activities)
                st.download_button("Download Activities", json.dumps(activities), file_name="activities.json")

            # Display Budget
            st.subheader("Budget Breakdown")
            if os.path.exists("travel/budget.md"):
                with open("travel/budget.md", "r") as f:
                    st.markdown(f.read())
                with open("travel/budget.md", "rb") as f:
                    st.download_button("Download Budget", f, file_name="budget.md")

            # Display Itinerary
            st.subheader(f"{trip_days}-Day Itinerary")
            if os.path.exists("travel/itinerary.md"):
                with open("travel/itinerary.md", "r") as f:
                    st.markdown(f.read())
                with open("travel/itinerary.md", "rb") as f:
                    st.download_button("Download Itinerary", f, file_name="itinerary.md")

            # Display Usage Metrics
            st.subheader("Usage Metrics")
            st.json(usage_metrics)

        except Exception as e:
            st.error(f"Error during planning: {str(e)}")

# Instructions for running
st.markdown("---")
