import shutil
import os
import importlib.util
import tkinter as tk
from turtle import TurtleScreen
from .. import utils


class MainWindow:

    def __init__(self, param_dict):
        self.root = None

        self.param_dict = param_dict

        self.screen_size = (param_dict['Display']['width'], param_dict['Display']['height'])
        self.max_width = int(self.screen_size[0] / 2 - 10)
        self.max_height = int(self.screen_size[1] / 2 - 10)

        self.top_interface_frame = None
        self.entity_interface_dict = None
        self.class_names_dict = None

        self.canvas = None
        self.wn = None

        self.bottom_interface_frame = None
        self.start_button = None
        self.reset_button = None
        self.quit_button = None

        self.images_directory = "./images/"
        self.entity_count_dict = {}
        self.entity_list_dict = {}
        self.class_names_set = None

        self.running = False

        self.create_entity_info()
        self.create_window()
        self.create_entities()

    def create_entity_info(self):
        class_file_list = utils.list_py_files("src/entities/") + utils.list_py_files("src/agents/")
        self.class_names_dict = utils.get_class_names_set_from_files(class_file_list)

        for key in self.param_dict:
            if key != "Display":
                if key in self.class_names_dict:
                    if 'count' in self.param_dict[key]:
                        self.entity_count_dict[key] = self.param_dict[key]['count']
                    else:
                        self.entity_count_dict[key] = 0


    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Pynamica")

        self.create_top_interface()
        self.create_turtle_canvas()
        self.create_bottom_interface()

    def create_top_interface(self):

        self.top_interface_frame = tk.Frame(self.root)
        self.top_interface_frame.pack()

        self.entity_interface_dict = {}

        for entity_name, count in self.entity_count_dict.items():
            if count > 0:
                self.create_entity_interface(entity_name)

    def create_entity_interface(self, entity_name):
        entity_label = tk.Label(self.top_interface_frame, text=entity_name)
        entity_label.pack(side=tk.LEFT, padx=(10, 0))
        self.entity_interface_dict[entity_name+" label"] = entity_label

        entity_entry = tk.Entry(self.top_interface_frame, width=5)
        entity_entry.insert(0, str(self.param_dict[entity_name]['count']))
        entity_entry.pack(side=tk.LEFT)
        self.entity_interface_dict[entity_name + " entry"] = entity_entry

    def create_turtle_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.screen_size[0],
                                height=self.screen_size[1])
        self.canvas.pack()
        self.wn = TurtleScreen(self.canvas)
        self.wn.onkey(self.start_stop, "space")
        self.wn.listen()
        self.wn.tracer(0, 0)
        self.wn.update()

    def create_bottom_interface(self):
        self.bottom_interface_frame = tk.Frame(self.root)
        self.bottom_interface_frame.pack()

        self.start_button = tk.Button(self.bottom_interface_frame, text="Start", fg="black", command=self.start_stop)
        # noinspection DuplicatedCode
        self.reset_button = tk.Button(self.bottom_interface_frame, text="Reset", fg="black", command=self.reset)
        self.quit_button = tk.Button(self.bottom_interface_frame, text="Quit", fg="black", command=self.quit)

        self.start_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    def create_entities(self):

        for entity_name, count in self.entity_count_dict.items():
            self.entity_list_dict[entity_name] = []

            if entity_name in self.class_names_dict:
                for i in range(count):
                    class_path = self.class_names_dict[entity_name]
                    module_name = os.path.splitext(os.path.basename(class_path))[0]
                    spec = importlib.util.spec_from_file_location(module_name, class_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Get the class object using getattr
                    class_obj = getattr(module, entity_name)

                    # Create an instance of the class
                    instance = class_obj(self, str(i+1))
                    self.entity_list_dict[entity_name].append(instance)
        #
        #     # Try to find the class in the objects module first
        #     class_reference = getattr(entities, entity_name, None)
        #
        #     # If not found in objects, try agents
        #     if class_reference is None:
        #         class_reference = getattr(agents, entity_name, None)
        #
        #     # If not found in agents, try entities
        #     if class_reference is None:
        #         class_reference = getattr(entities, entity_name, None)
        #
        #     # If still not found, raise an exception
        #     if class_reference is None:
        #         raise ValueError(
        #             f"Class {object_name_without_spaces} not found in objects, agents, or entities modules.")
        #
        #     # Create instances of the class and add them to the object list
        #     for i in range(count):
        #         object_instance = class_reference(self, str(i+1))
        #         print(object_instance)
        #         self.object_list_dict[object_name].append(object_instance)
        self.wn.update()

    def start_stop(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
        else:
            self.running = True
            self.start_button.config(text="Pause")
            self.run_simulation()

    def run_simulation(self):
        if not self.running:
            return

        for object_type, object_list in self.object_list_dict.items():
            for current_object in object_list:
                current_object.update()
        self.wn.update()
        self.root.after(10, self.run_simulation)

    def reset(self):
        pass
        # self.vehicle_list = []
        # self.heat_source_list = []
        #
        # self.wn.clear()
        # self.wn.tracer(0, 0)
        # self.create_heat_sources()
        # self.create_vehicles()
        # self.wn.update()

    # def on_screen_click(self, x, y):
    #     # This function will be called whenever the screen is clicked
    #     print(f"Screen clicked at ({x}, {y})")

    @staticmethod
    def clear_directory(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    def quit(self):
        # Recursively delete everything in the specified directory
        if os.path.exists(self.images_directory):
            self.clear_directory(self.images_directory)
        self.root.destroy()
