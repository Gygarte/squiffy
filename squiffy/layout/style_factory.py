import os
from squiffy.abstract import abstract_style
from .style_components import StyleHeader, StyleFooter, StyleContent, Padding
from .style import Style


class StyleFactory(abstract_style.AbstractStyleFactory):
    def __init__(self) -> None:
        self._header: abstract_style.AbstractStyleHeader = None
        self._footer: abstract_style.AbstractStyleFooter = None
        self._content: abstract_style.AbstractStyleContent = None
        self._help: abstract_style.AbstractStyleHelp = None
        self._border: str = None

        # Upon initializationm the screen size is provided by the "get_terminal_size"
        self._screen_hight: int = os.get_terminal_size().lines
        self._screen_width: int = os.get_terminal_size().columns

    def create(self, style_sheet: dict) -> Style:
        self._parse_style_sheet(style_sheet)

        return Style(
            header=self._header,
            footer=self._footer,
            content=self._content,
        )

    def _parse_style_sheet(self, style_sheet: dict) -> None:
        if style_sheet["dimensions"]["type"] == "auto":
            _padding_info: dict = style_sheet.get("padding")
            padding = Padding(
                top=_padding_info.get("top"),
                bottom=_padding_info.get("bottom"),
                left=_padding_info.get("left"),
                right=_padding_info.get("right"),
            )

            self._header = StyleHeader(
                max_dimensions=(self._screen_hight, self._screen_width),
                padding=padding,
                border=style_sheet["border"]["type"],
            )

            self._footer = StyleFooter(
                max_dimensions=(self._screen_hight, self._screen_width),
                padding=padding,
                border=style_sheet["border"]["type"],
            )

            self._content = StyleContent(
                max_dimensions=(self._screen_hight, self._screen_width),
                padding=padding,
                border=style_sheet["border"]["type"],
            )
