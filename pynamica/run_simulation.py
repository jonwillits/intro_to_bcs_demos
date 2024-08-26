from src.display import main_window
import params

def main():
    param_dict = params.get_param_dict()
    turtle_window = main_window.MainWindow(param_dict)
    turtle_window.wn.mainloop()


main()
