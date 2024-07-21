from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator


def generate_signal_name(submenu_name: str, option_name: str) -> str:
    return f"{submenu_name.upper()}_{option_name.upper()}"


def take_break() -> None:
    prompt("Press Enter to continue...")


def _is_number_within_limits(
    lower: int | float = 0, upper: int | float = 99999
) -> Validator:
    def __is_number_within_limits(text: str) -> bool:
        return text.isdigit() and (int(text) >= lower) and (int(text) <= upper)

    validator = Validator.from_callable(
        __is_number_within_limits,
        error_message=f"""Please enter a valid number! 
                                        Min = {lower} and Max={upper}""",
        move_cursor_to_end=True,
    )
    return validator
