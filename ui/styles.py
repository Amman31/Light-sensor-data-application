def apply_main_style(main_window):
    """Apply the main application stylesheet from a .qss file"""
    try:
        with open("assets/stylesheet/style.qss", "r") as f:
            main_window.setStyleSheet(f.read())
    except FileNotFoundError:
        print("style.qss not found.")