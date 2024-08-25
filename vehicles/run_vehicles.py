from src import main_window


def main():
    screen_size = (800, 600)
    object_type_list = ["Heat Source"]
    turtle_window = main_window.MainWindow(screen_size, object_type_list)
    turtle_window.wn.mainloop()


main()
