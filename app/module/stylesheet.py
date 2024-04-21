# coding: utf-8
import os.path
from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    LINK_CARD = "link_card"
    SAMPLE_CARD = "sample_card"
    HOME_INTERFACE = "home_interface"
    AUDIO_INTERFACE = "audio_interface"
    VIEW_INTERFACE = "view_interface"
    FRAME = "frame"
    TAB = "tab"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f"./resources/qss/{theme.value.lower()}/{self.value}.qss"

