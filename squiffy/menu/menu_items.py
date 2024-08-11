import rich.pretty as rp
from prompt_toolkit import print_formatted_text as print
from traceback import format_exc
from typing import Optional, Union
from squiffy.abstract.abstract_menu import AbstractItem, AbstractItemsCollection
from squiffy import signals
from squiffy import utils


class Item(AbstractItem):
    """
    A class that represents an item in a menu.
    The item represent an option that the user can select
    and which triggers an action or an event.

    The events could be handled by the Submenu in which the Item
    resides or by an external controller. The Item does not care.

    """

    def __init__(
        self,
        option: str,
        signal: signals.Signal,
        help: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        self._option = option.upper()
        self._signal = signal
        self._help = help

        self.args = args
        self.kwargs = kwargs

    def show(self) -> str:
        return self._option

    def help(self) -> None:
        if self._help is not None:
            print(self._help)
            utils.take_break()
        else:
            print(f"No help available for {self._option}")
            utils.take_break()

        return

    def emit(self) -> signals.Signal:
        return self._signal

    def __repr__(self) -> str:
        return self._option


class ItemsCollection(AbstractItemsCollection):
    """
    Keeps an collection of items and provides methods to
    access the items and manipulate them

    """

    def __init__(self, uid: str, items: list[Item]) -> None:
        self.__items = items
        self.__items_tree: dict[int, Item] = dict({})
        self._update_tree()

        self.__uid: str = uid

    def show(self) -> None:
        rp.pprint(self.__items_tree, expand_all=True, indent_guides=True)

    def emit(
        self, idx: int
    ) -> Union[
        signals.SwitchSubmenu,
        signals.ReturnToMain,
        signals.ReturnToPrevious,
        signals.Signal,
        signals.OK,
        signals.Do,
        signals.Error,
    ]:
        try:
            item = self.get_item(idx)
        except KeyError:
            # TODO: Refactor, if an option does not exist why should the user be able to select it? Raise an error
            # in this case or route the error to the menu?
            return signals.Error(
                origin=self.__uid, log_message="Item not found", traceback=format_exc()
            )

        except Exception:
            return signals.Error(
                origin=self.__uid,
                log_message="""An error occurred within ItemsCollection or Item instance.
                                                Check the traceback for more information.""",
                traceback=format_exc(),
            )
        else:
            return item.emit()

    def add_item(self, item: Item) -> None:
        self.__items.append(item)
        self._update_tree()

    def remove_item(self, index: int = -1) -> None:
        self.__items.pop(index)
        self._update_tree()

    def get_item(self, index: int) -> Item:
        return self.__items[index]

    def _update_tree(self) -> None:
        for index, item in enumerate(self.__items):
            self.__items_tree.update({index: item})

    def __len__(self) -> int:
        return len(self.__items)

    @property
    def items(self) -> dict:
        return self.__items_tree
