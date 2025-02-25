#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from neo_bond.crew import NeoBond
from be_and_intergration_crew.crew import NeoBond_BE
from ai_crew.crew import NeoBond_AI

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    print("Enter BE for backend and integration crew\n")
    print("Enter AI for AI crew\n")
    crew = input("Enter the crew you want to run: ")
    if crew == "BE":
        crew = NeoBond_BE().crew().kickoff()
    elif crew == "AI":
        crew = NeoBond_AI().crew().kickoff()
    