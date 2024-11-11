def copy_to_clipboard(value: str | int | None) -> None:
    if value is None:
        return
    try:
        import pyperclip

        pyperclip.copy(str(value))
        print("Copied to clipboard!")
    except ImportError:
        print("Not copied to clipboard - pyperclip could not be imported")
        pass
