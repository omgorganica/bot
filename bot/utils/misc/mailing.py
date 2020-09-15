import os
import smtplib  # Импортируем библиотеку по работе с SMTP
# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения

from dotenv import load_dotenv

load_dotenv()

addr_from = os.getenv("email_from")  # Адресат
addr_to = str(os.getenv("email_to"))  # Получатель
password = str(os.getenv("email_password"))  # Пароль

msg = MIMEMultipart()  # Создаем сообщение
msg['From'] = addr_from  # Адресат
msg['To'] = addr_to  # Получатель
msg['Subject'] = 'Результат работы старшего смены'  # Тема сообщения

body = "Test message"
msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

server = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
server.starttls()  # Начинаем шифрованный обмен по TLS
server.login(addr_from, password)  # Получаем доступ
server.send_message(msg)  # Отправляем сообщение
server.quit()  # Выходим
