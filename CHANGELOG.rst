==================
Changelog
==================

Version 0.1.3 (2024-08-28)
--------------------------

* [Bugfix] Fixed the issue with the error raised by the *Application* class when am *signal.Abort* is handled. The initial error was raised due to the fact that the *handle_abordt* method did not accepted the signal as an argument. The issue has been fixed now.
* [Bugfix] Fixed quitting mechanism. The previous implementation did not autosave the state while quitting the application. The issue has been fixed now.
* [Miscellaneous] Improved the **State** class. Added *save_except* attribute, which define which values from the state are excepted from saving. Additionally added checks for the existance of *save* method in each object in the *State*. The *save_except* mechanism nullify the pre-check for the mentioned objects.
* [Miscellaneous] Added the **StateContentNotSavable** exception, which is raised when the *save* method is not implemented in the objects within the *State* class.
* [Tests] Added unit test for *Application* class. Tested if signals returned from a callback function trigger an error (Error signal is tested for triggering the error handler, alongside unexpected errors). 
* [Tests] Additionally, tested if the quitting mechanism triggered the *save* method of the **State** during the quitting process and all its implications. Added testing for the State pre-checks method. 
* [Documentation] Improved the documentation. Added more information about the *State* class and its implications. Additionally, added information about the *save_except* attribute and the *StateContentNotSavable* exception.

Version 0.1.2 (2024-08-12)
--------------------------

* [Bugfix] Fixed the initialization of the State. The previous versions included the mention of initializing the State with a custom dictionary, which was not implemented. This has been fixed now.
* [Bugfix] Changes the method accesed from the Executor class when an error should be raised. The Context did not have a dedicated method for error handling, but hangles them through "handle_signal".  The previous implementation of Executor accessed the "handle_error" not "handle_signal" methods.  Fixed now.
* [Bugfix] Fixed the issue with errors raised when the the user selects an option with no callback functions attached to it. The issue come from the fact that the Context was looking for an Executor with the option signature and failled, raising KeyError. Now, the error is ignored, forcing the desired behaviour.
* [Tests] Added tests for the State and Context classes.
* [Documentation] Created and updated the CHANGELOG.
* [Miscellaneous] Changed method name in State from "load" to "update", which makes more sense in this context.
* [Miscellaneous] Changed module name: "context2" become "context". Additionally included some explanations regarding the usage of the Context in the overall architecture.
* [Miscellaneous] Additional changes in naming, commenting and type returned by functions.

Version 0.1.1 (2024-08-07)
--------------------------

* [Bugfix] Resolve issue with accessing the example. The previous version did not permit to access the example from the CLI or by import. The issue has been resolved now.
* [Documentation] Update README. Included new instructions for accessing the example.

Version 0.1.0 (2024-08-07)
--------------------------

* Initial release

