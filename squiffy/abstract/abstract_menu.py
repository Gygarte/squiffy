from abc import ABC, abstractmethod
from squiffy import signals


class AbstractObserver(ABC):
    """
    Abstract base class for an observer.
    """

    @abstractmethod
    def inform(self, payload: object | signals.Signal) -> None:
        """
        Informs the observer with the given payload.

        Parameters:
            payload (object): The payload to be passed to the observer.

        Returns:
            None
        """
        pass


class AbstractMenu(ABC):
    """
    Abstract base class for a menu.
    """

    @abstractmethod
    def show(self) -> None:
        """
        Runs the menu.

        Returns:
            None
        """
        pass

    @abstractmethod
    def _return_to_previous(self) -> None:
        """
        Returns to the previous menu.

        Returns:
            None
        """
        pass

    @abstractmethod
    def _return_to_main(self) -> None:
        """
        Returns to the main menu.

        Returns:
            None
        """
        pass

    @abstractmethod
    def handle_errors(self, error: object | signals.Signal) -> None:
        """
        Handles errors that occur during menu execution.

        Parameters:
            error (object): The error object.

        Returns:
            None
        """
        pass

    @abstractmethod
    def handle_signals(self, event: object | signals.Signal) -> None:
        """
        Handles events triggered during menu execution.

        Parameters:
            event (object): The event object.

        Returns:
            None
        """
        pass

    @abstractmethod
    def _quit(self) -> None:
        """
        Quits the menu.

        Returns:
            None
        """
        pass


class AbstractSubmenu(ABC):
    """
    Abstract base class for a submenu.
    """

    @abstractmethod
    def show(self) -> None:
        """
        Displays the submenu.

        Returns:
            None
        """
        pass

    @abstractmethod
    def handle_signals(self, event: object | signals.Signal) -> None:
        """
        Handles events triggered during submenu execution.

        Parameters:
            event (object): The event object.

        Returns:
            None
        """
        pass


class AbstractErrorSubmenu(ABC):
    @abstractmethod
    def show(self):
        pass


class AbstractItem(ABC):
    """
    Abstract base class for an item.
    """

    @abstractmethod
    def show():
        pass

    @abstractmethod
    def help():
        pass

    @abstractmethod
    def emit():
        pass


class AbstractItemsCollection(ABC):
    """
    Abstract base class for a collection of items.
    """

    @abstractmethod
    def show(self):
        """
        Shows the items in the collection.

        Returns:
            None
        """
        pass

    @abstractmethod
    def emit(self):
        """
        Activates the selected item.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_item(self) -> None:
        """
        Gets the selected item.

        Returns:
            None
        """
        pass

    @abstractmethod
    def add_item(self) -> None:
        """
        Adds an item to the collection.

        Returns:
            None
        """
        pass

    @abstractmethod
    def remove_item(self) -> None:
        """
        Removes an item from the collection.

        Returns:
            None
        """
        pass


class AbstractMenuObserversLayer(ABC):
    @abstractmethod
    def attach(self, observer: AbstractObserver) -> None:
        """
        Attaches an observer to the menu.

        Parameters:
            observer (Observer): The observer to be attached.

        Returns:
            None
        """
        pass

    @abstractmethod
    def detach(self, observer: AbstractObserver) -> None:
        """
        Detaches an observer from the menu.

        Parameters:
            observer (Observer): The observer to be detached.

        Returns:
            None
        """
        pass

    @abstractmethod
    def send(self, event: object | signals.Signal) -> None:
        """
        Sends an event to the observers. The Event is originated
        the a submenu and passes by the Menu to the MenuExtender

        Parameters:
            event (object): The event to be sent.

        Returns:
            None
        """
        pass

    @abstractmethod
    def handle_errors(self, error: object | signals.Signal) -> None:
        """
        Handles errors that occur during menu execution.

        Parameters:
            error (object): The error object.

        Returns:
            None
        """
        pass

    @abstractmethod
    def run(self) -> None:
        """
        Runs the menu.

        Returns:
            None
        """
        pass
