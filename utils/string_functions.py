import re


def to_snake_case(text: str) -> str:
    # Step 1: Convert PascalCase (UpperCase) and camelCase to snake_case
    text = re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()

    # Step 2: Ensure existing snake_case remains unchanged
    # Remove any double underscores that might occur
    text = re.sub(r"_{2,}", "_", text)

    return text
