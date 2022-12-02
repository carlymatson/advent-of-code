import re


def capture(name: str, pattern: str) -> str:
    return f"(?P<{name}>{pattern})"


def regex_snippets():
    # Example of using capture groups
    s = "And then we have Carly: +32 \n and Nick: -35"
    name_re = capture("name", "\w+")
    age_re = capture("age", "[+-]?\d+")
    pattern = f"{name_re}: {age_re}"

    matches = [m.groupdict() for m in re.finditer(pattern, s)]
    print(matches)


regex_snippets()
