# squiffy - a light library for interactive CLI application

This is squiffy, a small, small - wonderfully small -  library for developing and deploying locally 
interactive CLI applications. 

It's intended for things that should be done quickly, with prime focuse on 
functionality and not on the infrastructure.

We aim to provide a bit of infrastructure for simple applications, that depend on user interaction
which triggers custom actions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Future Developments](#future-developments)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can use *pip* to install squiffy into your environment.

```bash

pip install squiffy

```

Additionally we encourage usage of virtualenv to for development environments. 
we recommend to use pipenv for your development environment. 

Install pipenv using pip:

```bash
pip install pipenv
```

If restricted or there are problems with pip, you can use:

```bash
python -m pip install pipenv

```

Navigate in the directory you wish to install squiffy into and develop the app and
use *pipenv install* to install squiffy.

```bash
cd my_app
pipenv install squiffy

```
If you want to modify squiffy to suit your need, just clone the repo:

```bash
cd my_app
git init.
git clone https://github.com/Gygarte/squiffy.git

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

Start using squiffy in your project. 


Note: Refer to the *pipenv* documentation here: https://pypi.org/project/pipenv/
## Usage

Squiffy uses four mandatory items to setup the CLI application:
1. **layout.json** the blueprint of your application's layout.
2. **LayoutFactory** the main class for app layout construction
3. **State** the main class for configuring an internal state - which contains whatever informations is needed in the app
4. **Application** the main class to be used

### Creating a layout.json

An example equals to 1000 words :D (please be advise that I purposfully let some keywords that 
do nothing yet! Squiffy is still in alpha and I'm still a noob)

```json
{
    "submenu": [
        {
            "title": "Main_Menu",
            "main":true,
            "logo_path": null,  // NOT IMPLEMENTED
            "header_msg": "This is the header for the main menu",
            "footer_msg": "Gabriel Artemie@2023",
            "return_to_previous": false,
            "return_to_main": false,
            "quit": true,
            "options": [
                {
                    "option": "SwitchToSubmenu2",
                    "include_help": true,  // NOT IMPLEMENTED
                    "help": "SwitchToSubmenu2 help",  // NOT IMPLEMENTED
                    "switch":"Second_Menu",
                    "action": null  // NOT IMPLEMENTED
                },
                {
                    "option": "Print_and_wait",
                    "include_help": true,  // NOT IMPLEMENTED
                    "help": "Print_and_wait help",  // NOT IMPLEMENTED
                    "switch":null,
                    "action": null  // NOT IMPLEMENTED
                },
                {
                    "option": "Trigger_an_error",
                    "include_help": true,  // NOT IMPLEMENTED
                    "help": "Trigger_an_error help",  // NOT IMPLEMENTED
                    "switch":null,
                    "action": null  // NOT IMPLEMENTED
                }
            ],
            "style":null // NOT IMPLEMENTED: to use a special style for each submenu
        },
        {
            "title": "Second_Menu",
            "main":false,
            "logo_path": null,  // NOT IMPLEMENTED
            "header_msg": "This is another header message for submenu2",
            "footer_msg": "Gabriel Artemie@2023",
            "return_to_previous": true,
            "return_to_main": true,
            "quit": true,
            "options": [
                {
                    "option": "Accept_an_input",
                    "include_help": true,  // NOT IMPLEMENTED
                    "help": "option1 help",  // NOT IMPLEMENTED
                    "switch":null,
                    "action": null  // NOT IMPLEMENTED
                },
                {
                    "option": "Print_the_state",
                    "include_help": true,  // NOT IMPLEMENTED
                    "help": "option2 help",  // NOT IMPLEMENTED
                    "switch":null,
                    "action": null  // NOT IMPLEMENTED
                }
            ],
            "style":null // NOT IMPLEMENTED: to use a special style for each submenu
        }
    ],
    "error_handling":{
        "name":"Error",
        "include":true,
        "log_path":null  // NOT IMPLEMENTED
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
            "type":"light" // You can chouse from "light", "thick" and "double" border style
        }
    }
}

```
### The *LayoutFactory*

The layout is created by passing the path to the layout.json to the LayoutFactory constructor

```python
from squiffy import LayoutFactory

layout = LayoutFactory('my_app/layout.json') 

```

### The style

The style sheet is still a simple approach for a kinda' retro style type.
The inspiration for the style apperance was drawn from the **console-menu** project by @aergirhall
(many many thanks to you for the ideas and I hope you do not dissaprove that I've used them)

From the above **layout.json** you can guess what styling options are available in this version. 

Please see the [Future Developments](#future-developments) section bellow for details regarding the development of this feature.

### Setting a State

A **State** keeps data that are used by the callback functions. Using this you can pass informations 
to and from the callback funtions. 

The **State** is configured to be saved whenewer the app is quitting or an error is triggered. So, any information passed to the **State** should implement a saving mechanism. If there is a reason for which 
an object within the **State** should not be saved, pass it's name to the *save_except* attribute 
during class initialization, or implement a *save_except:bool* attribute within the object itself. 

No builtin objects are save excepted by default. So if you need to pass an builtin object through the 
**State**, make sure to pass it's name to the *save_except*.

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

If you want to *MyConfig* from beeing saved, you can implement within the class the following:

```python

@dataclass
class MyConfig:
    save_except= True

```

or pass it's name to the *save_except*:

```python

state = State({'config':MyConfig()}, save_except= ['config'])
```

As we mentioned, a callback funtion can modify the **State** by returning an **OK** signal with *payload* containing a dictionary in the same format: **{name[str]:data[object]}**.

What happens when no *save* method exists and the object is not excepted? An **StateContentNotSavable** is raised during **State** initialization. 

### Setting the application

This is as simple as passing the **State** and **Layout** to the **Application** constructor and hit run.

```python

app = Application(layout=layout, state=state)

app.run()
```

### Setting callback functions

In order to do some stuff with all this we need some end function. The end functions should use the 
**State** and return a signal like *OK*, *Error*, *Abort*

Let's see an example:

```python
from squiffy import State
from squiffy.signals import OK, Error, Abort

def my_func(state:State) -> OK | Error | Abort:

    # do some stuff and return something

```

In order to save the results of the computation in the **State** you just pass a dictionary
with the *name_of_the_data* and the *actual_data_object* to the **OK.payload()**. 

If an error occured you can pass the following arguments to the **Error**: *origin*, *log_message*, *traceback*

```python

from squiffy import State
from squiffy.signals import OK, Error, Abort

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

We enjoy having an example ready to be explored. just write the following and enjoy our small and not-so-creative example.

```bash

python -m squiffy.example.example

```

or if this fails, try to write the following in a *.py* file.

```bash

from squiffy import example

if __name__ == "__main__":
    example.main()

```

## Future Developments

1. Include the rendering and display of the logo based on a logo_path.
2. Include a keybinding for visualizing the *help* information for each option on the menu.
3. Include special stylesheet for each submenu (not sure I will follow this path tho!)
4. Include error logging into dedicated file.
5. Separate the style sheet from the layout sheet.
6. Refactoring: improvements of the architecture, code redability, commenting and more.
7. Include keybindings for common options like: *return_to_previous*, *return_to_main*, *quit* and others.
8. Write tests!  
9. Window auto-resizing.

## Contributing

We accept contributions, sugestions and any thought on how to improve squiffy or what edge cases should be treated (ofc and new features suggestions). 

## License

Please see the License section.
