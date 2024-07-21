import json
from pathlib import Path
from squiffy.abstract.abstract_layout import AbstractLayoutFactory
from squiffy import utils, signals
from squiffy.menu import menu
from squiffy.menu import submenu
from squiffy.menu import menu_items
from squiffy.menu import error_submenu
from squiffy.screen import Screen
from .style import Style
from .style_factory import StyleFactory

# signals triggered from an option have the
# name following the template: "{SUBMENU_NAME}-{OPTION_NAME}"
# in upper case letters


class LayoutFactory(AbstractLayoutFactory):
    def __init__(self, layout_file_path: Path, error_handler=None) -> None:
        self._screen = Screen()
        self.error_handler = error_handler

        try:
            with open(layout_file_path, "r") as file:
                self._layout: dict = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Layout file not found at {layout_file_path}")
        except Exception:
            raise Exception(
                f"An error occured while trying to read the layout file at {layout_file_path}"
            )

    def create(self) -> menu.Menu:
        submenues = self._ansemble_submenu()
        error_handling = self._create_error_handling()

        return menu.Menu(
            submenu=submenues, main_submenu_idx=0, error_submenu=error_handling
        )

    def _ansemble_submenu(self) -> list[submenu.Submenu]:
        submenues: list[submenu.Submenu] = list([])

        for submenu_details in self._layout.get("submenu"):
            items: list[menu_items.Item] = list([])

            for option in submenu_details.get("options"):
                item = self._create_items(
                    item_details=option, parent_submenu=submenu_details.get("title")
                )

                items.append(item)

            items_collection = menu_items.ItemsCollection(
                uid=f"{submenu_details.get('title')}_items".upper(), items=items
            )
            # Configure the style
            if submenu_details.get("style") is None:
                style: Style = self._create_style()

            if submenu_details.get("main"):
                submenues.insert(
                    0,
                    self._create_submenu(
                        submenu_details=submenu_details,
                        items_collection=items_collection,
                        style=style,
                    ),
                )

            else:
                submenues.append(
                    self._create_submenu(
                        submenu_details=submenu_details,
                        items_collection=items_collection,
                        style=style,
                    )
                )

        return submenues

    def _create_submenu(
        self,
        submenu_details: dict,
        items_collection: menu_items.ItemsCollection,
        style: Style = None,
    ) -> submenu.Submenu:
        if submenu_details.get("logo") is not None:
            logo = self._import_logo(submenu_details.get("logo"))
        else:
            logo = None

        # Configure the style
        if style is None:
            style = self._create_style(submenu_details.get("style"))

        return submenu.Submenu(
            title=submenu_details.get("title"),
            items=items_collection,
            logo=logo,
            style=style,
            header_msg=submenu_details.get("header_msg"),
            footer_msg=submenu_details.get("footer_msg"),
            add_return=submenu_details.get("return_to_previous"),
            add_return_to_main=submenu_details.get("return_to_main"),
            add_quit=submenu_details.get("quit"),
        )

    def _create_items(self, item_details: dict, parent_submenu: str) -> menu_items.Item:
        if item_details.get("include_help") is True:
            help = item_details.get("help")
        else:
            help = None

        # Check for menu switch and append the appropriate signal
        if item_details.get("switch") is not None:
            swith_to = item_details.get("switch")

            return menu_items.Item(
                option=item_details.get("option"),
                signal=signals.SwitchSubmenu(target_id=swith_to),
                help=help,
            )

        return menu_items.Item(
            option=item_details.get("option"),
            signal=signals.Do(
                utils.generate_signal_name(parent_submenu, item_details.get("option"))
            ),
            help=help,
        )

    def _create_error_handling(self) -> error_submenu.ErrorSubmenu:
        _info: dict = self._layout.get("error_handling")

        if _info.get("include"):
            if _info.get("logger_path") is not None:
                logger = self._create_logger(_info.get("logger_path"))
                return error_submenu.ErrorSubmenu(logger=logger)

            else:
                return error_submenu.ErrorSubmenu()
        else:
            return self.error_handler

    def _create_style(self, style_sheet: dict | None = None) -> Style:
        style_factory = StyleFactory(screen=self._screen)

        if style_sheet is None:
            return style_factory.create(style_sheet=self._layout.get("default_style"))

    def _import_logo(self, logo_path) -> str:
        pass

    def _create_logger(self, log_path: Path):
        pass
