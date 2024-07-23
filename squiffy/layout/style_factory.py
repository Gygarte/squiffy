from squiffy.screen import Screen
from squiffy.abstract import abstract_style
from .style_components import StyleHeader, StyleFooter, StyleContent, Padding
from .style import Style


class StyleFactory(abstract_style.AbstractStyleFactory):
    def __init__(self, screen: Screen) -> None:
        self._screen: Screen = screen

        self._header: abstract_style.AbstractStyleHeader = None
        self._footer: abstract_style.AbstractStyleFooter = None
        self._content: abstract_style.AbstractStyleContent = None
        self._help: abstract_style.AbstractStyleHelp = None
        self._border: str = None

    def create(self, style_sheet: dict) -> Style:
        self._parse_style_sheet(style_sheet)

        return Style(
            screen=self._screen,
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
                max_dimensions=(self._screen.hight, self._screen.width),
                padding=padding,
                border=style_sheet["border"]["type"],
            )

            self._footer = StyleFooter(
                max_dimensions=(self._screen.hight, self._screen.width),
                padding=padding,
                border=style_sheet["border"]["type"],
            )

            self._content = StyleContent(
                max_dimensions=(self._screen.hight, self._screen.width),
                padding=padding,
                border=style_sheet["border"]["type"],
            )
