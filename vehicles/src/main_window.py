import tkinter as tk
from turtle import TurtleScreen
from . import objects
from . import entities
from . import agents
import ast
import shutil
import os


class MainWindow:

    def __init__(self, screen_size=(800, 600), object_type_list=('Heat Source', "Black Vehicle")):
        self.root = None
        self.canvas = None
        self.wn = None

        self.screen_size = screen_size
        self.max_width = int(self.screen_size[0] / 2 - 10)
        self.max_height = int(self.screen_size[1] / 2 - 10)

        self.top_interface_frame = None
        self.object_interface_dict = None

        self.num_starting_objects = 1
        self.object_type_list = object_type_list
        self.object_count_dict = {}
        self.object_list_dict = {}

        self.bottom_interface_frame = None
        self.start_button = None
        self.reset_button = None
        self.quit_button = None

        self.images_directory = "./images/"

        self.running = False

        self.create_object_info()
        self.create_window()
        self.create_objects()

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Braitenberg's Vehicles")

        self.create_top_interface()
        self.create_turtle_canvas()
        self.create_bottom_interface()


    def create_object_info(self):
        class_name_set = self.get_class_names_from_file("src/objects.py")

        for object_name in self.object_type_list:
            object_name_without_spaces = object_name.replace(" ", "")

            if object_name_without_spaces in class_name_set:
                self.object_count_dict[object_name] = self.num_starting_objects

    @staticmethod
    def get_class_names_from_file(file_path):
        with open(file_path, "r") as file:
            content = file.read()
            tree = ast.parse(content, filename=file_path)

        class_name_list = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        class_name_set = set(class_name_list)
        return class_name_set

    def create_top_interface(self):

        self.top_interface_frame = tk.Frame(self.root)
        self.top_interface_frame.pack()

        self.object_interface_dict = {}

        print(self.object_count_dict)
        for object_name in self.object_count_dict:
            self.create_object_interface(object_name)

    def create_object_interface(self, object_name):
        object_label = tk.Label(self.top_interface_frame, text=object_name)
        object_label.pack(side=tk.LEFT, padx=(10, 0))
        self.object_interface_dict[object_name+" label"] = object_label

        object_entry = tk.Entry(self.top_interface_frame, width=5)
        object_entry.insert(0, str(self.num_starting_objects))  # Set the default number of heat sources
        object_entry.pack(side=tk.LEFT)
        self.object_interface_dict[object_name + " entry"] = object_entry

    def create_turtle_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.screen_size[0],
                                height=self.screen_size[1])
        self.canvas.pack()
        self.wn = TurtleScreen(self.canvas)
        self.wn.onkey(self.start_stop, "space")
        self.wn.listen()
        self.wn.tracer(10, 10)
        self.wn.update()

    def create_bottom_interface(self):
        self.bottom_interface_frame = tk.Frame(self.root)
        self.bottom_interface_frame.pack()

        self.start_button = tk.Button(self.bottom_interface_frame, text="Start", fg="black", command=self.start_stop)
        self.reset_button = tk.Button(self.bottom_interface_frame, text="Reset", fg="black", command=self.reset)
        self.quit_button = tk.Button(self.bottom_interface_frame, text="Quit", fg="black", command=self.quit)

        self.start_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    def create_objects(self):
        for object_name, count in self.object_count_dict.items():
            self.object_list_dict[object_name] = []
            object_name_without_spaces = object_name.replace(" ", "")

            # Try to find the class in the objects module first
            class_reference = getattr(objects, object_name_without_spaces, None)

            # If not found in objects, try agents
            if class_reference is None:
                class_reference = getattr(agents, object_name_without_spaces, None)

            # If not found in agents, try entities
            if class_reference is None:
                class_reference = getattr(entities, object_name_without_spaces, None)

            # If still not found, raise an exception
            if class_reference is None:
                raise ValueError(
                    f"Class {object_name_without_spaces} not found in objects, agents, or entities modules.")

            # Create instances of the class and add them to the object list
            for _ in range(count):
                object_instance = class_reference(self)
                self.object_list_dict[object_name].append(object_instance)
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

    def quit(self):
        # Recursively delete everything in the specified directory
        if os.path.exists(self.images_directory):
            shutil.rmtree(self.images_directory)
            print(f"Deleted directory: {self.images_directory}")
        self.root.destroy()
