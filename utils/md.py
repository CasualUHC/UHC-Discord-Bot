"""
Convert the text into markdown safe text.
"""

def escape(text):
    """
    Escape the text.
    """
    return text.replace("_", "\\_")


def bold(text):
    """
    Make the text bold.
    """
    return f"**{text}**"

def italic(text):
    """
    Make the text italic.
    """
    return f"*{text}*"

def block_code(text):
    """
    Make the text code.
    """
    return f"```{text}```"

def inline_code(text):
    """
    Make the text inline code.
    """
    return f"`{text}`"
