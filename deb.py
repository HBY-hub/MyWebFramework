def render(context: dict) -> str:
    result = []
    append_result = result.append
    extend_result = result.extend
    to_str = str
    title = context["title"]
    extend_result(['\n    <p>', to_str(title), '</p>\n    <ul>\n        '])
    for i in range(10):
        if i%2==1:
            extend_result(['\n                <li>', to_str(i), '</li>\n            '])
    append_result('\n    </ul>\n')
    return ''.join(result)


print(render({"title":"11"}))
