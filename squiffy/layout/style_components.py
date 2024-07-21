import textwrap
from typing import Union
from squiffy.abstract import abstract_style
from .contants import STANDARD_WIDTH


class TextGenerator:
    def generate(
        self,
        screen_h: int,
        screen_w: int,
        border_style: str,
        padding_top: int,
        padding_bottom: int,
        padding_left: int,
        padding_right: int,
        texts: list[str],
        alignment: str = "center",
    ) -> str:
        if STANDARD_WIDTH > screen_w:
            total_width = screen_w
        else:
            total_width = STANDARD_WIDTH

        interior_width = total_width - padding_left - padding_right - 2

        form = list([])

        form.append(border_style * total_width)
        if padding_top > 0:
            for _ in range(padding_top):
                form.append(
                    self.row(
                        width=total_width,
                        border_style=border_style,
                        padding_left=padding_left,
                        padding_right=padding_right,
                        alignment=alignment,
                    )
                )

        for text in texts:
            for line in self.wrap_text(text, interior_width):
                form.append(
                    self.row(
                        width=total_width,
                        border_style=border_style,
                        padding_left=padding_left,
                        padding_right=padding_right,
                        text=line,
                        alignment=alignment,
                    )
                )

        if padding_bottom > 0:
            for _ in range(padding_bottom):
                form.append(
                    self.row(
                        width=total_width,
                        border_style=border_style,
                        padding_left=padding_left,
                        padding_right=padding_right,
                        alignment=alignment,
                    )
                )

        form.append(border_style * total_width)

        return "\n".join(form)

    @staticmethod
    def row(
        width: int,
        border_style: str,
        padding_left: int,
        padding_right: int,
        alignment: str = "center",
        text: Union[str, None] = None,
    ) -> str:
        if text is None:
            margins: int = width - padding_left - padding_right - 2
            return (
                border_style
                + margins * " "
                + padding_left * " "
                + padding_right * " "
                + border_style
            )

        assert len(text) <= width, "Text is too long for the given width"

        if alignment == "center":
            if len(text) % 2 != 0:
                left_margin: int = int(
                    ((width - padding_left - padding_right - 2) - len(text)) / 2
                )
                right_margin = left_margin + 1
            else:
                left_margin: int = int(
                    ((width - padding_left - padding_right - 2) - len(text)) / 2
                )
                right_margin = left_margin

            return (
                border_style
                + padding_left * " "
                + left_margin * " "
                + text
                + right_margin * " "
                + padding_right * " "
                + border_style
            )
        elif alignment == "left":
            right_margin: int = (
                width - padding_left - padding_right - len(text) - 2
            )  # the borders

            return (
                border_style
                + padding_left * " "
                + text
                + right_margin * " "
                + padding_right * " "
                + border_style
            )

        elif alignment == "right":
            left_margin: int = (
                width - padding_left - padding_right - len(text) - 2
            )  # the borders

            return (
                border_style
                + padding_left * " "
                + left_margin * " "
                + text
                + padding_right * " "
                + border_style
            )

    @staticmethod
    def wrap_text(text: str, max_width: int) -> list[str]:
        if len(text) > max_width:
            return textwrap.wrap(text, max_width)
        else:
            return [text]


class Padding(abstract_style.AbstractPadding):
    def __init__(self, top: int, bottom: int, left: int, right: int) -> None:
        self._top = top
        self._bottom = bottom
        self._left = left
        self._right = right

    @property
    def top(self) -> int:
        return self._top

    @property
    def bottom(self) -> int:
        return self._bottom

    @property
    def left(self) -> int:
        return self._left

    @property
    def right(self) -> int:
        return self._right


class StyleHeader(abstract_style.AbstractStyleHeader):
    def __init__(
        self, max_dimensions: tuple[int, int], padding: Padding, border: str
    ) -> None:
        self._title: str = None
        self._subtitle: str = None
        self._message: str = None

        self._screen_hight: int = max_dimensions[0]
        self._screen_width: int = max_dimensions[1]

        self._padding: Padding = padding
        self._border: str = border

    def create(self) -> str:
        text_generator = TextGenerator()
        return text_generator.generate(
            screen_h=self._screen_hight,
            screen_w=self._screen_width,
            border_style=self._border,
            padding_top=self._padding.top,
            padding_bottom=self._padding.bottom,
            padding_left=self._padding.left,
            padding_right=self._padding.right,
            texts=[self._title, self._subtitle, self._message],
            alignment="left",
        )

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def subtitle(self) -> str:
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle: str) -> None:
        self._subtitle = subtitle

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, message: str) -> None:
        self._message = message

    @property
    def hight(self) -> int:
        return self._screen_hight

    @hight.setter
    def hight(self, hight: int) -> None:
        self._screen_hight = hight

    @property
    def width(self) -> int:
        return self._screen_width

    @width.setter
    def width(self, width: int) -> None:
        self._screen_width = width

    @property
    def padding(self) -> Padding:
        return self._padding

    @padding.setter
    def padding(self, padding: Padding) -> None:
        self._padding = padding


class StyleFooter(abstract_style.AbstractStyleFooter):
    def __init__(
        self, max_dimensions: tuple[int, int], padding: Padding, border: str
    ) -> None:
        self._message: str = None

        self._hight: int = max_dimensions[0]
        self._width: int = max_dimensions[1]

        self._padding: Padding = padding
        self._border: str = border

    def create(self) -> str:
        text_generator = TextGenerator()
        return text_generator.generate(
            screen_h=self._hight,
            screen_w=self._width,
            border_style=self._border,
            padding_top=self._padding.top,
            padding_bottom=self._padding.bottom,
            padding_left=self._padding.left,
            padding_right=self._padding.right,
            texts=[self._message],
            alignment="left",
        )

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, message: str) -> None:
        self._message = message

    @property
    def hight(self) -> int:
        return self._hight

    @hight.setter
    def hight(self, hight: int) -> None:
        self._hight = hight

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @property
    def padding(self) -> Padding:
        return self._padding

    @padding.setter
    def padding(self, padding: Padding) -> None:
        self._padding = padding


class StyleContent(abstract_style.AbstractStyleContent):
    def __init__(
        self, max_dimensions: tuple[int, int], padding: Padding, border: str
    ) -> None:
        self._content: list[str] = None

        self._hight: int = max_dimensions[0]
        self._width: int = max_dimensions[1]

        self._padding: Padding = padding
        self._border: str = border

    def create(self) -> str:
        text_generator = TextGenerator()
        return text_generator.generate(
            screen_h=self._hight,
            screen_w=self._width,
            border_style=self._border,
            padding_top=self._padding.top,
            padding_bottom=self._padding.bottom,
            padding_left=self._padding.left,
            padding_right=self._padding.right,
            texts=self._content,
            alignment="left",
        )

    @property
    def content(self) -> list[tuple[int, str]]:
        return self._content

    @content.setter
    def content(self, content: dict[str, str]) -> None:
        self._content = [f"{key}>>>{value}" for key, value in content.items()]

    @property
    def hight(self) -> int:
        return self._hight

    @hight.setter
    def hight(self, hight: int) -> None:
        self._hight = hight

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @property
    def padding(self) -> Padding:
        return self._padding

    @padding.setter
    def padding(self, padding: Padding) -> None:
        self._padding = padding
