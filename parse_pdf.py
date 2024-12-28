import fitz  # PyMuPDF для работы с PDF файлами
import re  # Регулярные выражения для поиска шаблонов в тексте
from datetime import datetime, timedelta  # Работа с датами и временем

# Функция для извлечения текста из PDF файла
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)  # Открываем PDF файл
    text = ""
    for page_num in range(len(document)):  # Проходим по всем страницам документа
        page = document.load_page(page_num)  # Загружаем страницу
        text += page.get_text()  # Извлекаем текст со страницы
    return text  # Возвращаем весь текст

# Функция для поиска секции текста между двумя шаблонами
def find_section(text, start_pattern, end_pattern):
    pattern = re.compile(rf'({start_pattern}.*?){end_pattern}', re.DOTALL)  # Компилируем регулярное выражение
    match = pattern.search(text)  # Ищем совпадение в тексте
    if match:
        return match.group(0)  # Возвращаем найденную секцию
    return None  # Если ничего не найдено, возвращаем None

# Функция для поиска дат в секции текста
def find_dates_in_section(section):
    date_pattern = re.compile(r'\b\d{2}\.\d{2}\.\d{4}\b')  # Шаблон для поиска дат в формате DD.MM.YYYY
    dates = date_pattern.findall(section)  # Ищем все даты в секции
    if len(dates) >= 2:
        return dates[:2]  # Возвращаем первые две найденные даты
    return None  # Если найдено меньше двух дат, возвращаем None

# Основная функция для парсинга PDF файла
def parse_pdf(pdf_path):
    start_pattern = '3\\.1'  # Начальный шаблон для поиска секции
    end_pattern = '\\n\\s*\\n'  # Конечный шаблон для поиска секции
    extracted_text = extract_text_from_pdf(pdf_path)  # Извлекаем текст из PDF файла
    section = find_section(extracted_text, start_pattern, end_pattern)  # Ищем секцию текста
    if section:
        dates = find_dates_in_section(section)  # Ищем даты в найденной секции
        if dates:
            return dates  # Возвращаем найденные даты
    return None  # Если ничего не найдено, возвращаем None

# Функция для поиска даты отгрузки в тексте
def find_shipping_date(text):
    pattern = re.compile(r'Дата отгрузки \(сдачи\)\s*\n\s*(\d{2}\s+[А-Яа-я]+\s+\d{4}\s+г\.)')  # Шаблон для поиска даты отгрузки
    match = pattern.search(text)  # Ищем совпадение в тексте
    if match:
        date_str = match.group(1)  # Извлекаем строку с датой
        return convert_date_to_dd_mm_yyyy(date_str)  # Конвертируем дату в формат DD.MM.YYYY
    return None  # Если ничего не найдено, возвращаем None

# Функция для поиска даты подписания в тексте
def find_signed_date(text):
    pattern = re.compile(r'ДОКУМЕНТ ПОДПИСАН\nЭЛЕКТРОННОЙ ПОДПИСЬЮ\nДОКУМЕНТ ПОДПИСАН\nЭЛЕКТРОННОЙ ПОДПИСЬЮ\n\s*(\d{2}\.\d{2}\.\d{4})')  # Шаблон для поиска даты подписания
    match = pattern.search(text)  # Ищем совпадение в тексте
    if match:
        return match.group(1)  # Возвращаем найденную дату
    return None  # Если ничего не найдено, возвращаем None

# Функция для конвертации даты из текстового формата в формат DD.MM.YYYY
def convert_date_to_dd_mm_yyyy(date_str):
    months = {
        "января": "01", "февраля": "02", "марта": "03", "апреля": "04",
        "мая": "05", "июня": "06", "июля": "07", "августа": "08",
        "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"
    }
    parts = date_str.split()  # Разделяем строку на части
    if len(parts) != 4:
        raise ValueError(f"Неправильный формат даты: {date_str}")  # Если формат неверный, выбрасываем исключение
    day, month, year, _ = parts  # Извлекаем день, месяц и год
    return f"{day.zfill(2)}.{months[month]}.{year[:4]}"  # Возвращаем дату в формате DD.MM.YYYY

# Функция для поиска номера статьи 4 в тексте
def find_article_4_number(text):
    section = find_section(text, '4\\.1', '\\n\\s*\\n')  # Ищем секцию текста
    if section:
        section = section.replace('4.1', '', 1)  # Убираем '4.1' один раз из начала
        match = re.search(r'\b(\d+)\b', section)  # Ищем число в секции
        if match:
            return int(match.group(1))  # Преобразуем в число и возвращаем
    return None  # Если ничего не найдено, возвращаем None

# Функция для парсинга дополнительных PDF файлов
def parse_additional_pdfs(additional_pdf_paths):
    all_dates = []
    for path in additional_pdf_paths:
        text = extract_text_from_pdf(path)  # Извлекаем текст из PDF файла
        
        shipping_date = find_shipping_date(text)  # Ищем дату отгрузки
        if shipping_date:
            all_dates.append(shipping_date)  # Добавляем дату в список
        
        signed_date = find_signed_date(text)  # Ищем дату подписания
        if signed_date:
            all_dates.append(signed_date)  # Добавляем дату в список
    
    return all_dates  # Возвращаем все найденные даты

# Функция для добавления рабочих дней к дате
def add_business_days(start_date, num_days):
    current_date = start_date
    while num_days > 0:
        current_date += timedelta(days=1)  # Добавляем один день
        if current_date.weekday() < 5:  # Если это рабочий день (понедельник-пятница)
            num_days -= 1  # Уменьшаем количество оставшихся дней
    return current_date  # Возвращаем конечную дату

# Основная функция для парсинга нескольких PDF файлов
def parse_multiple_pdfs(main_pdf_path, additional_pdf_paths):
    main_dates = parse_pdf(main_pdf_path)  # Парсим основной PDF файл
    additional_dates = parse_additional_pdfs(additional_pdf_paths)  # Парсим дополнительные PDF файлы
    article_4_number = find_article_4_number(extract_text_from_pdf(main_pdf_path))  # Ищем номер статьи 4 в основном PDF файле
    return main_dates, additional_dates, article_4_number  # Возвращаем найденные данные