# Кофейная карта Москвы
Эта программа запрашивает у вас абсолютно любое место в городе Москва и выдаёт необходимое вам количество кофеен (из ```.json``` файла со списком кофеен), переходя при этом на сайт с картой, где все кофейни отмечены синим маркером, а ваше местоположение красным.

## Как установить
Для начала необходимо зарегистрироваться в [Яндекс.Кабинет разработчика](https://developer.tech.yandex.ru/services/) и подключить API JavaScript API и HTTP Геокодер (тариф бесплатный с ограничениями). Это необходимо для получения координаты места, которое вам необходимо. 

Сохранять API публично плохая идея. Потому, после получения API-интерфейса все чувствительные данные стоит скрыть. Для этого в корне репозитория нужно создать ```.env``` файл и поместить ключ туда, прописав:
```python
YANDEX_API_KEY='Ваш API-ключ'
```
в самом коде это выглядит так:
```python
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
```
В проекте используется пакет [python-dotenv](https://github.com/theskumar/python-dotenv). Он позволяет загружать переменные окружения из файла .env в корневом каталоге приложения.
Этот .env-файл можно использовать для всех переменных конфигурации.
Ну и естественно Python3 должен быть уже установлен. Затем используйте pip (или pip3,если есть конфликт с Python2) для установки зависимостей:
```python
pip install -r requirements.txt
```
## Как пользоваться 
После запуска ```main.py``` она попросит у вас ввести ЛЮБОЕ место в Москве (Например:Новый Арбат) и выведет вам линк на сайт, где уже и находится карта c метками.

![](https://user-images.githubusercontent.com/83189636/131366888-96cfca93-bfe7-476b-9388-dbafef102b1b.PNG)
![](https://user-images.githubusercontent.com/83189636/131366969-ec199e14-07a2-4cef-9cd4-d619bd92e204.PNG) 

Примеры запуска скрипта в консоли.



 
