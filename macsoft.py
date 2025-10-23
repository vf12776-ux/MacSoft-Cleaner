import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

class MacSoftCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("MacSoft Cleaner")
        self.root.geometry("400x300")
      
        try:
            self.icon = tk.PhotoImage(file='icon38.png')
            self.root.iconphoto(False, self.icon)
            self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon)
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")
        
        # Кнопки без кастомных цветов
        tk.Button(root, text="Сканировать мусор", command=self.scan_junk, width=20).pack(pady=5)
        tk.Button(root, text="Очистить мусор", command=self.clean_junk, width=20).pack(pady=5)
        tk.Button(root, text="Удалить файл/папку", command=self.delete_item, width=20).pack(pady=5)
        tk.Button(root, text="Выход", command=root.quit, width=20).pack(pady=5)

        self.status = tk.Label(root, text="Готов к работе")
        self.status.pack(pady=10)

    def scan_junk(self):
        self.status.config(text="Сканирую...")
        junk_size = 0
        junk_dirs = [os.path.expanduser("~/Downloads"), os.path.expanduser("~/Desktop"), os.path.expanduser("~/Library/Caches")]
        for directory in junk_dirs:
            if os.path.exists(directory):
                for dirpath, _, filenames in os.walk(directory):
                    for file in filenames:
                        try:
                            junk_size += os.path.getsize(os.path.join(dirpath, file))
                        except:
                            pass
        size_mb = junk_size / (1024 * 1024)
        self.status.config(text=f"Найдено мусора: ~{size_mb:.2f} MB")

    def clean_junk(self):
        if messagebox.askyesno("Подтверждение", "Удалить весь мусор? Это необратимо!"):
            self.status.config(text="Очищаю...")
            junk_dirs = [os.path.expanduser("~/Downloads"), os.path.expanduser("~/Desktop"), os.path.expanduser("~/Library/Caches")]
            deleted = 0
            for directory in junk_dirs:
                if os.path.exists(directory):
                    for item in os.listdir(directory):
                        path = os.path.join(directory, item)
                        try:
                            if os.path.isfile(path):
                                os.remove(path)
                                deleted += 1
                            elif os.path.isdir(path):
                                shutil.rmtree(path)
                                deleted += 1
                        except Exception as e:
                            self.status.config(text=f"Ошибка: {e}")
            self.status.config(text=f"Удалено {deleted} элементов")

    def delete_item(self):
        path = filedialog.askdirectory() or filedialog.askopenfilename()
        if path and os.path.exists(path):
            if messagebox.askyesno("Подтверждение", f"Удалить {path}?"):
                self.status.config(text=f"Удаляю {path}...")
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                    self.status.config(text=f"Удалено: {path}")
                except Exception as e:
                    self.status.config(text=f"Ошибка: {e}")
        else:
            self.status.config(text="Путь не выбран")

if __name__ == "__main__":
    root = tk.Tk()
    app = MacSoftCleaner(root)
    root.mainloop()