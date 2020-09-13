import tkinter as tk
import os
from PIL import Image, ImageTk
import shutil
from datetime import datetime

class ManualClassification():
    
    def __init__(self, images_path, classes):
        self.images_path = images_path # location of images to classify
        self.classes = classes # classes to use for classification
        
        self.image_count = 0 # keep track of index in images list (defined below)
        
        # save list of strings, where each element is the full path of an image to be classified
        self.images = [os.path.join(images_path,img) for img in os.listdir(images_path)]
        
        # Dimensions of tkinter window
        self.window_width = 1000
        self.window_height = 1000
        
        self.data = dict()
        for Class in self.classes:
            self.data[Class] = []
        
    def create_window(self):
        
        # Create Tkinter window, specify window size
        self.main_window = tk.Tk()
        self.main_window.geometry(str(self.window_width)+"x"+str(self.window_height))

        # Add title to the window
        self.main_window.title("Label Data")
        
        # Create the canvas (where image will get shown). Size in pixels.
        self.canvas = tk.Canvas(self.main_window, width=300, height=200)

        # Pack the canvas into a frame/form
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # load the image file
        photo = self.get_image()

        # Put image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.image_on_canvas = self.canvas.create_image(50, 10, image=photo, 
                                      anchor=tk.NW)
        
        # Create folders and buttons per class. Will store classified images into respective folders.
        for Class in self.classes:
            print("for class:",Class)
            if not os.path.exists(Class):
                os.mkdir(Class)
            self.create_button(Class, lambda theclass=Class: self.mark_class(theclass))
            
        # Create a skip button in case user wants to disregard (not classify) an image shown
        self.create_button("SKIP", self.next_image, "blue", "blue3", "white")
        
        # Create a save button
        self.create_button("SAVE", self.save, "green", "green3", "white")
            
        # Create a quit button so user may exit the application
        self.create_button("QUIT", self.main_window.destroy, "red", "red3", "white")
        
        self.main_window.mainloop()
        
    def get_image(self):
        
        # Get path to image from list of paths
        image_path = self.images[self.image_count]
        
        # Load image
        image = Image.open(image_path)
        
        print("Image path:",image_path)
        
        # Resize/scale image so it fits the GUI window
        width, height = image.size
        scale = max(height,width)/(self.window_height - (self.window_height/7))
        image = image.resize((int(width/scale), int(height/scale)))
        
        # Turn image into a Tkinter-compatible photo image
        compatible_image = ImageTk.PhotoImage(image)
        
        return compatible_image
    
    def create_button(self, text, command, activebg=None, bg=None, fg=None):
    
        button = tk.Button(self.main_window, text=text, 
                           width=25, command= command, 
                           activebackground=activebg, bg=bg, fg=fg)
        button.pack()
        
    def mark_class(self, Class):
        print("class:",Class)
        
        # copy image to class folder
        shutil.copy(self.images[self.image_count], Class)
        
        # add image path to class key in data dictionary
        self.data[Class].append(self.images[self.image_count])
        
        # show next image
        self.next_image()
        
    def next_image(self):
        
        # show next image
        self.image_count += 1
        
        #global new_image 
        self.new_image = self.get_image()
        self.canvas.itemconfigure(self.image_on_canvas, image = self.new_image)
        
    def save(self):
        string = ""
        print(self.data)
        for a_class,paths in self.data.items():
            for path in paths:
                string += a_class + " " + path + "\n"
        f = open("annotations.txt", "w")
        f.write(string)
        f.close()
        print("saved at",datetime.now())
        
        
def main():
    
    classes = ["crowd","not_crowd"]
    images_path = "/home/mramos/Documents/Git/RickyRenuncia_Protests/downloaded_media"

    app = ManualClassification(images_path,classes)

    app.create_window()
    
main()