from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np
import matplotlib.pyplot as plt

model = load_model('mnist_cnn.h5')

def predict_digit(img):
    
    #resie image to 28x28
    img = img.resize((28,28))
    
    #convert rgb to grayscale and turn to array
    img = img.convert('L')
    img = np.array(img)
    
    #reshaping to be an accetable input to the cnn and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    
    #plot image to see if imageGrab is centered
    plt.imshow(img[0,:,:,0],cmap='gray')
    plt.show()
    
    #predicting the class
    res = model.predict([img])[0]
    
    #returning the argmax and its probability
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = 0 
        self.y = 0

        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "black", cursor="cross")
        self.label = tk.Label(self, text="Draw a number", font=("Comic Sans", 48))
        self.classify_btn = tk.Button(self, text = "Predict", command = self.predictions) 
        self.clear_btn = tk.Button(self, text = "Erase", command = self.erase)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2)
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.clear_btn.grid(row=1, column=0, pady=2, padx =2)

        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def erase(self):
        self.canvas.delete("all")

    def predictions(self):

        im = ImageGrab.grab((200,200,500,500))
        digit, acc = predict_digit(im)
        self.label.configure(text='Prediction: ' + str(digit)+
                             '\n Probability '+ str(int(acc*100))+'%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=7
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white',outline="white")

app = App()
mainloop()