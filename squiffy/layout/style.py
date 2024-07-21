from squiffy.abstract import abstract_style


class Style(abstract_style.AbstractStyle):
    def __init__(
        self,
        screen: abstract_style.AbstractScreen,
        header: abstract_style.AbstractStyleHeader = None,
        content: abstract_style.AbstractStyleContent = None,
        footer: abstract_style.AbstractStyleFooter = None,
        help: abstract_style.AbstractStyleHelp = None,
    ) -> None:
        self._screen = screen
        self._header = header
        self._content = content
        self._footer = footer
        self._help = help

    def create(
        self, title: str, subtitle: str, header_msg: str, content: dict, footer_msg: str
    ) -> str:
        self._header.title = title
        self._header.subtitle = subtitle
        self._header.message = header_msg
        self._content.content = content
        self._footer.message = footer_msg

        return "\n".join(
            [self._header.create(), self._content.create(), self._footer.create()]
        )
