from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileWriterTool

@CrewBase
class NeoBond_AI():
    """AI Companion Ecosystem Builders Crew"""

    @agent
    def nlp_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['nlp_agent'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    @agent
    def speech_to_text_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['speech_to_text_agent'],
            verbose=True,
            tools=[SerperDevTool()]
        )
    @agent
    def computer_vision_engineer(self) -> Agent:
        cs_agent = Agent(
            config=self.agents_config['computer_vision_engineer'],
            verbose=True,
            tools=[SerperDevTool()]
        )
        return cs_agent
    @task
    def nlp_task(self) -> Task:
        return Task(
            config=self.tasks_config['nlp_task'],
        )
    
    @task
    def speech_to_text_task(self) -> Task:
        return Task(
            config=self.tasks_config['speech_to_text_task'],
        )
    # @task
    # def computer_vision_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['computer_vision_task'],
    #     )
    @task
    def facial_emotion_task(self) -> Task:
        return Task(
            config=self.tasks_config['facial_emotion_task'],
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
    crew = NeoBond_AI()
    crew.crew().start()
