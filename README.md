# Тестовое задание для младшего аналитика данных

Этот репозиторий содержит решение тестового задания для младшего аналитика данных. Задание разделено на две части: обработка данных и визуализация данных.

## **Часть 1: Обработка данных**

Задача обработки данных заключается в подготовке и обработке исходных данных для использования во второй части задания. Требования к выходным данным указаны в постановке задачи. Реализация этой части находится в файле **`solution1.py`**.

### **Шаги обработки данных:**

1. Загрузить входные данные
2. Оставить требуемые столбцы
3. Присвоить цвета фразам на основе кластеров
4. Удалить дубликаты ключевых слов в одной области
5. Переименовать столбцы, если это необходимо
6. Отсортировать выходные данные
7. Сохранить выходные данные в файл формата CSV или в таблицу Google Sheets

### **Используемые библиотеки:**

- pandas

## **Часть 2: Визуализация данных**

Задача визуализации данных заключается в создании диаграмм рассеяния на основе обработанных данных. Каждая диаграмма рассеяния представляет собой одну область. Реализация этой части находится в файле **`solution2.py`**.

### **Шаги визуализации данных:**

1. Определить функцию для разделения длинных фраз
2. Загрузить выходные данные из Части 1
3. Создать диаграммы рассеяния для каждой области
4. Сохранить диаграммы рассеяния в виде файлов PNG

### **Используемые библиотеки:**

- pandas
- matplotlib

## **Структура репозитория**

- **`solution1.py`**: Python-скрипт для Части 1: Обработка данных
- **`solution2.py`**: Python-скрипт для Части 2: Визуализация данных
- ````main**.py**`: Python-скрипт запускающий оби части
- **`scatter_plots/`**: Папка, содержащая изображения диаграмм рассеяния для каждой области
- **`Тестовое задание.xlsx`**: Входные данные в формате Excel
- **`output_data.csv`**: Обработанные данные, сохраненные в виде файла CSV

## **Использование**

1. Установите необходимые зависимости:

```
pip install pandas matplotlib

```

1. Запустите скрипт **`solution1.py`** для обработки входных данных

```bash
python solution1.py
```

1. Запустите скрипт **`solution2.py`** для обработки входных данных

```bash
python solution2.py
```

Точечные диаграммы будут сохранены в виде PNG-файлов в папке **`scatter_plots/`**
