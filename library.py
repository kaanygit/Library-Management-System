from tkinter import *
from tkinter import messagebox
from database import MongoDBHandler




class Library:
    def __init__(self):
        self.file = open('books.txt', 'a+')
        self.read_file = open('books.txt', 'r')
        self.list_book_window = None
        self.scroll_bar = Scrollbar()
        self.mongo_handler = MongoDBHandler()
    
    
    def read_books(self):
        # self.file.seek(0)
        # books_lines = self.file.readlines()
        # books_list = [line.strip().split(",") for line in books_lines]
        # print(books_list)
        
        self.mongo_handler.get_all_books_data()

    def add_books(self, text_box):
        new = Toplevel()
        new.geometry("400x400")
        new.title("Add Book")

        label_book_name = Label(new, text="Book Name:")
        entry_book_name = Entry(new, width=30)
        label_book_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_book_name.grid(row=0, column=1, padx=10, pady=5)

        label_book_author = Label(new, text="Book Author:")
        entry_book_author = Entry(new, width=30)
        label_book_author.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_book_author.grid(row=1, column=1, padx=10, pady=5)

        label_release_year = Label(new, text="Release Year:")
        entry_release_year = Entry(new, width=30)
        label_release_year.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_release_year.grid(row=2, column=1, padx=10, pady=5)

        label_num_pages = Label(new, text="Number of Pages:")
        entry_num_pages = Entry(new, width=30)
        label_num_pages.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_num_pages.grid(row=3, column=1, padx=10, pady=5)

        label_information = Label(new, text="Book Information:")
        entry_information = Text(new, width=30, height=10)
        label_information.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_information.grid(row=4, column=1, padx=10, pady=5)

        def button_write_text():
            book_name_content = entry_book_name.get()
            book_author_content = entry_book_author.get()
            book_release_content = entry_release_year.get()
            book_number_page_content = entry_num_pages.get()
            book_information_content = entry_information.get("1.0", "end-1c")

            if not all([book_name_content, book_author_content, book_release_content, book_number_page_content, book_information_content]):
                messagebox.showwarning("Warning", "Please fill in all the fields.")
                return
            else:
                self.read_file.seek(0)
                books_lines = self.read_file.readlines()
                books_list = [line.strip().split(",") for line in books_lines]

                if any(book[0].strip() == book_name_content and book[1].strip() == book_author_content for book in books_list):
                    messagebox.showwarning("Warning", "Book already exists.")
                    return
                else:
                    if len(book_information_content) > 50:
                        messagebox.showwarning("Warning", "Information cannot exceed 50 characters.")
                        return
                    
                    ##MongoDB Add Book
                    new_book = {
                        "Book Name": book_name_content,
                        "Author": book_author_content,
                        "Release Year": book_release_content,
                        "Number of Pages": book_number_page_content,
                        "Information": book_information_content
                    }
                    self.mongo_handler.add_book_database(new_book)
                    
                                       
                    self.file.write(
                        f"{book_name_content}, {book_author_content}, {book_release_content}, {book_number_page_content}, {book_information_content}\n"
                    )
                    print("The book added to database and books.txt")

                    self.file.seek(0)
                    updated_content = self.file.readlines()
                    updated_list = [line.strip().split(",") for line in updated_content]
                    text_box.delete(1.0, END)
                    for item in updated_list:
                        text_box.insert('end', item[0] + "\n")

                    new.destroy()
                    self.list_book()

        send_write_text_button = Button(new, text="Write", command=button_write_text)
        send_write_text_button.grid(row=5, columnspan=2, pady=10)

    def list_book(self):
        if self.list_book_window:
            self.list_book_window.destroy()

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

        for index in range(4):
            content_frame = Frame(new_window)
            content_frame.grid(row=1, column=index + 1)
            text_box = Text(content_frame, height=20, width=20, wrap="word")
            text_box.pack(side=LEFT, expand=True)

            scroll_bar = Scrollbar(content_frame, command=text_box.yview)
            scroll_bar.pack(side=RIGHT, fill=Y)
            text_box.config(yscrollcommand=scroll_bar.set, state=NORMAL, cursor="arrow")

            def on_click_details(event, i):
                print(i)
                self.show_details(index_number=i, list_book_window_old=new_window)

            ## mongodb den gelen data ile değişim
            for item_index, item in enumerate(books_list):
                text_box.insert('end', item[index] + "\n")
                text_box.tag_configure(f"tag{item_index}", foreground="blue", underline=False)
                text_box.tag_bind(f"tag{item_index}", "<Button-1>", lambda event, i=item_index: on_click_details(event, i))
                text_box.tag_add(f"tag{item_index}", f"{item_index + 1}.0", f"{item_index + 1}.end")




    def remove_book(self, index_number, window):
        pop_up_window = Toplevel()
        pop_up_window.title("Remove Book")

        label_message = Label(pop_up_window, text="Are you sure you want to delete it?")
        label_message.grid(row=0, column=0, columnspan=2, pady=10)

        def remove_confirm():
            print("I confirm deletion")
            self.remove_book_from_list(index_number)
            pop_up_window.destroy()
            self.list_book()

        def remove_cancel():
            print("Cancel Deletion")
            pop_up_window.destroy()

        confirm_button = Button(pop_up_window, text="Yes", command=remove_confirm)
        confirm_button.grid(column=0, row=1, padx=5, pady=10)

        cancel_button = Button(pop_up_window, text="No", command=remove_cancel)
        cancel_button.grid(column=1, row=1, padx=5, pady=10)

        pop_up_window.update_idletasks()
        width = pop_up_window.winfo_width()
        height = pop_up_window.winfo_height()
        x = (pop_up_window.winfo_screenwidth() - width) / 2
        y = (pop_up_window.winfo_screenheight() - height) / 2
        pop_up_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    def remove_book_from_list(self, index):
        try:
            with open("books.txt", "r") as file:
                lines = file.readlines()

            del lines[index]

            with open("books.txt", "w") as file:
                file.writelines(lines)                 
                self.mongo_handler.remove_data_index(index)

            messagebox.showinfo("Success", "Selected book has been removed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # def update_book(self, index_number):
    #     print(f"Index to be updated {index_number}")

    def all_books_remove(self, text_box):
        pop_up_window = Toplevel()
        pop_up_window.title("Remove All Book")
        self.mongo_handler.get_all_books_data()
        label_message = Label(pop_up_window, text="Do you confirm deleting all books?")
        label_message.grid(row=0, column=0, columnspan=2, pady=10)

        def remove_all_confirm():
            print("I confirm deletion of all books")
            try:
                with open('books.txt', 'w') as file:
                    text_box.delete(1.0, END)
                    print("All books deleted.")
                    messagebox.showinfo("Success", "All books have been removed.")
                    self.mongo_handler.all_remove_books()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            pop_up_window.destroy()

        def remove_all_cancel():
            print("Cancel Deletion")
            pop_up_window.destroy()

        confirm_button = Button(pop_up_window, text="Yes", command=remove_all_confirm)
        confirm_button.grid(column=0, row=1, padx=5, pady=10)

        cancel_button = Button(pop_up_window, text="No", command=remove_all_cancel)
        cancel_button.grid(column=1, row=1, padx=5, pady=10)

        pop_up_window.update_idletasks()
        width = pop_up_window.winfo_width()
        height = pop_up_window.winfo_height()
        x = (pop_up_window.winfo_screenwidth() - width) / 2
        y = (pop_up_window.winfo_screenheight() - height) / 2
        pop_up_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

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

    def show_details(self, index_number, list_book_window_old):
        list_book_window_old.destroy()
        details_window = Toplevel()
        details_window.geometry("400x400")
        details_window.title("Book Details")

        def open_menu():
            self.list_book()
            details_window.destroy()

        details_window.protocol("WM_DELETE_WINDOW", open_menu)

        with open("books.txt", "r") as file:
            file.seek(0)
            books_content = file.readlines()
            books_list = [line.strip().split(",") for line in books_content]
            book_details = books_list[index_number]
            labels = ["Book Name", "Author", "Release Year", "Number of Pages"]
            for i, label_text in enumerate(labels):
                label = Label(details_window, text=label_text)
                label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

                entry = Entry(details_window, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, book_details[i])

            labels = Label(details_window, text="Information")
            labels.grid(row=4, column=0, padx=10, pady=5, sticky="e")
            entry_information = Text(details_window, width=30, height=10)
            entry_information.grid(row=4, column=1, padx=10, pady=5)
            entry_information.insert('1.0', book_details[3])

            # update_book_button = Button(details_window, text="Update Book", command=lambda: self.update_book(index_number=index_number))
            # update_book_button.grid(row=5, columnspan=2, pady=10)
            remove_book_button = Button(details_window, text="Remove Book", command=lambda: self.remove_book(index_number=index_number, window=details_window))
            remove_book_button.grid(row=6, columnspan=2, pady=10)




