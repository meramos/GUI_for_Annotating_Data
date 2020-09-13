import tkinter as tk
import os
from PIL import Image, ImageTk

class ManualClassification():
    
    def __init__(self, images_path, classes):
        self.images_path = images_path
        self.classes = classes
        
        self.image_count = 0
    
        self.images = [os.path.join(images_path,img) for img in os.listdir(images_path)]
        
        self.window_width = 1000
        self.window_height = 1000
        
    def create_window(self):
        
        self.main_window = tk.Tk()
        self.main_window.geometry(str(self.window_width)+"x"+str(self.window_height))

        self.main_window.title("Label Data")

        # create the canvas, size in pixels
        self.canvas = tk.Canvas(self.main_window, width=300, height=200)

        # pack the canvas into a frame/form
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # load the .gif image file
        photo = self.get_image()

        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.image_on_canvas = self.canvas.create_image(50, 10, image=photo, 
                                      anchor=tk.NW)
        
        for Class in self.classes:
            self.create_button(Class)
        
        self.main_window.mainloop()
        
    def get_image(self):
        
        image_path = self.images[self.image_count]
        
        image = Image.open(image_path)
        
        print("Image path:",image_path)
        
        width, height = image.size
        
        scale = int(max(height,width)/(self.window_height - 100))
        
        image = image.resize((int(width/scale), int(height/scale)))
        
        return ImageTk.PhotoImage(image)
    
    def create_button(self, Class):
    
        button = tk.Button(self.main_window, text=Class, 
                           width=25, command= lambda:self.mark_class(Class))
        button.pack()
        
    def mark_class(self, Class):
        print("Class selected",Class)
        
        self.image_count += 1
        
        # show next image
        new_image = self.get_image()
        self.canvas.itemconfigure(self.image_on_canvas, image = new_image)
        
        
def main():
    
    classes = ["crowd","not_crowd"]
    images_path = "/home/mramos/Documents/Git/RickyRenuncia_Protests/downloaded_media"

    app = ManualClassification(images_path,classes)

    app.create_window()
    
main()