class Menu_tab:
    def __init__(self, menu_id: int, img_file_path: str, pos: (int, int), name: str) -> None:
        self.name = name
        self.id = menu_id
        self.pos = pos
        self.img_file_path = img_file_path

    def __str__(self) -> str:
        return f"{self.name} tab using :" + self.name + f" @ {self.pos}"

    def get_img_file_path(self) -> str:
        return self.img_file_path

    def get_pos(self) -> (int, int):
        return self.get_pos

    def get_id(self) -> int:
        return self.pos

    def get_name(self) -> str:
        return self.name
    pass


MAIN_MENU = 0
INVENTORY = 1
TRADERS = 2
FLEA_MARKET = 3

tabs = [Menu_tab(MAIN_MENU, 'menu_tabs//main_menu.png', (100, 1420), 'main_menu'), Menu_tab(INVENTORY, 'menu_tabs//character.png', (1306, 1420), 'character'),
        Menu_tab(TRADERS, 'menu_tabs//traders.png', (1480, 1420), 'traders'), Menu_tab(FLEA_MARKET, 'menu_tabs//flea_market.png', (1620, 1420), 'flea market')]
