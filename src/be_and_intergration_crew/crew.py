from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class NeoBond_BE():
    """AI Companion Ecosystem Builders Crew"""
    @agent
    def api_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['api_agent'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    
    @agent
    def database_agent  (self) -> Agent:
        return Agent(
            config=self.agents_config['database_agent'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    
    @agent
    def intergration_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['intergration_agent'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    # Task definitions
    @task
    def api_task(self) -> Task:
        return Task(
            config=self.tasks_config['api_task'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    @task
    def database_task(self) -> Task:
        return Task(
            config=self.tasks_config['database_task'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    @task
    def intergration_task(self) -> Task:
        return Task(
            config=self.tasks_config['intergration_task'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    @crew
    def crew(self) -> Crew:
        """Creates the AI Ecosystem crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

if __name__ == "__main__":
    crew = NeoBond_BE()
    crew.crew().start()
