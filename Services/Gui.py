import os
import tkinter
import tkinter.ttk

from HelpUtil.Move import Move
from HelpUtil.Delete import Delete


class Gui:
    def __init__(self):
        self.notice = None

    def upper(self, source, check_var):
        if source.get() != "":
            move = Move(check_var.get())
            move.upper(source.get())
            self.notice.configure(text='UPPER FILES', fg='red')

    def no_dir(self, source, check_var):
        if source.get() != "":
            move = Move(check_var.get())
            move.no_directories(source.get())
            self.notice.configure(text='PULL ALL FILES', fg='red')

    def delete_new_site(self, source):
        if source.get() != "":
            Delete.new_site_pattern(source.get())
            self.notice.configure(text='Delete new site', fg='red')

    def move(self, source, destination, check_var):
        if source.get() != "" and destination.get() != "" and source.get() != destination.get():
            move = Move(check_var.get())
            move.mv(source.get(), destination.get())
            self.notice.configure(text='All files moved', fg='red')

    def similar_move(self, source, destination, check_var):
        if source.get() != "" and destination.get() != "" and source.get() != destination.get():
            path = source.get()
            move = Move(check_var.get())
            move.similar_mv("\\".join(path.split("\\")[:-1]), destination.get(), path.split("\\")[-1])
            self.notice.configure(text='Similar files moved', fg='red')

    def delete_empty_space(self, source):
        if source.get() != "":
            Delete.empty(source.get())
            self.notice.configure(text='DEL Empty Dir', fg='red')

    def update_list(self, event, entry, entry_var=None, tree=None, list_frame=None):
        path = entry_var.get()

        # Show the Treeview and scrollbar if there is text in the entry
        if path:
            list_frame.pack(after=entry, fill=tkinter.BOTH, expand=True)
        else:
            list_frame.pack_forget()

        # Clear the current list
        for item in tree.get_children():
            tree.delete(item)

        # Get the directory part of the path
        dir_path = os.path.dirname(path)

        if os.path.exists(dir_path):
            # List directories in the current path
            for name in os.listdir(dir_path):
                full_path = os.path.join(dir_path, name)
                if os.path.isdir(full_path) and full_path.startswith(path):
                    tree.insert('', 'end', text=full_path)

    def on_tree_select(self, event, list_frame, entry_var):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], 'text')
            entry_var.set(item_text)
            list_frame.pack_forget()


    def on_tree_select_key(self, event, entry_var, entry_widget):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], 'text')
            entry_var.set(item_text)
            # Move cursor to the end
            entry_widget.icursor(tkinter.END)

    def create(self):
        window = tkinter.Tk()
        window.title("파일 다루기")
        window.geometry("600x300")
        window.resizable(False, False)
        src_path = tkinter.Frame(window)
        src_path.pack(padx=10, pady=10, fill='x', expand=True)
        dest_path = tkinter.Frame(window)
        dest_path.pack(padx=10, pady=10, fill='x', expand=True)

        # path
        src_path_label = tkinter.Label(src_path, text="Source Path : ")
        src_path_label.pack(fill='x', expand=True)

        source_var = tkinter.StringVar()
        source = tkinter.ttk.Entry(src_path, textvariable=source_var)
        source.pack(fill='x', expand=True)
        source.bind('<KeyRelease>', lambda event: self.update_list(event, source, source_var, source_list, source_list_frame))

        source_list_frame = tkinter.ttk.Frame(src_path)
        source_list_frame.pack(expand=True, fill=tkinter.BOTH)
        source_list = tkinter.ttk.Treeview(source_list_frame)
        source_list.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        source_yscrollbar = tkinter.ttk.Scrollbar(source_list_frame, orient="vertical", command=source_list.yview)
        source_yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        source_list.configure(yscrollcommand=source_yscrollbar.set)

        # Initially hide the Treeview and Scrollbar for Entry 1
        source_list_frame.pack_forget()

        # Bind the selection event of the Treeview for Entry 1
        source_list.bind('<<TreeviewSelect>>', lambda event: self.on_tree_select(event, source_list_frame, source_var))
        source_list.bind('<Return>', lambda event: self.on_tree_select_key(event, source_var, source))

        check_var = tkinter.IntVar()
        check1 = tkinter.Checkbutton(src_path, text="파일 이름 강제 변경", variable=check_var)
        check1.pack(fill="x", expand=True)

        nodir_button = tkinter.Button(src_path, text="상위 디렉터리 이동", command=lambda: self.upper(source, check_var))
        nodir_button.pack(side="left", expand=True, pady=10)

        nodir_button = tkinter.Button(src_path, text="모든 디렉터리 삭제", command=lambda: self.no_dir(source, check_var))
        nodir_button.pack(side="left", expand=True, pady=10)

        newsite_button = tkinter.Button(src_path, text="빈 디렉터리 삭제", command=lambda: self.delete_empty_space(source))
        newsite_button.pack(side="left", expand=True, pady=10)

        dest_path_label = tkinter.Label(dest_path, text="Destination Path :")
        dest_path_label.pack(fill='x', expand=True)

        destination_var = tkinter.StringVar()
        destination = tkinter.ttk.Entry(dest_path, textvariable=destination_var)
        destination.pack(fill='x', expand=True)
        destination.bind('<KeyRelease>', lambda event: self.update_list(event, destination, destination_var, destination_list, destination_list_frame))

        # Treeview and Scrollbar for Entry 2
        destination_list_frame = tkinter.ttk.Frame(dest_path)
        destination_list_frame.pack(expand=True, fill=tkinter.BOTH)
        destination_list = tkinter.ttk.Treeview(destination_list_frame)
        destination_list.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        destination_yscrollbar = tkinter.ttk.Scrollbar(destination_list_frame, orient="vertical", command=destination_list.yview)
        destination_yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        destination_list.configure(yscrollcommand=destination_yscrollbar.set)

        # Initially hide the Treeview and Scrollbar for Entry 2
        destination_list_frame.pack_forget()

        # Bind the selection event of the Treeview for Entry 2
        destination_list.bind('<<TreeviewSelect>>', lambda event: self.on_tree_select(event, destination_list_frame, destination_var))
        destination_list.bind('<Return>', lambda event: self.on_tree_select_key(event, destination_var, destination))

        move_button = tkinter.Button(dest_path, text="모든 파일 이동", command=lambda: self.move(source, destination, check_var))
        move_button.pack(side="left", expand=True, pady=10)

        move_button = tkinter.Button(dest_path, text="비슷한 파일 이동", command=lambda: self.similar_move(source, destination, check_var))
        move_button.pack(side="left", expand=True, pady=10)

        self.notice = tkinter.Label(window)
        self.notice.pack(side="bottom", expand=True, fill=tkinter.BOTH)

        window.mainloop()
