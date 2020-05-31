import re
from framework.codeBuilder import CodeBuilder


class Template:
    html_regex = re.compile(r'(?s)({{.*?}}|{%.*?%}|{#.*?#})')
    valid_name_regex = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*$')
    def __init__(self, html: str, context: dict = None) -> None:
        self.context = context or {}
        self.code = CodeBuilder()
        self.all_vars = set()
        self.loop_vars = set()
        self.code.start_func()
        vars_code = self.code.add_section()
        buffered = []

        def flush_output() -> None:

            if len(buffered) == 1:
                self.code.add_line(f'append_result({buffered[0]})')
            elif len(buffered) > 1:
                self.code.add_line(f'extend_result([{", ".join(buffered)}])')
            del buffered[:]

        strings = re.split(self.html_regex, html)

        for string in strings:
            if string.startswith('{%'):
                flush_output()
                words = string[2:-2].strip().split()
                ops = words[0]
                if ops == 'if':
                    if len(words) != 2:
                        self._syntax_error("Don't understand if", string)
                    self.code.add_line(f'if {words[1]}:')
                    self.code.indent()
                elif ops == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("Don't understand for", string)
                    i = words[1]
                    iter_obj = words[3]
                    # 这里被迭代的对象可以是一个变量,也可以是列表,元组或者range之类的东西,因此使用_variable来检验
                    try:
                        self._variable(iter_obj, self.all_vars,1)
                    # except TemplateSyntaxError:
                    except Exception:
                        pass
                    self._variable(i, self.loop_vars,1)
                    self.code.add_line(f'for {i} in {iter_obj}:')
                    self.code.indent()
                elif ops == 'end':
                    if len(words) != 1:
                        self._syntax_error("Don't understand end", string)
                    self.code.dedent()
                else:
                    self._syntax_error("Don't understand tag", ops)
            elif string.startswith('{{'):
                expr = string[2:-2].strip()
                self._variable(expr, self.all_vars,0)
                buffered.append(f'to_str({expr})')
            else:
                if string.strip():
                    # 这里使用repr把换行符什么的改成/n的形式,不然插到code字符串中会打乱排版
                    buffered.append(repr(string))
        flush_output()
        for var_name in self.all_vars - self.loop_vars:
            vars_code.add_line(f'{var_name} = context["{var_name}"]')
        self.code.end_func()

    def _variable(self, name: str, vars_set: set,isFor:int) -> None:
        if isFor ==0:
            if name.find('.') >= 0:
                return
            if name.find('\'')>=0:
                return
        # 当解析html过程中出现变量,就调用这个函数
        # 一方面检验变量名是否合法,一方面记下变量名
        if not re.match(self.valid_name_regex, name):
            self._syntax_error('Not a valid name', name)
        vars_set.add(name)

    def _syntax_error(self, message: str, thing: str) -> None:
        return
        # raise TemplateSyntaxError(f'{message}: {thing}')  # 这个Error类直接继承Exception就行

    def render(self, context=None) -> str:
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        print(render_context)
        return self.code.get_globals()['render'](render_context)