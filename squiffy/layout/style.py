from squiffy.abstract import abstract_style


class Style(abstract_style.AbstractStyle):
    def __init__(
        self,
        autoscale: bool,
        header: abstract_style.AbstractStyleHeader = None,
        content: abstract_style.AbstractStyleContent = None,
        footer: abstract_style.AbstractStyleFooter = None,
        helps: abstract_style.AbstractStyleHelp = None,
    ) -> None:
        self._autoscale = autoscale
        self._header = header
        self._content = content
        self._footer = footer
        self._help = helps

    def create(
        self,
        title: str,
        subtitle: str,
        header_msg: str,
        content: dict,
        footer_msg: str,
    ) -> str:
        self._header.title = title
        self._header.subtitle = subtitle
        self._header.message = header_msg

        self._content.content = content

        self._footer.message = footer_msg

        return "\n".join(
            [self._header.create(), self._content.create(), self._footer.create()]
        )

    def set_dimensions(self, height: int, width: int) -> None:
        if self._header is not None:
            self._header.set_dimensions(height, width)

        if self._content is not None:
            self._content.set_dimensions(height, width)

        if self._footer is not None:
            self._footer.set_dimensions(height, width)

        if self._help is not None:
            self._help.set_dimensions(height, width)

    @property
    def autoscale(self) -> bool:
        return self._autoscale
