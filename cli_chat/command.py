class CommandManagerBase:
    def __init__(self):
        self.bot = None
        self.console = None

    def setup(self, bot):
        self.bot = bot
        self.console = bot.console

    @staticmethod
    def parse_command(seq_str):
        for part in seq_str.split("|"):
            if "{" in part:
                part, _, _tags = part.partition("{")
                tags = set(_tags[:-1].split(","))
            else:
                tags = set()
            if "(" in part:
                part, _, _args = part.partition("(")
                args = _args[:-1].split(",")
            else:
                args = []
            yield part.replace("-", "_"), args, tags

    def check_commands(self, commands):
        for cmd, _, _ in commands:
            if getattr(self, f"pre_handler__{cmd}", None):
                continue
            elif getattr(self, f"post_handler__{cmd}", None):
                continue
            else:
                self.console.warning(f"Unknown command: {cmd}, ignored.")

    def preprocess(self, commands, question):
        for cmd, args, tags in commands:
            handler = getattr(self, f"pre_handler__{cmd}", None)
            if handler:
                question = handler(question, *args, **{k: True for k in tags})
                if question is None:
                    break
        return question

    def postprocess(self, commands, answer):
        for cmd, args, tags in commands:
            handler = getattr(self, f"post_handler__{cmd}", None)
            if handler:
                answer = handler(answer, *args, **{k: True for k in tags})
                if answer is None:
                    break
        return answer


class CommandManager(CommandManagerBase):
    def pre_handler__long(self, question):
        return question + "\n" + self.console.user_prompt(long=True)

    def pre_handler__load_file(self, question):
        file_path = self.console.file_prompt()
        with open(file_path) as f:
            question += f.read()
        return question

    def pre_handler__save(self, question, append=False):
        if self.bot.answer_history:
            file_path = self.console.file_prompt()
            with open(file_path, "a" if append else "w") as f:
                f.write(self.bot.answer_history[-1])
            self.console.info(f"Last answer Saved to {file_path}")
        else:
            self.console.error("[red]No output to save[/red]")
        return question

    def pre_handler__continue(self, question, num):
        num = int(num)
        self.bot.clear_answer_history(-num)
        return question

    def pre_handler__forget(self, question):
        self.bot.clear_answer_history()
        return question

    def pre_handler__history(self, question):
        self.bot.print_history()
        return question

    def post_handler__no_render(self, answer):
        self.bot.toggle_render_markdown(False)
        return answer

    @staticmethod
    def post_handler__hide_answer(_):
        return "**Answer Hidden**"
