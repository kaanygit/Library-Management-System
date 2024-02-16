from tkinter import *
from tkinter import messagebox


class Library:
    def __init__(self):
        self.file = open('books.txt', 'a+')

    def read_books(self):
        self.file.seek(0)
        books_lines = self.file.readlines()
        books_list=[line.strip().split(",") for line in books_lines]
        print(books_list)
        # for book in books_list:
        #     print(book)

    def add_books(self, text_box):
        new = Toplevel()
        new.geometry("400x400")
        new.title("Add Book")

        # Book Name
        label_book_name = Label(new, text="Book Name:")
        entry_book_name = Entry(new, width=30)
        label_book_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_book_name.grid(row=0, column=1, padx=10, pady=5)

        # Book Author
        label_book_author = Label(new, text="Book Author:")
        entry_book_author = Entry(new, width=30)
        label_book_author.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_book_author.grid(row=1, column=1, padx=10, pady=5)

        # Release Year
        label_release_year = Label(new, text="Release Year:")
        entry_release_year = Entry(new, width=30)
        label_release_year.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_release_year.grid(row=2, column=1, padx=10, pady=5)

        # Number of Pages
        label_num_pages = Label(new, text="Number of Pages:")
        entry_num_pages = Entry(new, width=30)
        label_num_pages.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_num_pages.grid(row=3, column=1, padx=10, pady=5)
        
        #Book information
        label_information=Label(new,text="Book İnformation : ")
        entry_information=Text(new,width=30,height=10)
        label_information.grid(row=4,column=0,padx=10,pady=10,sticky="e")
        entry_information.grid(row=4,column=1,padx=10,pady=5)

        def button_write_text():
            book_name_content = entry_book_name.get()
            book_author_content=entry_book_author.get()
            book_release_content=entry_release_year.get()
            book_number_page_content=entry_num_pages.get()
            book_information_content = entry_information.get("1.0", "end-1c")
            
            # if kontrolu olacak içleri boşsa tekrar yazacaklar
            if not all([book_name_content, book_author_content, book_release_content, book_number_page_content, book_information_content]):
                messagebox.showwarning("Warning", "Please fill in all the fields.")
                return
            else:
                self.file.write(
                    f"{book_name_content}, {book_author_content}, {book_release_content}, {book_number_page_content}, {book_information_content}\n"
                )
                print("Yazı yazıldı")

                ## update textbox
                self.file.seek(0)
                updated_content = self.file.readlines()
                updated_list = [line.strip().split(",") for line in updated_content]
                text_box.delete(1.0, END)  # Delete existing content
                for item in updated_list:
                    text_box.insert('end',item[0]+"\n")
                    
                new.destroy()

        send_write_text_button = Button(new, text="Write", command=button_write_text)
        send_write_text_button.grid(row=5, columnspan=2, pady=10)


    def list_book(self):
        new_window = Toplevel()
        new_window.geometry("750x400")
        new_window.title("List Books")
        labels = ["Name", "Author", "Year", "Pages"]
        for i, label_text in enumerate(labels, start=1):
            label = Label(new_window, text=label_text)
            label.grid(column=i, row=0)

        self.file.seek(0)
        books_lines = self.file.readlines()
        books_list = [line.strip().split(",") for line in books_lines]

        for index in range(4):  # Iterate over columns
            content_frame = Frame(new_window)
            content_frame.grid(row=1, column=index + 1)
            text_box = Text(content_frame, height=20, width=20, wrap="word")
            text_box.pack(side=LEFT, expand=True)
            scroll_bar = Scrollbar(content_frame, command=text_box.yview)
            scroll_bar.pack(side=RIGHT, fill=Y)
            text_box.config(yscrollcommand=scroll_bar.set)
            # for item in books_list:
            #     text_box.insert('end', item[index] + "\n")
            
            
            def on_click_details(event,i):
                print(i) 
                self.show_details(index_number=i)   
                
            for item_index, item in enumerate(books_list):
                text_box.insert('end', item[index] + "\n")
                # Add a binding to call on_textbox_click when the text box is clicked
                text_box.tag_configure(f"tag{item_index}", foreground="blue", underline=True)
                text_box.tag_bind(f"tag{item_index}", "<Button-1>", lambda event, i=item_index: on_click_details(event, i))
                text_box.tag_add(f"tag{item_index}", f"{item_index + 1}.0", f"{item_index + 1}.end")
         
  
            
    def remove_book(index,index_number):
        # Seçili kitabı silme
        print(f"Remove Edilecek index {index_number} remove ediliyor onaylıyor musunuz ?")
        ## Acılır pencere yapımı emin misin

    
    def update_book(self,index_number):
        print(f"Update Edilecek index {index_number}")
        ## eski sürümle kontrol ve değişiklik istiyomusunuz onay mesajı

    def all_books_remove(self, text_box):
        # Tüm Kitapları Silme
        with open('books.txt', 'w') as file:
            text_box.delete(1.0, END)
            print("Tüm Kitaplar silindi.")
    
    def updated_text_box(self):
        updated_content = self.file.readlines()
        updated_list = [line.strip().split(",") for line in updated_content]
        return "\n".join(item[0] for item in updated_list)
    
    def get_content(self, index):
        with open('books.txt', 'r') as file:
            file.seek(0)
            get_content = file.readlines()
            get_list = [line.strip().split(',') for line in get_content]
            for item in get_list:
                print(item[index])
                
    def show_details(index):
        details_window=Toplevel()
        details_window.geometry("400x400")
        details_window.title("Book Details")
        
        with open("books.txt","r") as file:
            file.seek(0)
            books_content=file.readlines()
            books_list=[line.strip().split(",") for line in books_content]
            book_details=books_list[index]
            labels = ["Book Name", "Author", "Release Year", "Number of Pages", "Information"]
            for i, label_text in enumerate(labels):
                label = Label(details_window, text=label_text)
                label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

                entry = Entry(details_window, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, book_details[i])

            close_button = Button(details_window, text="Close", command=details_window.destroy)
            close_button.grid(row=len(labels), columnspan=2, pady=10)
            
    def show_details(self,index_number):
        details_window=Toplevel()
        details_window.geometry("400x400")
        details_window.title("Book Details")
        
        with open("books.txt","r") as file:
            file.seek(0)
            books_content=file.readlines()
            books_list=[line.strip().split(",") for line in books_content]
            book_details=books_list[index_number]
            labels = ["Book Name", "Author", "Release Year", "Number of Pages"]
            for i, label_text in enumerate(labels):
                label = Label(details_window, text=label_text)
                label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

                entry = Entry(details_window, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0,book_details[i])
                
            labels=Label(details_window,text="Information")
            labels.grid(row=4,column=0,padx=10, pady=5, sticky="e")
            entry_information=Text(details_window,width=30,height=10)
            entry_information.grid(row=4,column=1 ,padx=10, pady=5)
            entry_information.insert('1.0',book_details[3])

            update_book_button=Button(details_window,text="Update Book",command=lambda:self.update_book(index_number=index_number))
            update_book_button.grid(row=5, columnspan=2,pady=10)
            remove_book_button = Button(details_window, text="Remove Book", command=lambda:self.remove_book(index_number=index_number))
            remove_book_button.grid(row=6 ,columnspan=2, pady=10)

    





















