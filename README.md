# Tipsy - a light library for interactive CLI application

This is Tipsy, a small small library for developing and deploying (locally!!)
small, interactive CLI applications. 

It's intended for things that should be done quickly, with prime focuse on 
functionality and not on the infrastructure.

It's intended for simple applications, that depend on user to make a selection
and trigger an action.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Future Developments](#future-developments)
- [Contributing](#contributing)
- [License](#license)

## Installation

Preferably use a virtualenv to run tipsy and the whole application. For the 
moment pipenv could be used to deploy, install and run your application. 

Install pipenv using pip:

```bash
pip install pipenv
```

If restricted or there are problems with pip, you can use:

```bash
python -m pip install pipenv

```

Navigate in the directory you wish to install tipsy and develop the app and
clone the repo

```bash
cd my_app
git init.
git clone https://github.com/Gygarte/tipsy.git

```

Create the environment and install de dependencies specified in the Pipfile using:

```bash
pipenv --python 3.12
pipenv install --dev

```

or:

```bash
python -m pipenv --python 3.12
python -m pipenv install --dev

```

Start using tipsy in your project. 

Note: Refer to the *pipenv* documentation here: https://pypi.org/project/pipenv/
## Usage

Tipsy uses four mandatory items to setup the CLI application:
1. **Application** main class to be used
2. **LayoutFactory** main class for app layout construction
3. **State** main class for configuring an internal state - which contains whatever informations
is needed in the app
4. **layout.json** the blueprint of the layout.

### Creating a layout.json

An example equal to 1000 words :D

```json
{
    "submenu": [
        {
            "title": "Main_Menu",
            "main":true,
            "logo_path": null,
            "header_msg": "This is the header for the main menu",
            "footer_msg": "Gabriel Artemie@2023",
            "return_to_previous": false,
            "return_to_main": false,
            "quit": true,
            "options": [
                {
                    "option": "SwitchToSubmenu2",
                    "include_help": true,
                    "help": "SwitchToSubmenu2 help",
                    "switch":"Second_Menu",
                    "action": null
                },
                {
                    "option": "Print_and_wait",
                    "include_help": true,
                    "help": "Print_and_wait help",
                    "switch":null,
                    "action": null
                },
                {
                    "option": "Trigger_an_error",
                    "include_help": true,
                    "help": "Trigger_an_error help",
                    "switch":null,
                    "action": null
                }
            ],
            "style":null // NOT IMPLEMENTED: to use a special style for each submenu
        },
        {
            "title": "Second_Menu",
            "main":false,
            "logo_path": null,
            "header_msg": "This is another header message for submenu2",
            "footer_msg": "Gabriel Artemie@2023",
            "return_to_previous": true,
            "return_to_main": true,
            "quit": true,
            "options": [
                {
                    "option": "Accept_an_input",
                    "include_help": true,
                    "help": "option1 help",
                    "switch":null,
                    "action": null
                },
                {
                    "option": "Print_the_state",
                    "include_help": true,
                    "help": "option2 help",
                    "switch":null,
                    "action": null
                }
            ],
            "style":null // NOT IMPLEMENTED: to use a special style for each submenu
        }
    ],
    "error_handling":{
        "name":"Error",
        "include":true,
        "log_path":null
    },
    "style_sheet_path":null, //NOT IMPLEMENTED: a path to a separate style sheet
    "default_style":{
        "dimensions":{
            "type":"auto",
            "width":null,
            "height":null
        },
        "padding":{
            "top":1,
            "right":2,
            "bottom":1,
            "left":2
        },
        "border":{
            "type":"*"
        }
    }
}

```

The layout is created by passing the path to the layout.json to the LayoutFactory constructor

```python
from tipsy import LayoutFactory

layout = LayoutFactory('my_app/layout.json') 

```

### The style

The style sheet is still a simple approach for a kinda' retro style type.
The inspiration for the style apperance was draw from the **console-menu** by @aergirhall
(many many thanks to you for idea. I hope to see your project functional again!)

From the above **layout.json** you can guess what styling options are available in this version. 

Please see the [Future Developments](#future-developments) section bellow for details regarding the development of this feature.

### Setting a State

A **State** keeps data that are used by the end functions. You can add specific configuration in the 
**State** from the app initialization and from the end functions. 

The **State** is configured to be saved whenewer the app is quitting or an error is triggered. So, any 
configurations passed to the **State** should implement a saving mechanism. 

Let's assume:
```python

from dataclass import datacalss

@dataclass
class MyConfig:

    # a bunch of attributes and configurations

    def save(self) -> None:
        # some saving logic

```

So the **State** will be defined as:

```python

state = State({"config":MyConfig()})

```

### Setting the application

This is as simple as passing the **State** and **Layout** to the **Application** constructor and hit run.

```python

app = Application(layout=layout, state=state)

app.run()
```

### Setting end functions

In order to do some stuff with all this we need some end function. The end functions should use the 
**State** and return a signal like *OK*, *Error*, *Abort*

Let's see an example:

```python
from tipsy import State
from tipsy.signals import OK, Error, Abort

def my_func(state:State) -> OK | Error | Abort:

    # do some stuff and return something

```

In order to save the results of the computation in the **State** you just pass a dictionary
with the *name_of_the_data* and the *actual_data_object* to the **OK.payload()**. 

If an error occured you can pass the following arguments to the **Error**: *origin*, *log_message*, *traceback*

```python

from tipsy import State
from tipsy.signals import OK, Error, Abort

def my_func(state:State) -> OK | Error | Abort:

    # all is good and the computation runned smoothly
    resulted_state = {"name_of_the_data":actual_data_object}

    return OK(pyload=resulted_state)

    # an error occured
    return Error()

    # you are fancy and use try-except and traceback.format_exc
    try:
        # some shady stuff
    except Exception:
        return Error(origin="here",log_message="Some shady error occured!", traceback=format_exc())

```

Finally your function is passed to the app instance as follows

```python

def main() -> None:

    app = Application(layout=layout, state=state)
    app.add(function=my_func, option="Option1", submenu="Submenu1") # tadaaaa

    app.run()

if __name__ == "__main__":
    main()
```

**That is all!** You can start building simple and beautifull stuff and show your work bestie the cool stuff you do because you do not have a real life :D. Cheers! 

## Examples

In order to run an example, just run the **__example__.py** from the root folder. I was lazy to solve some import issues.

## Future Developments

TO BE CONTINUED

## Contributing

No public contributions are currently accepted!

## License

No, not yet!
