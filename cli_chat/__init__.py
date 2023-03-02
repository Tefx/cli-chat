from pathlib import Path

import openai
from openai.error import OpenAIError
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style


def parse_control_cmd(input_str):
    input_str = input_str.strip()
    if input_str.startswith("\\"):
        control_cmd, _, input_str = input_str[1:].partition(" ")
        return control_cmd.split(","), input_str
    return [], input_str


def main():
    key_path = Path(".key")
    if not key_path.exists():
        key = prompt(
            "Cannot find key, maybe this is the first time you use, please key in a valid OpenAI Key:"
        )
        with key_path.open("w") as f:
            f.write(key)

    with open(".key") as f:
        openai.api_key = f.read().strip()

    style = Style.from_dict({"prompt": "#7fff00 bold", "": "#ADD8E6"})
    history = FileHistory(".history")
    auto_suggest = AutoSuggestFromHistory()
    console = Console()

    completion = None
    while True:
        question = prompt(
            "You: ",
            history=history,
            auto_suggest=auto_suggest,
            style=style,
        )

        if question.strip() == "":
            console.print("Please input something")
            continue

        control_cmds, question = parse_control_cmd(question)

        if "no-render" in control_cmds:
            markdown = False
        else:
            markdown = True

        if "long" in control_cmds:
            question += prompt("> ",
                               multiline=True,
                               history=history,
                               auto_suggest=auto_suggest,
                               style=style,
                               prompt_continuation="> ")

        if "load-file" in control_cmds:
            file_path = prompt("File path: ",
                               history=history,
                               auto_suggest=auto_suggest,
                               style=style)
            with open(file_path) as f:
                question += f.read()

        if "save" in control_cmds:
            if not completion:
                console.print("No output to save")
                continue
            file_path = prompt("File path: ",
                               history=history,
                               auto_suggest=auto_suggest,
                               style=style)
            with open(file_path, "w") as f:
                f.write(completion["choices"][0]["message"]["content"])
            console.print(f"Last response saved to {file_path}")
            if question.strip() == "":
                continue

        if question.lower() in ["thanks", "thank you", "thx", "tq"]:
            break

        messages = [
            {"role": "system", "content": f"render your answer in markdown"},
            {"role": "user", "content": question},
        ]
        if completion:
            messages.append(completion["choices"][0]["message"])

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        except OpenAIError as e:
            console.print(f"\n[red][bold]Error:[/bold][/red]")
            console.print(str(e))

        if "hide-answer" in control_cmds:
            continue

        answer = completion["choices"][0]["message"]["content"]
        if markdown:
            answer = Markdown(answer)

        console.print(f"\n[green][bold]Bot:[/bold][/green]")
        console.print(answer)
        console.print()
