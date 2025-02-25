from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class NeoBond():
    """AI Companion Ecosystem Builders Crew"""

    # agents_config = 'src/neo_bond/config/agents.yaml'
    # tasks_config = 'src/neo_bond/config/tasks.yaml'
    

    # @agent
    # def ai_architect(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['ai_architect'],
    #         verbose=True,
    #         tools=[SerperDevTool()]
    #     )

    @agent
    def computer_vision_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['computer_vision_engineer'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def nlp_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['nlp_agent'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    # @agent
    # def matching_social_ai_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['matching_social_ai_agent'],
    #         verbose=True,
    #         tools=[SerperDevTool()]
    #     )

    @agent
    def frontend_ui_ux_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_ui_ux_agent'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    # @agent
    # def ai_ethics_safety_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['ai_ethics_safety_agent'],
    #         verbose=True,
    #         tools=[SerperDevTool()]
    #     )

    # Task definitions
    @task
    def computer_vision_task(self) -> Task:
        return Task(
            config=self.tasks_config['computer_vision_task'],
        )

    @task
    def nlp_task(self) -> Task:
        return Task(
            config=self.tasks_config['nlp_task'],
        )

    @task
    def backend_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_task'],
        )

    # @task
    # def matching_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['matching_task'],
    #     )

    @task 
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    # @task
    # def ethics_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['ethics_task'],
    #     )

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
    crew = NeoBond()
    crew.crew().start()
