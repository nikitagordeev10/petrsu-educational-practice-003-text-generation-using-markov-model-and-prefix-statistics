# Импортируем необходимые библиотеки
import string
import random
import language_tool_python
import time

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

# Основная функция программы
def main():
    # Пути к файлам с исходным и результативным текстом
    source_filepath = "source.txt"
    answer_filepath = "answer.txt"

    # Настройки для генерации текста
    prefix_length = 1
    initial_prefix = "my"
    text_length = 1000

    # Загружаем текст из файла
    corpus = load_text_from_file(source_filepath)
    # Предварительно обрабатываем текст
    cleaned_text = preprocess_text(corpus)

    # Строим статистику по префиксам
    prefix_stats = build_prefix_stats(cleaned_text, prefix_length)
    # Приводим начальный префикс к нижнему регистру
    initial_prefix = initial_prefix.lower()
    # Генерируем текст на основе полученной статистики по префиксам
    generated_text = generate_text(prefix_stats, initial_prefix, text_length)

    # Проверяем генерированный текст на грамматику и стиль
    corrected_text = grammar_and_style_check(generated_text)

    # Записываем результативный текст в файл
    with open(answer_filepath, 'w') as f:
        f.write(corrected_text)

# Запуск программы
if __name__ == "__main__":
    main()