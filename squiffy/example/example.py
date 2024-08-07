"""
A simple example of how to use the library.

It uses the example1.json file to create the layout.
"""

import os
from squiffy import State, Application, LayoutFactory
from squiffy.signals import OK, Error


def print_and_wait(state: State) -> OK:
    print("This is a simple example of how to use the library.")
    input("Press enter to continue...")

    return OK()


def trigger_an_error(state: State) -> Error:
    print("This is an  example of how an error looks like at time moment.")
    input("Press enter to raise error...")

    return Error(log_message="This is a test error")


def accept_an_input(state: State) -> OK:
    user_input = input("Insert a number from 1 to 10!")

    return OK("accept_an_input", payload={"input": user_input})


def print_the_state(state: State) -> OK:
    print(f"The state is {state.get('input')}")
    input("Press enter to continue...")

    return OK()


def main() -> None:
    path_to_layout = os.path.join(os.path.dirname(__file__), "ex_layout.json")

    layout = LayoutFactory(layout_file_path=path_to_layout)
    state = State()

    app = Application(layout=layout, state=state)

    app.add(
        function=print_and_wait, option_name="Print_and_wait", submenu_name="Main_Menu"
    )
    app.add(
        function=trigger_an_error,
        option_name="Trigger_an_error",
        submenu_name="Main_Menu",
    )
    app.add(
        function=accept_an_input,
        option_name="Accept_an_input",
        submenu_name="Second_Menu",
    )
    app.add(
        function=print_the_state,
        option_name="Print_the_state",
        submenu_name="Second_Menu",
    )

    app.run()


if __name__ == "__main__":
    main()
