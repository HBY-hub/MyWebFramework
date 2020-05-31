class CodeBuilder:
    INDENT_STEP = 4

    def __init__(self, indent_level: int = 0) -> None:
        self.indent_level = indent_level
        self.code = []
        self.global_namespace = None

    def start_func(self) -> None:
        self.add_line('def render(context: dict) -> str:')
        self.indent()
        self.add_line('result = []')
        # self.add_line('print("ccccccccccccc")')
        # self.add_line('print(context)')
        # self.add_line('print("ccccccccccccccc")')
        self.add_line('append_result = result.append')
        self.add_line('extend_result = result.extend')
        self.add_line('to_str = str')

    def end_func(self) -> None:
        self.add_line("return ''.join(result)")
        self.dedent()

    def add_section(self) -> 'CodeBuilder':
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        print("section")
        print(self.code)
        print("section")
        return section

    def __str__(self) -> str:
        return ''.join(str(line) for line in self.code)

    def add_line(self, line: str) -> None:
        self.code.extend([' ' * self.indent_level + line + '\n'])

    def indent(self) -> None:
        self.indent_level += self.INDENT_STEP
        # self.add_line("print(type(i))")

    def dedent(self) -> None:
        self.indent_level -= self.INDENT_STEP

    def get_globals(self) -> dict:
        if self.global_namespace is None:
            self.global_namespace = {}
            python_source = str(self)
            print(python_source)
            print("-----------------")
            # print(self.global_namespace)
            print("--------------------------")
            print(self.global_namespace)
            exec(python_source, self.global_namespace)
        return self.global_namespace