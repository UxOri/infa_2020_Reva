import tkinter as tk

class SampleApp(tk.Tk):
    '''
    Полускопипастченный класс, который нужен для создания диалогового окна 
    с вопросом.
    '''
    def __init__(self):
        '''
        entry - объект, отвечающий за содержимое строки, написанной игроком
        button - объект, отвечающий за нажатие кнопки "ввести имя"
        ans - переменная, хранящая введённое игроком
        '''
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Ввести имя", width=12, height=1, command=self.on_button)
        self.button.pack()
        self.entry.pack(pady=20)
        self.ans = ''

    def on_button(self):
        '''
        Записывает введённое игроком значение в переменную, когда нажата кнопка
        '''
        self.ans = self.entry.get()
        self.destroy()
        
    def text_out(self):
        '''
        Возвращает написанное игроком (так нагляднее)
        '''
        return self.ans