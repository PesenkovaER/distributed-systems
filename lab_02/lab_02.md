# Лабораторная работа 2. Проектирование и реализация клиент-серверной системы. HTTP, веб-серверы и RESTful веб-сервисы

## Вариант 15

---

## Задание

Выполнить следующие задачи:

1. Анализ HTTP-ответов от ozon.ru при поиске товара.
2. Реализовать REST API "Каталог автомобилей".
3. Настроить Nginx как обратный прокси для Flask API.

---


## Архитектура решения

В работе реализована классическая **клиент-серверная архитектура** с использованием **Nginx** в качестве обратного прокси.

```mermaid
flowchart LR
    Client[Клиент<br>curl / браузер]
    Nginx[Nginx<br>обратный прокси]
    Flask[Flask API<br>app.py]
    Data[Хранилище данных<br>в памяти]

    Client -->|HTTP-запрос| Nginx
    Nginx -->|proxy_pass| Flask
    Flask --> Data
    Data --> Flask
    Flask -->|HTTP-ответ| Nginx
    Nginx --> Client
```
## Компоненты системы

**Клиент (curl / браузер)**  
Отправляет HTTP-запросы к Nginx для получения данных или отправки информации.

**Nginx**  
Выступает в роли обратного прокси. Принимает входящие запросы от клиента и перенаправляет их к Flask-приложению в соответствии с настроенным правилом `location /api/`.

**Flask API ([app.py](app.py))**  
Обрабатывает HTTP-запросы, полученные от Nginx. Реализует бизнес-логику работы с каталогом автомобилей (CRUD операции).

**Хранилище данных**  
Имитация базы данных. Данные о автомобилях (список `cars`) хранятся в оперативной памяти приложения Flask.

---

## Описание реализации

### Анализ HTTP-ответов Ozon

Для анализа HTTP-запросов использовалась утилита `curl`.

**Получение заголовков ответа:**
```bash
curl -I https://www.ozon.ru/search/?text=iphone
```
**Получение полного ответа:**
```bash
curl -i https://www.ozon.ru/search/?text=iphone
```
В ответе были проанализированы:
- HTTP статус-код: 307 Temporary Redirect
- тип содержимого (content-type): text/html
- используемый сервер: nginx

<img width="691" height="358" alt="image" src="https://github.com/user-attachments/assets/54e1338b-b45a-45c1-b420-628fa8d24747" />

*Скриншот: результат выполнения `curl -I`*

<img width="818" height="499" alt="image" src="https://github.com/user-attachments/assets/35dc786e-7402-46b2-b4de-45271904bb8c" />

*Скриншот: результат выполнения `curl -i`*

---

### Реализация REST API «Каталог автомобилей»

API реализован с использованием **Flask**.  
Код приложения находится в файле **[app.py](app.py)**

**Структура объекта Car:**
```json
{
  "id": 1,
  "make": "Toyota",
  "model": "Camry",
  "year": 2020
}
```
## Реализованные методы:

- `GET /api/cars` — получить список автомобилей
- `POST /api/cars` — добавить автомобиль

Запуск сервера выполняется командой:
```bash
python3 app.py
```
Сервер запускается на `http://127.0.0.1:5000`

<img width="644" height="276" alt="image" src="https://github.com/user-attachments/assets/86e36833-dd27-4ad6-a96a-b0cacdfd5829" />

📷 *Скриншот: запущенный Flask-сервер*

**Проверка API:**

Добавление автомобиля:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"make":"Toyota","model":"Camry","year":2020}' \
http://127.0.0.1:5000/api/cars
```
**Получение списка:**
```bash
curl http://127.0.0.1:5000/api/cars
```

<img width="649" height="510" alt="image" src="https://github.com/user-attachments/assets/b9c99851-6822-4a1d-bef8-e25a1cfca149" />

Скриншот: POST-запрос к API

**Получение списка по id**
```bash
curl http://127.0.0.1:5000/api/cars/1
```
<img width="802" height="171" alt="image" src="https://github.com/user-attachments/assets/a53894a3-4885-4042-867d-fd6c85405455" />


### Настройка Nginx как обратного прокси

Была выполнена установка Nginx командой `sudo apt install nginx -y`. После установки была настроена конфигурация в файле `/etc/nginx/sites-available/default`, куда добавлен блок `location /api/ { proxy_pass http://127.0.0.1:5000; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }`. Затем выполнена проверка конфигурации командой `sudo nginx -t` и перезапуск сервера `sudo systemctl restart nginx`. Работа прокси была проверена с помощью `curl http://localhost/api/cars` — запрос успешно прошел через Nginx и был перенаправлен на Flask-приложение.

<img width="702" height="103" alt="image" src="https://github.com/user-attachments/assets/8a9debec-32e7-4d97-8541-1fe356ec0328" />

*Скриншот: проверка конфигурации Nginx*

<img width="632" height="511" alt="image" src="https://github.com/user-attachments/assets/f8423e0b-48f0-4431-b943-2e8778046d80" />

*Скриншот: запрос через Nginx*

---

##  Используемые технологии

- Python 3
- Flask
- Nginx
- HTTP / REST
- curl

---

## Запуск проекта

Для запуска проекта необходимо активировать виртуальное окружение командой `source venv/bin/activate`, затем запустить Flask-сервер командой `python3 app.py` и Nginx командой `sudo systemctl start nginx`.

---

## Результат работы

В результате выполнения лабораторной работы был проведен анализ HTTP-запросов сайта Ozon с использованием `curl`, разработан REST API для работы с каталогом автомобилей на Flask, а также настроен Nginx в качестве обратного прокси для Flask-приложения. Обеспечено перенаправление запросов с Nginx на Flask API.

---

## 📌 Вывод

В ходе выполнения лабораторной работы были изучены принципы работы HTTP-протокола и проанализированы ответы веб-сервера. Был реализован REST API с использованием Flask, а также настроен Nginx как обратный прокси. В результате были получены практические навыки разработки веб-сервисов и работы с серверной инфраструктурой.
