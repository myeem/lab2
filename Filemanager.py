import os
import shutil
from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showerror

class FileManager:
    def __init__(self):
        self.window = Tk()#cjplftv jryj
        self.top_frame = Frame(self.window)
        self.bottom_frame = Frame(self.window)
        self.file_list = Listbox(self.top_frame, width=60, height=37) #параметры для левого окна
        self.file_content = Listbox(self.top_frame, width=60, height=35) #параметры для правого
        self.text = StringVar()
        self.label = Label(self.bottom_frame, width=100, textvariable=self.text)
        self.console = Entry(self.bottom_frame, width=100)
        self.commands = {
            "newfile": self.new_file,  # создание нового файла
            "newdir": self.new_dir,  # создание новой папки
            "readfile": self.read_file,  # открыть файл для чтения
            "writeinfile": self.writein_file,  # записать в файл инормацию
            "removefile": self.remove_file,  # удалить файл
            "removedir": self.remove_dir,  # удалить папку
            "copyfile": self.copy_file,  # копирование файла
            "movefile": self.move_file,  # переместить файл
            "renamefile": self.rename_file,  # изменить имя файла
            "changedir": self.change_dir,# изменить папку
        }
        self.path = os.getcwd()
        self.configure_window()

    def configure_window(self):
        self.window.title("Файловый менеджер") # задаем название
        self.window.bind('<Return>', self.get_command) #с помощью bind  связываем событие и действие
        self.top_frame.configure(bg="#c8a2c8") #далее задаем шрифты и цвета
        self.bottom_frame.configure(bg="#DA70D6")
        self.top_frame.pack(fill=BOTH)
        self.bottom_frame.pack(fill=BOTH)
        self.file_list.pack(side=LEFT, padx=10, pady=10)
        self.file_list.configure(font=Font(size=10, weight="bold"), bg="#FFDAB9", fg="#000000",
                                 selectbackground="#FFFFFF", selectforeground="#000000")
        self.file_content.pack(side=RIGHT, padx=10, pady=10)
        self.file_content.configure(font=Font(size=10, weight="bold"), bg="#FFDAB9", fg="#000000",
                                    selectbackground="#FFFFFF", selectforeground="#000000")
        self.label.pack(side=TOP, padx=10)
        self.label.configure(font=Font(size=10, weight="bold"), bg="#FFDAB9", fg="#000000")
        self.console.pack(side=TOP, padx=10, pady=2)
        self.console.configure(font=Font(size=10, weight="bold"), bg="#FFDAB9", fg="#000000")
        self.display_dir_content()
        self.display_path()
        self.window.mainloop() #бесконечный цикл окна, пока оно не будет закрыто пользователем

    def display_dir_content(self):
        self.file_list.delete(0, END) #удалить с нулевой позиции и до конца
        for file in os.listdir(os.getcwd()):
            self.file_list.insert(END, file) #insert-ставляем элемент

    def display_path(self):
        self.text.set(self.path)

    def display_content(self, content):
        self.file_content.delete(0, END)
        for line in content:
            self.file_content.insert(END, line)

    def get_command(self, event):
        line = self.console.get().split(" ")
        self.console.delete(0, END)
        if len(line) > 0:
            command, arguments = line[0], line[1:] #записываем саму команду и аргументы
            if command in self.commands.keys(): #если команда существует
                self.commands[command](*arguments) #вызываем команду и передаем аргументы
            else:
                showerror("ОШИБКА","Такой команды нет")
            self.display_path()

    def new_dir(self, *args):
        if len(args) > 1: #должен быть только один аргумент (имя папки)
            showerror("ОШИБКА","Слишком много аргументов. Попробуйте снова")
        else:
            dirName = args[0]
            try:
                os.mkdir(self.path + os.sep + dirName)
                self.display_dir_content()
            except Exception as e:
                showerror("ОШИБКА", str(e))

    def new_file(self, *args):
        try:
            for file_name in args:
                if ".txt" not in file_name:
                    file_name += ".txt"
                open(file_name, 'a').close()
            self.display_dir_content()
        except Exception as e:
            showerror("ОШИБКА", str(e))

    def remove_dir(self, *args):
        if len(args) > 1:#должен быть только один аргумент (имя папки)
            showerror("ОШИБКА","Слишком много аргументов. Попробуйте снова")
        else:
            dirName = args[0]
            try:
                shutil.rmtree(self.path + os.sep + dirName)
                self.display_dir_content()
            except Exception as e:
                showerror("ОШИБКА", str(e))

    def remove_file(self, *file_names):
        try:
            for file_name in file_names:
                if ".txt" not in file_name:
                    file_name += ".txt"
                os.remove(file_name)

            self.display_dir_content()
        except Exception as e:
            showerror("ОШИБКА", str(e))
    def change_dir(self, *args):
        if len(args) > 1:#должен быть один аргмуент (имя папки)
            showerror("ОШИБКА","Слишком много аргументов. Попробуйте снова")
        else:
            try:
                os.chdir(args[0])
                self.path = os.getcwd()
                self.display_dir_content()
            except Exception as e:
                showerror("ОШИБКА", str(e))

    def writein_file(self, *args):
        if len(args) < 2:# минимум три аргмуента (команда, имя файла, текст)
            showerror("Слишком мало аргументов. Попробуйте снова")
        else:
            try:
                file_name, data = args[0], args[1:]
                if ".txt" not in file_name:
                    file_name += ".txt"
                with open(file_name, 'a') as file:
                    file.write(" ".join(data) + "\n")
                self.display_dir_content()
            except Exception as e:
                showerror("ОШИБКА", str(e))

    def read_file(self, *args):
        if len(args) > 1: #только имя файла
            showerror("Слишком много аргументов. Попробуйте снова")
        else:
            try:
                file_name = args[0]
                if ".txt" not in file_name:
                    file_name += ".txt"
                with open(file_name, 'r') as file:
                    self.display_content(file)
            except Exception as e:
                showerror("ОШИБКА", str(e))

    def copy_file(self, *args):
        file_names = args[:-1]
        dirPath = args[-1]
        try:
            for file_name in file_names:
                if ".txt" not in file_name:
                    file_name += ".txt"
                shutil.copy(file_name, dirPath)

            self.display_dir_content()
        except Exception as e:
            showerror("ОШИБКА", str(e))

    def move_file(self, *args):
        file_names = args[:-1]
        dirPath = args[-1]
        for file_name in file_names:
            if ".txt" not in file_name:
                file_name += ".txt"
            shutil.move(file_name, dirPath)

        self.display_dir_content()

    def rename_file(self, *args):
        if len(args) > 2: #должно быть 2 (имя и новое имя)
            showerror("ОШИБКА","Слишком много аргументов. Попробуйте снова")
        elif len(args) < 2:
            showerror("ОШИБКА","Слишком мало аргументов. Попробуйте снова")
        else:
            file_name = args[0]
            if ".txt" not in file_name:
                file_name += ".txt"
            new_file_name = args[1]
            if ".txt" not in new_file_name:
                new_file_name += ".txt"
            os.rename(file_name, new_file_name)
        self.display_dir_content()

def main():
    FileManager()

if __name__ == '__main__':
    main()
