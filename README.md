# PyGame Kombat
### Реалика файтинга "Mortal Kombat 1"  
## 1. Краткое описание
Игра пытается клонировать всем известный файтинг "MK1"  
Обращу ваше внимание, что игра в отличие от оригинала сильно урезана.

* В игре реализована возможность играть двум игрокам на одной  
клавиатуре. 
* Искусственный интеллект отсутствует  
* Большая часть мувсета отсутствует
* Реализованы только движения и удары
* Рандомная локация при каждом новом матче
* Время на матч бесконечное
* Количество раундов: 1. До первой победы
* Добивания и фаталити отсутствуют
* По завершению матча возвращает игрока на главный экран по нажатию на Enter

## 2. Демонстрация
![Image alt](https://github.com/GooseInBacket/MK/blob/master/data/content/props/demo_1.png)
![Image alt](https://github.com/GooseInBacket/MK/blob/master/data/content/props/demo_2.png)
![Image alt](https://github.com/GooseInBacket/MK/blob/master/data/content/props/demo_3.png)

## 2. Установка:
### **!Внимание: В проекте используется Python 3.10!**

Выполните стандартный набор команд в консоле, чтобы запустить проект:
* Установить виртуальное окружение
```commandline
python -m venv env
```
* Из корня папки перейти и выполнить 
```commandline 
cd env/scripts/activate.bat
```
* Установить зависимости 
```commandline
pip install requirements.txt 
```
* Если всё прошло успешно, то приложение готово к использованию
## 3. Запуск
Есть два возможных варианта:
* файл main.exe
* файл main.py
## 4. Управление
* **Главное меню**
  * **(↑, ↓, ←, →)** - управление в меню
  * **Enter** - выбор / выход из настроек / завершить матч


* **Игрок №1**
  * W - прыжок
  * S - присесть
  * A - идти влево
  * D - идти вправо
  * Q - блок
  * i - удар рукой
  * O - удар ногой в живот
  * P - удар ногой в голову


* **Игрок №2**
  * ↑ - прыжок
  * ↓ - присесть
  * ← - идти влево
  * → - идти вправо
  * NUM-0 - блок
  * NUM-1 - удар рукой
  * NUM-2 - удар ногой в живот
  * NUM-3 - удар ногой в голову
