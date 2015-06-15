def main():
    import tkinter as Tk
    from tkinter import messagebox as TkMessageBox
    from tkinter import simpledialog as TkSimpleDialog
    from tkinter import filedialog as TkFileDialog
    from Trie import Trie

    class MainApp():
        def __init__(self, tk_master, trie_file_location="trie.json"):
            self.tk_master = tk_master
            self.tk_master.minsize(width=350, height=250)
            self.trie_file_location = trie_file_location

            self.input_frame = Tk.Frame(self.tk_master)
            self.button_frame = Tk.Frame(self.tk_master)
            self.menu = Tk.Menu(tk_master)
            self.tk_master.config(menu=self.menu)

            self.input_frame.grid(row=0, column=0, sticky="n")
            self.button_frame.grid(row=0, column=1)

            self.menu.add_command(label="Save to file", command=self.save_trie)

            self.autocomplete_field = Tk.Text(self.input_frame, width=20)
            self.autocomplete_field.grid(row=0, column=0)
            self.autocomplete_field.bind("<KeyRelease>", self.autocomplete_last_word)

            self.button = Tk.Button(self.input_frame, text="Add words", command=self.add_word)

            self.trie = Trie.from_JSON_file(trie_file_location)

        def mainloop(self):
            self.tk_master.mainloop()

        def save_trie(self, trie_file_location=None):
            if trie_file_location is None:
                trie_file_location = TkFileDialog.asksaveasfilename()
                if not trie_file_location:
                    return
            self.trie.to_JSON(trie_file_location)
            TkMessageBox.showinfo("Saved", "Saved successfully!")

        def auto_save_trie(self):
            self.trie.to_JSON(self.trie_file_location)

        def add_word(self, new_word=None):
            if new_word is None:
                new_word = self.autocomplete_field.get(1.0)
            if not new_word:
                TkMessageBox.showerror("Error", "word must not be empty")
                return
            if new_word in self.trie:
                TkMessageBox.showerror("Error", "Word already in list")
                return
            assoc_number = len(new_word)
            self.trie.add_word(new_word, assoc_number)
            self.auto_save_trie()
            TkMessageBox.showinfo("Success", "Word added successfully!")

        def create_entry_updater(self, word_suffix):
            def sample_entry_updater(event):
                self.autocomplete_field.insert(Tk.END, word_suffix)
                self.button_frame.grid_forget()
            return sample_entry_updater

        def create_word_adder(self, word, destroy=False):
            def word_adder():
                self.add_word(word)
                if destroy:
                    self.button_frame.grid_forget()
            return word_adder

        def get_last_word(self, event):
            typed = self.autocomplete_field.get(1.0, Tk.END).rstrip()
            if typed:
                word = []
                for k in reversed(typed):
                    if k.isspace():
                        break
                    word.append(k)
                word = "".join(reversed(word))
                return word

        def ask_to_add(self, event):
            last_word = self.get_last_word(event)
            if last_word:
                if last_word not in self.trie:
                    frame = Tk.Frame(self.tk_master)
                    add_button = Tk.Button(frame, text=("Add word: " + last_word),
                                           command=self.create_word_adder(last_word))
                    add_button.grid(sticky="w")

                    self.button_frame = frame
                    self.button_frame.grid(row=0, column=1, sticky="nw")

        def autocomplete_last_word(self, event):
            self.button_frame.grid_forget()
                                                     # backspace
            if event.char.isspace() or event.keycode == 8:  # ask to add new word
                self.ask_to_add(event)
            else:
                word = self.get_last_word(event)
                if not word:
                    return

                prefix_len = len(word)
                words = self.trie.list_words_with_prefix(word)

                if not words:
                    return
                if len(words) == 1:  # Only one word, should we automatically complete it?
                    pass

                frame = Tk.Frame(self.tk_master, height=100)

                for word in sorted(words.keys(), key=len):

                    simulated_button = Tk.Label(frame, text=word)
                    simulated_button.bind("<Button-1>", self.create_entry_updater(word[prefix_len:] + " "))
                    simulated_button.grid(sticky="w")

                self.button_frame = frame
                self.button_frame.grid(row=0, column=1, sticky="nw")

    root = Tk.Tk()

    main_app = MainApp(root)

    main_app.mainloop()  # Blocking call


if __name__ == "__main__":
    main()