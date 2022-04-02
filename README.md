## News Guide

Будущее раcположение сайта: https://news_guide.herokuapp.com

____ 
### Описание проекта
Тема проекта: новостной агрегатор. Он имеет интуитивно понятный интерфейс, в котором удобно читать и создавать новостные статьи. На основной странице платформы будут выведены с помощью сторонних API курсы валют по ЦБ и популярные новости в настоящее время. Данный агрегатор должен помочь пользователю не запутаться в потоке новостей и собрать их в одном месте для быстрого и удобного прочтения или создания. 

____
### ТЗ проекта
Используемые API:
- Курсы валют ЦБ РФ в XML (https://www.cbr-xml-daily.ru/)
- Mews API (https://newsapi.org/)

Стек проекта:
- flask (flask_login, wtforms, flask_wtf)
- Bootstrap (v5.1.3)
- sqlalchemy (SQLite)

У пользователей нашей платформы не будет опасений по поводу их безопасности, так как форма регистрации предусматривает установку сложного пароля, состоящего из минимум 8 символов, латинских букв верхнего и нижнего регистров, цифр и специальных символов.

На главной странице пользователь видит свежие популярные новости, отобранные с помощью News API, новости других пользователей платформы и курсы доллара и евро по ЦБ России. С помощью инструментов платформы пользователь сможет создать свою новость, используя специальную форму, где можно будет прикрепить картинку к новости. Новости, написанные лично пользователем, будут видны в отдельной вкладке платформы. Каждая новость будет содержать в  себе заголовок, краткое описание, дату написания, картинку, указывающую на содержание новости, имя автора и сам текст новости. Если новость берётся из News API, то будет указываться и источник.

____
- master - основная ветка
- ars - ветка Арсения
- Kirill - ветка Кирилла
- test - ветка для тестов
____
