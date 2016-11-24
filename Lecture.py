def lecture_circuit():
    root = tk.Tk()
    
    root.withdraw()
    
    circuit = dial.askopenfile(mode='r',filetypes=[('images JPG', '.jpg')])
    
    im = imageio.imread(circuit.name)
    
    root.destroy()
    
    return im


if __name__=='__main__':
    import imageio
    import tkinter as tk
    from tkinter import filedialog as dial
    
    lecture_circuit()