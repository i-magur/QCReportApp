from .welcome import WelcomePage
from .home import HomePage
from .data import LoadedDataPage

FRAMES = [
    WelcomePage,
    HomePage,
    LoadedDataPage
]
START_PAGE = WelcomePage
