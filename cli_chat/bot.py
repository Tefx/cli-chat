import os

import openai
from openai import OpenAIError, ChatCompletion

from .console import Console


class Bot:
    def __init__(self, openai_api_key,
                 console=None,
                 command_manager=None,
                 model="gpt-3.5-turbo"):
        self.model = model
        self.console = console or Console()
        self.answer_history = []
        self.render_markdown = True
        self.command_manager = command_manager
        self.command_manager.setup(self)

        openai.api_key = openai_api_key

    def extract_command(self, input_str):
        input_str = input_str.strip()
        if input_str.startswith("\\"):
            control_cmd, _, input_str = input_str[1:].partition(" ")
            commands = self.command_manager.parse_command(control_cmd)
            return list(commands), input_str.strip()
        return [], input_str

    def ask(self, user_content, previous_answer):
        message = [
            dict(role="system", content="render answer in markdown"),
            dict(role="user", content=user_content),
        ]
        if previous_answer:
            message.append(dict(role="assistant", content=previous_answer))
        try:
            completion = ChatCompletion.create(
                model=self.model,
                messages=message,
            )
            answer = completion.choices[0]["message"]["content"]
            self.answer_history.append(answer)
            return answer
        except OpenAIError as e:
            self.console.error(str(e))

    def one_round(self):
        self.render_markdown = True
        question = self.console.user_prompt(long=False)
        if question.strip() == "":
            self.console.warning("Please input something")
            return True
        if question.lower() in ["thanks", "thank you", "thx", "tq"]:
            return False
        commands, question = self.extract_command(question)
        self.command_manager.check_commands(commands)
        question = self.command_manager.preprocess(commands, question)
        if not question:
            return True
        answer = self.ask(question, self.answer_history[-1] if self.answer_history else None)
        answer = self.command_manager.postprocess(commands, answer)
        if answer:
            self.console.bot_prompt()
            self.console.print(answer, render=self.render_markdown)
        return True

    def __call__(self):
        while True:
            continue_flag = self.one_round()
            self.console.gap()
            if not continue_flag:
                break

    def toggle_render_markdown(self, state: bool):
        self.render_markdown = state

    def clear_answer_history(self, last_num=None):
        if last_num is None:
            self.answer_history = []
        elif last_num > len(self.answer_history):
            self.answer_history = []
        else:
            self.answer_history = self.answer_history[:-last_num]

    def print_history(self):
        for i in range(len(self.answer_history)):
            idx = len(self.answer_history) - i - 1
            answer = self.answer_history[idx].partition(os.linesep)[0]
            self.console.print_history_item(-i, answer)
