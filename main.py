from tkinter import *
from library import Library
from database import MongoDBHandler

root = Tk()
root.title("Library Management System")
root.config(padx=100, pady=100)
lib = Library()
mongodb=MongoDBHandler()

titleLabel = Label(root, text="Library Management System")
titleLabel.grid(column=0, row=0, columnspan=2, pady=(0, 10))

## Content
contentFrame = Frame(root)
contentFrame.grid(row=1, column=0, columnspan=2)

text_Box = Text(contentFrame, height=13, width=20, wrap="word")
text_Box.pack(side=LEFT, expand=True)

scrollBar = Scrollbar(contentFrame, command=text_Box.yview)
scrollBar.pack(side=RIGHT, fill=Y)
text_Box.config(yscrollcommand=scrollBar.set,state=NORMAL,cursor="arrow")



# updated opening screen
def data_add_text_box_home():
    print("Ana ekrana veri tabanından veri ekledi")
    data=mongodb.get_all_books_data()
    print(data)
    for book_name in data:
        text_Box.insert('end',book_name['Book Name']+"\n")
    
data_add_text_box_home()


# with open('books.txt', 'r') as file:
#     file.seek(0)
#     updated_content = file.readlines()
#     updated_list = [line.strip().split(',') for line in updated_content]
#     for item in updated_list:
#         text_Box.insert('end', item[0] + "\n")



## Command Buttons
add_book_button = Button(root, text="Add Book", command=lambda: lib.add_books(text_Box))
add_book_button.grid(row=2, column=0, pady=(10, 0), sticky="ew")

read_book_button = Button(root, text="Read Books", command=lib.read_books)
read_book_button.grid(row=3, column=0, pady=(5, 0), sticky="ew")

list_book_button = Button(root, text="List Book",command=lib.list_book)
list_book_button.grid(row=4, column=0, pady=(5, 0), sticky="ew")


all_remove_books = Button(root, text="All Books Remove", command=lambda: lib.all_books_remove(text_Box))
all_remove_books.grid(row=6, column=0, pady=(5, 0), sticky="ew")









## MAİN LOOP
root.mainloop()



