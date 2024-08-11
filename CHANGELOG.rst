==================
Changelog
==================


Version 0.1.2 (2024-08-12)
--------------------------

* [bugfix] Fixed the initialization of the State. The previous versions 
included the mention of initializing the State with a custom dictionary, which was
not implemented. This has been fixed now.
* Changed method name in State from "load" to "update", which makes more sense in this context.
* Changed module name: "context2" become "context". Additionally included some explanations
regarding the usage of the Context in the overall architecture.
* [bugfix] Fixed the issue with errors raised when the the user selects an option
with no callback functions attached to it. The issue come from the fact that the Context
was looking for an Executor with the option signature and failled, raising KeyError. Now, 
the error is ignored, forcing the desired behaviour.
* Additional changes in naming, commenting and type returned by functions.
* [bugfix] Changes the method acces from the Executor class when an error should be raised. The Context
did not have a dedicated method for error handling, but hangles them through "handle_signal". 
The previous implementation of Executor accessed the "handle_error" not "handle_signal" methods. 
Fixed now.
* [tests] Added tests for the State and Context classes.
* [documentation] Created and updated the CHANGELOG.

Version 0.1.1 (2024-08-07)
--------------------------

* [bugfix] Resolve issue with accessing the example. The previous version did not permit 
to access the example from the CLI or by import. The issue has been resolved now.
* [documentation] Update README. Included new instructions for accessing the example.

Version 0.1.0 (2024-08-07)
--------------------------

* Initial release

