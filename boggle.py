import tkinter as tk
import random

class BaseApp():
    def __init__(self, parent):
        self.parent = parent
        self.parent.attributes('-fullscreen', True)

class MainMenu(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        center_x = int((screen_width - 200) / 2)
        center_y = int((screen_height - 150) / 2)
        self.button1 = tk.Button(self.parent, text="Играть", width=35, height=5, font=("Helvetica", 15), command=self.select_time)
        self.button1.place(x=center_x-75, y=center_y-50)
        self.button2 = tk.Button(self.parent, text="Выход", width=35, height=5, font=("Helvetica", 15),  command=self.parent.destroy)
        self.button2.place(x=center_x-75, y=center_y+84)
        self.img = tk.PhotoImage(file="rule.png")
        self.button = tk.Button(self.parent, image=self.img, width=50, height=50, command=self.rule_window)
        self.button.place(relx=0.98, rely=0.04, anchor="center")
        self.nadpic1 = tk.PhotoImage(file="nadpic.png")
        self.nadpic = tk.Label(self.parent, image=self.nadpic1)
        self.nadpic.place(relx=0.5, rely=0.25, anchor="center")
        self.ice_cube1 = tk.PhotoImage(file="ice-cube.png.")
        self.ice_cube = tk.Label(self.parent, image=self.ice_cube1, width=70, height=70)
        self.ice_cube.place(relx=0.5, rely=0.3, anchor="center")
        self.cube1 = tk.PhotoImage(file="cube.png.")
        self.cube = tk.Label(self.parent, image=self.cube1, width=250, height=250)
        self.cube.place(relx=0.2, rely=0.6, anchor="center")
        self.cube2 = tk.PhotoImage(file="cube2.png.")
        self.cube_lbl = tk.Label(self.parent, image=self.cube2, width=250, height=250)
        self.cube_lbl.place(relx=0.8, rely=0.3, anchor="center")

    def rule_window(self):
        rule_window = tk.Toplevel(self.parent)
        rule_window.geometry("720x320")
        rule_window.title("Правила игры Boggle")
        rule_window.attributes('-toolwindow', True)
        rule_window.protocol("WM_DELETE_WINDOW", lambda: None)
        rule_window.resizable(False, False)
        rule_window.grab_set()
        rule_label = tk.Label(rule_window, text="Правила игры Boggle\n\n1. Слова состоят из букв на кубиках\n2. Слова должны иметь длину не менее трех букв\n3. Слова должны состоять только из букв на кубиках, не более одной копии каждой буквы\n4. Слова могут идти только по горизонтали, вертикали или диагонали\n5. Слова не могут повторяться\n6. Игра заканчивается, когда время вышло\n7. Каждое правильно угаданное слово дает очки, которые зависят от его длины", justify="left", font=("Helvetica", 12))
        rule_label.pack(padx=10, pady=10)
        ok_button = tk.Button(rule_window, text="OK", command=lambda: (rule_window.grab_release(), rule_window.destroy()))
        ok_button.pack(pady=10)

    def select_time(self):
        time_window = tk.Toplevel(self.parent)
        time_window.title("Выбор таймера")
        time_window.attributes('-toolwindow', True)
        time_window.resizable(False, False)
        time_window.grab_set()
        window_width = 400
        window_height = 400
        screen_width = time_window.winfo_screenwidth()
        screen_height = time_window.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        time_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        time_label = tk.Label(time_window, text="Выберите желаемый таймер", justify="left", font=("Helvetica", 14))
        time_label.pack(padx=10, pady=10)
        duration_var = tk.StringVar()
        duration_var.set("300")
        duration_frame = tk.Frame(time_window)
        duration_frame.pack(pady=10)
        durations = [("30 секунд", "30"), ("1 минута", "60"), ("2 минуты", "120"), ("5 минут", "300"), ("10 минут", "600")]
        for text, duration in durations:
            rb = tk.Radiobutton(duration_frame, text=text, variable=duration_var, value=duration, font=("Helvetica", 14))
            rb.pack(anchor=tk.W)
        input_button = tk.Button(time_window, text="Выбрать", command=lambda: (time_window.grab_release(), time_window.destroy(), self.play_game(duration_var.get())), font=("Helvetica", 14))
        input_button.pack(pady=10)
        close_button = tk.Button(time_window, text="Закрыть", command=lambda: (time_window.grab_release(), time_window.destroy()), font=("Helvetica", 14))
        close_button.pack(pady=10)
        time_window.mainloop()

    def play_game(self, duration):
        WordFinderApp(self.parent, duration=duration)
        self.button1.place_forget()
        self.button2.place_forget()

class WordFinderApp(BaseApp):
    def __init__(self, parent, size=4, width=None, height=None, duration=300):
        super().__init__(parent)
        self.size = size
        self.width = width if width is not None else self.parent.winfo_screenwidth()
        self.height = height if height is not None else self.parent.winfo_screenheight()
        self.canvas_width = self.width // 4
        self.canvas_height = self.height // 2
        self.dictionary = self.load_dictionary()
        self.grid = self.generate_grid()
        self.found_words = set()
        self.list_vse_words = set()
        self.end_window = None
        self.selected_word = ''
        self.grid_letters = tk.StringVar()
        self.grid_letters.set("Начать")
        self.grid_label = tk.Label(self.parent, textvariable=self.grid_letters, font=("Courier", 30))
        self.grid_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        self.input_frame = tk.Frame(parent)
        self.input_frame.place(relx=0.5, rely=0.74, anchor=tk.CENTER)
        self.input_label = tk.Label(self.input_frame, text="Введите слово:", font=("Helvetica", 14))
        self.input_label.pack(side=tk.LEFT)
        self.input_entry = tk.Entry(self.input_frame, font=("Helvetica", 16))
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_button = tk.Button(self.parent, text="Ввод", font=("Helvetica", 16), command=self.add_word)
        self.input_button.place(relx=0.65, rely=0.74, anchor=tk.CENTER)
        self.hint_button = tk.Button(self.parent, text="Подсказка", font=("Helvetica", 16), command=self.update_podskazka_words)
        self.hint_button.place(relx=0.32, rely=0.35, anchor=tk.CENTER)
        self.podskazka_words_listbox = tk.Listbox(self.parent, height=15, font=("Courier", 12))
        self.podskazka_words_listbox.place(relx=0.35, rely=0.54, anchor=tk.CENTER)
        self.new_grid_button = tk.Button(self.parent, text="Перемешать сетку", font=("Helvetica", 16), command=self.generate_grid_and_update)
        self.new_grid_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        self.words_listbox = tk.Listbox(self.parent, height=15, font=("Courier", 12))
        self.words_listbox.place(relx=0.65, rely=0.54, anchor=tk.CENTER)
        self.img2 = tk.PhotoImage(file="back2.png")
        self.button_back = tk.Button(self.parent, image=self.img2, width=50, height=50, command=self.back_to_menu)
        self.button_back.place(relx=0.02, rely=0.04, anchor="center")
        self.grid_buttons = []
        for i in range(4):
            row = []
            for j in range(4):
                button = tk.Button(self.parent, text='', font=("Courier", 30), width=2, height=1)
                button.grid(row=i, column=j, padx=5, pady=5)
                button.bind('<Button-1>', self.on_button_press)
                row.append(button)
            self.grid_buttons.append(row)

        for i in range(4):
            for j in range(4):
                self.grid_buttons[i][j].place(relx=0.5-0.075+j*0.04, rely=0.5-0.125+i*0.08)
        self.duration = duration
        self.timer = self.duration
        self.timer_id = None
        self.timer_label = tk.Label(self.parent, text=f"Таймер: {self.timer} сек.", font=("Courier", 20))
        self.timer_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.start_timer()
        self.generate_grid_and_update()
        self.vse_words()
        self.selected_buttons = []
        self.highlighted = []

    def on_button_press(self, event):
        button = event.widget
        letter = button['text']
        if len(self.selected_buttons) == 1 and button == self.selected_buttons[0]:
            button.config(bg='SystemButtonFace')
            self.selected_buttons.pop()
            self.input_entry.delete(0, tk.END)
        elif not self.selected_buttons:
            button.config(bg='light green')
            self.selected_buttons.append(button)
            self.input_entry.insert(tk.END, letter)
        else:
            if button in self.selected_buttons:
                if len(self.selected_buttons) > 1 and button == self.selected_buttons[-1]:
                    self.input_entry.delete(len(self.selected_buttons) - 1, tk.END)
                    button.config(bg='SystemButtonFace')
                    self.selected_buttons.pop()
            else:
                last_button = self.selected_buttons[-1]
                last_button_row, last_button_col = self.get_button_position(last_button)
                button_row, button_col = self.get_button_position(button)
                if self.is_adjacent(last_button_row, last_button_col, button_row, button_col):
                    button.config(bg='light green')
                    self.selected_buttons.append(button)
                    self.input_entry.insert(tk.END, letter)
                else:
                    self.clear_selected_buttons()


    def get_button_position(self, button):
        for i in range(4):
            for j in range(4):
                if self.grid_buttons[i][j] == button:
                    return i, j

    def is_adjacent(self, row1, col1, row2, col2):
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1

    def clear_selected_buttons(self):
        for button in self.selected_buttons:
            button.config(bg='SystemButtonFace')
        self.selected_buttons = []
        self.input_entry.delete(0, tk.END)

    def load_dictionary(self):
        with open('dictionary.txt', encoding='utf-8') as f:
            dictionary = set(word.strip().upper() for word in f)
        return dictionary

    def generate_grid(self):
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        words = []
        while len(words) < 3:
            grid = [[random.choice(alphabet) for _ in range(4)] for _ in range(4)]
            words = [word for word in self.dictionary if self.can_form_word(word, grid)]
        return grid


    def can_form_word(self, word, grid):
        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]

        def dfs(row, col, index):
            if index == len(word):
                return True
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False
            if visited[row][col]:
                return False
            if grid[row][col] != word[index]:
                return False
            visited[row][col] = True
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if dfs(row+i, col+j, index+1):
                        return True
            visited[row][col] = False
            return False

        for row in range(rows):
            for col in range(cols):
                if dfs(row, col, 0):
                    return True
        return False

    def update_podskazka_words(self):
        self.found_words = set()
        for word in self.dictionary:
            if self.can_form_word(word, self.grid):
                self.found_words.add(word)

        if self.hint_button['state'] == tk.NORMAL:
            self.podskazka_words_listbox.delete(0, tk.END)
            for word in sorted(self.found_words):
                self.podskazka_words_listbox.insert(tk.END, word)

    def generate_grid_and_update(self):
        self.grid = self.generate_grid()
        self.grid_letters.set('')
        for i in range(4):
            for j in range(4):
                letter = self.grid[i][j]
                button = self.grid_buttons[i][j]
                button.config(text=letter)
                button.config(state=tk.NORMAL)
        self.podskazka_words_listbox.delete(0, tk.END)
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()


    def add_word(self):
        word = self.input_entry.get().strip().upper()
        if word and self.can_form_word(word, self.grid) and word in self.dictionary:
            for i in range(self.words_listbox.size()):
                if word == self.words_listbox.get(i).split()[0]:
                    break
            else:
                self.input_entry.delete(0, tk.END)
                self.words_listbox.insert(tk.END, word)
                self.clear_selected_buttons()
            if len(self.list_vse_words) == len(self.words_listbox.get(0, tk.END)):
                self.generate_grid_and_update()

    def vse_words(self):
        self.list_vse_words = set()
        for word in self.dictionary:
            if self.can_form_word(word, self.grid):
                self.list_vse_words.add(word)

    def restart_game(self):
        self.timer = self.duration
        self.input_entry.delete(0, tk.END)
        self.words_listbox.delete(0, tk.END)
        self.podskazka_words_listbox.delete(0, tk.END)
        self.generate_grid_and_update()
        self.start_timer()

    def start_timer(self):
        if self.timer_id is None:
            self.timer_id = self.parent.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_id is not None:
            self.parent.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer(self):
        self.timer = int(self.timer) - 1
        self.timer_label.configure(text=f"Таймер: {self.timer} сек.")
        if self.timer <= 0:
            self.stop_timer()
            self.show_end_window()

        if self.timer_id is not None:
            self.timer_id = self.parent.after(1000, self.update_timer)

    def show_end_window(self):
        end_window = tk.Toplevel(self.parent)
        end_window.title("Игра окончена")
        end_window.attributes('-toolwindow', True)
        end_window.protocol("WM_DELETE_WINDOW", lambda: None)
        end_window.resizable(False, False)
        end_label = tk.Label(end_window, text="Время вышло! Твои результаты:", font=("Courier", 24))
        end_label.pack(padx=20, pady=20)
        found_label = tk.Label(end_window, text="Найденные слова:", font=("Courier", 18))
        found_label.pack(padx=20, pady=10)
        count_words_listbox = tk.Listbox(end_window, height=10, font=("Courier", 12))
        count_words_listbox.pack(padx=20, pady=10)
        words = [word.strip() for word in self.words_listbox.get(0, tk.END)]
        total_score = 0
        word_count = {}
        for word in words:
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
        for word, count in sorted(word_count.items()):
            count_words_listbox.insert(tk.END, f"{word}")
        for word in word_count.items():
            if len(word) == 3 or len(word) == 4:
                total_score += 1
            elif len(word) == 5:
                total_score += 2
            elif len(word) == 6:
                total_score += 3
            elif len(word) == 2:
                total_score += 5
        score_label = tk.Label(end_window, text=f"Всего очков: {total_score}", font=("Courier", 18))
        score_label.pack(padx=20, pady=10)
        button_frame = tk.Frame(end_window)
        button_frame.pack(padx=20, pady=20)
        quit_button = tk.Button(button_frame, text="Выйти в главное меню", command=lambda: (end_window.destroy(), self.back_to_menu()))
        quit_button.pack(side=tk.LEFT, padx=10)
        restart_button = tk.Button(button_frame, text="Начать заново", command=lambda: (end_window.destroy(), self.restart_game()))
        restart_button.pack(side=tk.LEFT, padx=20)
        end_window.grab_set()

    def back_to_menu(self):
        MainMenu(self.parent)
        self.grid_label.destroy()
        self.input_frame.destroy()
        self.input_button.destroy()
        self.button_back.destroy()
        for i in range(4):
            for j in range(4):
                self.grid_buttons[i][j].destroy()
        self.hint_button.destroy()
        self.podskazka_words_listbox.destroy()
        self.new_grid_button.destroy()
        self.words_listbox.destroy()
        self.timer_label.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

