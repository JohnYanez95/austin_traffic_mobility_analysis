import re


def to_snake_case(text):
    # Step 1: Remove any parentheses and special characters while keeping underscores
    text = re.sub(r"[^\w\s]", "", text)

    # Step 2: Replace spaces with underscores
    text = re.sub(r"\s+", "_", text)

    # Step 3: Convert PascalCase or camelCase to snake_case
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", text)

    # Step 4: Ensure all text is lowercase
    text = text.lower()

    # Step 5: Remove any consecutive underscores
    text = re.sub(r"_{2,}", "_", text)

    return text
