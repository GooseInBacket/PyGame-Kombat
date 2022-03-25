# PyGame Kombat
### Реалика файтинга "Mortal Kombat 1"  
## 1. Краткое описание
Игра пытается клонировать всем известный файтинг "MK1"  
Обращу ваше внимание, что игра в отличие от оригинала сильно урезана.

!Данная игра создавалась исключительно в рамках проектной деятельности и не претендует на нарушение
авторских прав!

* В игре реализована возможность играть двум игрокам на одной  
клавиатуре. Тип клавиатуры - 100%. Без Нампада будет тяжко.
* Искусственный интеллект отсутствует  
* Специальные удары отсутствуют
* Рандомная локация при каждом новом матче
* Играют до двух побед
* Ничьей пока нет
* По завершению матча возвращает игроков на главный экран

## 2. Демонстрация
![Demo1](https://github.com/GooseInBacket/MK/blob/master/data/content/props/demo_1.png)
![Demo2](https://github.com/GooseInBacket/MK/blob/master/data/content/props/demo_2.png)
![Demo3](https://github.com/GooseInBacket/MK/blob/master/data/content/props/demo_3.png)

## 3. Установка:
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
## 4. Запуск
Есть два варианта запуска:
* Запустить main.exe
* Запустить файл main.py
## 5. Управление
* **Главное меню**
  * **(↑, ↓, ←, →)** - управление в меню
  * **Enter** - выбор / выход из настроек / завершить матч
  * **ESC** - пауза (во время игры)


* **Игрок №1**
  * **W** - прыжок
  * **S** - присесть
  * **A** - идти влево
  * **D** - идти вправо
  * **SPACE** - блок
  * **Q** - удар рукой
  * **E** - удар ногой в живот
  * **F** - удар ногой в голову
  * **W + (A / D) + E** - удар ногой в полёте
  * **S + F** - подсечка


* **Игрок №2**
  * **↑** - прыжок
  * **↓** - присесть
  * **←** - идти влево
  * **→** - идти вправо
  * **NUM-0** - блок
  * **NUM-1** - удар рукой
  * **NUM-2** - удар ногой в живот
  * **NUM-3** - удар ногой в голову
  * **↑ + (← / →) + NUM-1 - удар ногой в полёте**
  * **↓ + NUM-2** - подсечка

## 6. Источники
* Спрайты / Звуки  - [Mortal Kombat Warehouse](https://www.mortalkombatwarehouse.com/mk1/)
