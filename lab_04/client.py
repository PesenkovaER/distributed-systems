import requests
from cryptography.fernet import Fernet
import json
import sys

# загрузка ключа
with open("encryption_key.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# ввод сообщения
data = input("Введите сообщение: ")

encrypted = fernet.encrypt(data.encode()).decode()

# отправка с обработкой ошибок
try:
    resp = requests.post(
        "http://127.0.0.1:8000/api/data",
        json={"data": encrypted},
        timeout=5
    )
except requests.exceptions.ConnectionError:
    print("\nОшибка: Координатор не запущен (порт 8000)")
    print("Файл не сохранен.")
    sys.exit(1)

print("\nОтвет сервера:")
print(resp.json())

# проверка успешности отправки
response_data = resp.json()
if "error" in response_data:
    print(f"\nОшибка: {response_data['error']}")
    print("Файл не сохранен.")
    sys.exit(1)

# выбор формата
fmt = input("\nВыберите формат (json/csv/xml): ")

try:
    resp = requests.get(
        f"http://127.0.0.1:8000/export?format={fmt}",
        timeout=5
    )
except requests.exceptions.ConnectionError:
    print("\nОшибка: Координатор не запущен (порт 8000)")
    print("Файл не сохранен.")
    sys.exit(1)

print("\nЭкспорт данных:")
print(resp.text)

# проверка успешности экспорта
if resp.status_code != 200:
    print(f"\nОшибка экспорта: {resp.text}")
    print("Файл не сохранен.")
    sys.exit(1)

# проверка на наличие ошибки в данных
try:
    export_data = resp.json() if fmt == "json" else resp.text
    if isinstance(export_data, dict) and "error" in export_data:
        print(f"\nОшибка: {export_data['error']}")
        print("Файл не сохранен.")
        sys.exit(1)
except:
    pass

# СОХРАНЕНИЕ В ФАЙЛ (только если нет ошибок)
filename = f"exported_data.{fmt}"

with open(filename, "w", encoding="utf-8") as f:
    f.write(resp.text)

print(f"\nФайл сохранен как: {filename}")