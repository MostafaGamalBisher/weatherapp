import tkinter as tk

window = tk.Tk()
window.title("almdrasa weather app")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

textarealabel = tk.Label(window, text="Location:")
textarealabel.grid( column=0 , row=0 , sticky="e" , padx=10 , pady=10)

textareaentry= tk.Entry(window)
textareaentry.grid(column=1, row=0, padx=10 , pady=10 , sticky="e")

searchbtt = tk.Button(window , text= "search")
searchbtt.grid(column=2,row=0 , padx=10, pady=10 , sticky="nsew" )


window.mainloop()