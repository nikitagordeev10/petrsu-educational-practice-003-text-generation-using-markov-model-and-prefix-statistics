# Импортируем необходимые библиотеки
import string
import random
import tkinter as tk
from tkinter import ttk
import language_tool_python

# Функция проверки текста на грамматику и стиль
def grammar_and_style_check(text):
    # Создаем объект класса LanguageTool на английском языке
    tool = language_tool_python.LanguageTool('en-US')
    # Получаем список найденных ошибок и предлагаемых исправлений
    matches = tool.check(text)
    # Исправляем найденные ошибки в тексте
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

# Загрузка текста из файла
def load_text_from_file(filepath):
    with open(filepath) as f:
        corpus = f.read()
    return corpus

# Предварительная обработка текста
def preprocess_text(text):
    # Приводим текст к нижнему регистру
    cleaned_text = text.lower()
    # Удаляем всю пунктуацию из текста
    cleaned_text = cleaned_text.translate(str.maketrans("", "", string.punctuation))
    # Заменяем символ новой строки на пробел
    cleaned_text = cleaned_text.replace("\n", " ")
    # Удаляем лишние пробелы, объединяя слова в тексте
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text

# Построение статистики по префиксам
def build_prefix_stats(text, prefix_length):
    prefix_stats = {}
    words = text.split()

    # Проходим по всем словам в тексте
    for i in range(len(words) - prefix_length):
        prefix = tuple(words[i : i + prefix_length])
        suffix = words[i + prefix_length]
        # Заполняем словарь статистикой по префиксам и соответствующим им суффиксам
        prefix_stats.setdefault(prefix, []).append(suffix)

    return prefix_stats

# Генерация текста на основе статистики по префиксам
def generate_text(prefix_stats, initial_prefix, length):
    current_prefix = tuple(initial_prefix.split())
    generated_text = list(current_prefix)

    # Генерируем текст, пока не достигнем заданной длины или не будет найдена последовательность без соответствующих суффиксов
    while len(generated_text) < length:
        if current_prefix not in prefix_stats or not prefix_stats[current_prefix]:
            break

        next_word = random.choice(prefix_stats[current_prefix])
        generated_text.append(next_word)
        current_prefix = tuple(generated_text[-len(current_prefix) :])

    return " ".join(generated_text)

# Функция для создания графического интерфейса пользователя.
def create_gui():
    # Создаем основное окно приложения.
    root = tk.Tk()

    # Создаем фрейм для настройки параметров генерации.
    parameters_frame = tk.Frame(root)
    parameters_frame.pack(side=tk.LEFT)

    # Создаем метки для отображения текущих значений параметров.
    prefix_length_label = tk.Label(parameters_frame, text=f"Prefix Length: {prefix_length}")
    prefix_length_label.pack()

    initial_prefix_label = tk.Label(parameters_frame, text=f"Initial Prefix: {initial_prefix}")
    initial_prefix_label.pack()

    text_length_label = tk.Label(parameters_frame, text=f"Text Length: {text_length}")
    text_length_label.pack()

    source_filepath_label = tk.Label(parameters_frame, text=f"Source File: {source_filepath}")
    source_filepath_label.pack()

    # Создаем кнопку для запуска генерации текста.
    generate_button = tk.Button(parameters_frame, text="Generate")
    generate_button.pack(pady=10)

    # Создаем текстовое поле для отображения сгенерированного текста.
    answer_text = tk.Text(root, wrap="word", font=("Consolas", 10))
    answer_text.pack(expand=True, fill="both")

    # Добавляем вертикальный скроллбар для текстового поля.
    scrollbar = tk.Scrollbar(root, command=answer_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    answer_text.config(yscrollcommand=scrollbar.set)

    # Создаем виджеты для задания параметров генерации текста и добавляем команду для кнопки генерации.
    create_widgets(parameters_frame, answer_text, prefix_length_label, initial_prefix_label, text_length_label, source_filepath_label, generate_button)

    # Запускаем главный цикл обработки событий.
    root.mainloop()

# Функция для создания виджетов пользовательского интерфейса, которые будут использоваться для генерации текста
def create_widgets(parameters_frame, answer_text, prefix_length_label, initial_prefix_label, text_length_label, source_filepath_label, generate_button):
    
    # Обновление параметров генерации текста на основе значений, введенных пользователем в поля.
    def update_parameters():
        global prefix_length, initial_prefix, text_length, source_filepath

        # Получаем текущие значения параметров из соответствующих полей.
        prefix_length = int(prefix_length_entry.get())
        initial_prefix = initial_prefix_entry.get()
        text_length = int(text_length_entry.get())
        source_filepath = source_filepath_entry.get()

        # Обновляем соответствующие метки, отображающие значения параметров.
        prefix_length_label.config(text=f"Prefix Length: {prefix_length}")
        initial_prefix_label.config(text=f"Initial Prefix: {initial_prefix}")
        text_length_label.config(text=f"Text Length: {text_length}")
        source_filepath_label.config(text=f"Source File: {source_filepath}")
    
    # Функция для генерации и сохранения текста на основе параметров.
    def generate_and_save_text():
        # Загружаем текст из файла
        corpus = load_text_from_file(source_filepath)

        # Предварительно обрабатываем текст
        cleaned_text = preprocess_text(corpus)

        # Строим статистику по префиксам
        prefix_stats = build_prefix_stats(cleaned_text, prefix_length)

        # Приводим начальный префикс к нижнему регистру
        initial_prefix_lc = initial_prefix.lower()

        # Генерируем текст на основе полученной статистики по префиксам
        generated_text = generate_text(prefix_stats, initial_prefix_lc, text_length)        

        # Проверяем генерированный текст на грамматику и стиль
        corrected_text = grammar_and_style_check(generated_text)

        # Записываем результативный текст в файл
        with open(answer_filepath, 'w') as f:
            f.write(corrected_text)

        # Отображаем сгенерированный и откорректированный текст в соответствующем поле 
        answer_text.delete("1.0", tk.END)
        answer_text.insert("1.0", corrected_text)

    # Создаем поля ввода для задания параметров генерации текста
    prefix_length_entry = tk.Entry(parameters_frame, width=5)
    prefix_length_entry.insert(tk.END, str(prefix_length))
    prefix_length_entry.pack(anchor=tk.W, padx=5, pady=5)
    prefix_length_entry.bind("<FocusOut>", lambda event: update_parameters())

    initial_prefix_entry = tk.Entry(parameters_frame, width=20)
    initial_prefix_entry.insert(tk.END, initial_prefix)
    initial_prefix_entry.pack(anchor=tk.W, padx=5, pady=5)
    initial_prefix_entry.bind("<FocusOut>", lambda event: update_parameters())

    text_length_entry = tk.Entry(parameters_frame, width=5)
    text_length_entry.insert(tk.END, str(text_length))
    text_length_entry.pack(anchor=tk.W, padx=5, pady=5)
    text_length_entry.bind("<FocusOut>", lambda event: update_parameters())

    source_filepath_entry = tk.Entry(parameters_frame, width=20)
    source_filepath_entry.insert(tk.END, source_filepath)
    source_filepath_entry.pack(anchor=tk.W, padx=5, pady=5)
    source_filepath_entry.bind("<FocusOut>", lambda event: update_parameters())

    # Добавляем команду для кнопки генерации текста
    generate_button.config(command=generate_and_save_text)

# Пути к файлам с исходным и результативным текстом
source_filepath = "source.txt"
answer_filepath = "answer.txt"

# Настройки для генерации текста
prefix_length = 1
initial_prefix = "because"
text_length = 1000

# Запуск программы
if __name__ == "__main__":
    create_gui()