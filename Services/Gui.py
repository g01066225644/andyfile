import os
import tkinter
import tkinter.ttk
from functools import partial

from HelpUtil.Extract import Extract
from HelpUtil.Thread import Thread
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
        else:
            self.notice.configure(text='FAILED', fg='red')

    def no_dir(self, source, check_var):
        if source.get() != "":
            move = Move(check_var.get())
            move.no_directories(source.get())
            self.notice.configure(text='PULL ALL FILES', fg='red')
        else:
            self.notice.configure(text='FAILED', fg='red')

    def delete_new_site(self, source):
        if source.get() != "":
            Delete.new_site_pattern(source.get())
            self.notice.configure(text='Delete new site', fg='red')
        else:
            self.notice.configure(text='FAILED', fg='red')

    def move(self, source, destination, check_var):
        if source.get() != "" and destination.get() != "" and source.get() != destination.get():
            move = Move(check_var.get())
            move.mv(source.get(), destination.get())
            self.notice.configure(text='All files moved', fg='red')
        else:
            self.notice.configure(text='FAILED', fg='red')

    def extract(self, source):
        if source.get() != "":
            for file_name in os.listdir(source.get()):
                if file_name.endswith(('.zip', '.tar.gz', '.rar', '.egg')):
                    ext = Extract()
                    ext.extract(os.path.join(source.get(), file_name))
            self.notice.configure(text='Extract done', fg='red')
        else:
            self.notice.configure(text='FAILED', fg='red')

    def similar_move(self, source, destination, check_var):
        if source.get() != "" and destination.get() != "" and source.get() != destination.get():
            path = source.get()
            move = Move(check_var.get())
            move.similar_mv("\\".join(path.split("\\")[:-1]), destination.get(), path.split("\\")[-1])
            self.notice.configure(text='Similar files moved', fg='red')
        else:
            self.notice.configure(text='FAILED', fg='red')

    def delete_empty_space(self, source):
        if source.get() != "":
            Delete.empty(source.get())
            self.notice.configure(text='DEL Empty Dir', fg='red')
        else:
            self.notice.configure(text='FAILED', fg='red')

    def delete_similar(self, source):
        if source.get() != "":
            path = source.get()
            delete = Delete()
            delete.similar("\\".join(path.split("\\")[:-1]), path.split("\\")[-1])
            self.notice.configure(text='Similar files delete', fg='red')
        else:
            self.notice.configure(text='FAILED', fg='red')

    def update_list(self, event, entry, entry_var, tree, list_frame):

        if event.keysym == 'Return':
            self.enter_key(event, entry, list_frame)
            return
        elif event.keysym in ["Up", "Down"]:
            self.select_UD(event, entry, entry_var, tree, list_frame)
            return

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
                if full_path.startswith(path):
                    tree.insert('', 'end', text=full_path)

    def on_tree_select(self, event, list_frame, entry_widget, entry_var):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], 'text')
            entry_var.set(item_text)
            list_frame.pack_forget()
        event.widget.after(10, lambda: entry_widget.focus())
        event.widget.after(20, lambda: entry_widget.icursor(tkinter.END))

    def find_similar_files(self, entry_path):
        similar_files = set()
        directory = os.path.dirname(entry_path)
        prefix = os.path.basename(entry_path)
        files_in_directory = [f for f in os.listdir(directory) if f.startswith(prefix)]
        similar_files.update(os.path.join(directory, f) for f in files_in_directory)
        return similar_files

    def find_common_prefix(self, similar_files):
        return os.path.commonprefix(list(similar_files)) or None

    def update_entry_and_tree(self, entry_widget, text):
        entry_widget.delete(0, tkinter.END)
        entry_widget.insert(0, text)
        entry_widget.selection_range(len(text), tkinter.END)

    def tab_key(self, event, entry_widget, tree_widget):
        entry_path = entry_widget.get()
        if entry_path == "":
            return
        similar_files = self.find_similar_files(entry_path)

        if similar_files:
            if len(similar_files) == 1:
                selected_file = similar_files.pop()
                self.update_entry_and_tree(entry_widget, selected_file)
            common_prefix = self.find_common_prefix(similar_files)
            if common_prefix:
                self.update_entry_and_tree(entry_widget, common_prefix)

        event.widget.after(10, lambda: entry_widget.focus())
        event.widget.after(20, lambda: entry_widget.icursor(tkinter.END))
        return "break"

    def select_UD(self, event, entry, entry_var, tree, list_frame):
        #수정 더 필요
        first_item = tree.get_children()[0]
        tree.selection_set(first_item)
        tree.focus(first_item)

    def enter_key(self, event, entry_widget, tree_widget):
        tree_widget.pack_forget()
        event.widget.after(10, lambda: entry_widget.focus())
        event.widget.after(20, lambda: entry_widget.icursor(tkinter.END))
        return "break"

    def create(self):
        window = tkinter.Tk()
        window.title("앤디파일")
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
        source.bind('<KeyRelease>',
                    lambda event: self.update_list(event, source, source_var, source_list, source_list_frame))
        source.bind("<Tab>", lambda event: self.tab_key(event, source, source_list))

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
        source_list.bind('<<TreeviewSelect>>',
                         lambda event: self.on_tree_select(event, source_list_frame, source, source_var))

        check_var = tkinter.IntVar()
        check1 = tkinter.Checkbutton(src_path, text="파일 이름 강제 변경", variable=check_var)
        check1.pack(fill="x", expand=True)

        upperdir_button = tkinter.Button(src_path, text="상위 디렉터리 이동",
                                         command=partial(Thread.make_thread, self.upper, source, check_var))
        upperdir_button.pack(side="left", expand=True, pady=10)

        nodir_button = tkinter.Button(src_path, text="모든 디렉터리 삭제",
                                      command=partial(Thread.make_thread, self.no_dir, source, check_var))
        nodir_button.pack(side="left", expand=True, pady=10)

        empty_button = tkinter.Button(src_path, text="빈 디렉터리 삭제",
                                      command=partial(Thread.make_thread, self.delete_empty_space, source))
        empty_button.pack(side="left", expand=True, pady=10)

        del_similar_button = tkinter.Button(src_path, text="비슷한 파일 전부 삭제",
                                            command=partial(Thread.make_thread, self.delete_similar, source))
        del_similar_button.pack(side="left", expand=True, pady=10)

        extract_button = tkinter.Button(src_path, text="압축파일 해제",
                                            command=partial(Thread.make_thread, self.extract, source))
        extract_button.pack(side="left", expand=True, pady=10)

        dest_path_label = tkinter.Label(dest_path, text="Destination Path :")
        dest_path_label.pack(fill='x', expand=True)

        destination_var = tkinter.StringVar()
        destination = tkinter.ttk.Entry(dest_path, textvariable=destination_var)
        destination.pack(fill='x', expand=True)
        destination.bind('<KeyRelease>',
                         lambda event: self.update_list(event, destination, destination_var, destination_list,
                                                        destination_list_frame))
        destination.bind("<Tab>", lambda event: self.tab_key(event, destination, destination_list))

        # Treeview and Scrollbar for Entry 2
        destination_list_frame = tkinter.ttk.Frame(dest_path)
        destination_list_frame.pack(expand=True, fill=tkinter.BOTH)
        destination_list = tkinter.ttk.Treeview(destination_list_frame)
        destination_list.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        destination_yscrollbar = tkinter.ttk.Scrollbar(destination_list_frame, orient="vertical",
                                                       command=destination_list.yview)
        destination_yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        destination_list.configure(yscrollcommand=destination_yscrollbar.set)

        # Initially hide the Treeview and Scrollbar for Entry 2
        destination_list_frame.pack_forget()

        # Bind the selection event of the Treeview for Entry 2
        destination_list.bind('<<TreeviewSelect>>',
                              lambda event: self.on_tree_select(event, destination_list_frame, destination,
                                                                destination_var))

        move_button = tkinter.Button(dest_path, text="모든 파일 이동",
                                     command=partial(Thread.make_thread, self.move, source, destination,
                                                     check_var))
        move_button.pack(side="left", expand=True, pady=10)

        similar_move_button = tkinter.Button(dest_path, text="비슷한 파일 이동",
                                             command=partial(Thread.make_thread, self.similar_move, source, destination,
                                                             check_var))
        similar_move_button.pack(side="left", expand=True, pady=10)

        self.notice = tkinter.Label(window)
        self.notice.pack(side="bottom", expand=True, fill=tkinter.BOTH)

        window.mainloop()
