# Тестовое задание Junior Data Analyst
<a name="оглавление"></a>
* [Задание №1](#Задание_№1)
* [Решение Задания №1](#Решение_Задания_№1)
* [Задание №2](#Задание_№2)
* [Решение Задания №2](#Решение_Задания_№2)
* [Инструкция по запуску скрипта](#Инструкция_по_запуску_скрипта)
* [Графики рассеяния](#Графики_рассеяния)

<a name="Задание_№1"></a>
### Задание №1 — Работа с данными
Входные данные для тестового задания можно найти [здесь](https://docs.google.com/spreadsheets/d/165sp-lWd1L4qWxggw25DJo_njOCvzdUjAd414NSE8co/edit?usp=sharing) (или [здесь](https://docs.google.com/spreadsheets/d/1SWZCf9MSjP1wNuphLEOH9bA23qbUIyt9/edit?usp=sharing&ouid=100308789753749109392&rtpof=true&sd=true), резервная ссылка).
Ваша задача - подготовить и обработать исходные данных так, чтобы их можно было использовать во второй части задания.

**Требования к выходным данным:**
1.     В выходной таблице должны остаться только следующие колонки:
* _area, cluster, cluster_name, keyword, x, y, count, color_, где:
*  _area_ - область,
*  _cluster_ - номер кластера,
*  _cluster_name_ - название кластера,
*  _keyword_ - словосочетание,
*  _count_ - показатель,
*  _x_ и _y_ - координаты для диаграммы рассеяния,
*  _color_ - цвет точки на карте для данного словосочетания
2.      Колонку color нужно добавить самостоятельн
3.      Цвет задается каждому словосочетанию согласно следующими правилам:
* внутри одной области цвета словосочетаний в одном кластере должны быть одинаковые, в разных - отличаться (например, у "Кластер 1" все слова будут окрашены в красный, у "Кластер 2" - в зеленый и т.д.)
* цвета кластеров в разных областях могут повторяться
* цвета кластеров в разных областях с разным номером не имеют никакой связи (у одной области _[area]_ слова из "Кластер 1" могут быть красного цвета, в другой области у слов из "Кластер 1" может быть другой цвет)
4.     Не должно быть дубликатов слов в одной и той же области (area), но словосочетание может повторяться из area в area
5.     Колонки должны называться именно так, как указано в п.1
6.     Сортировка должна происходить по колонкам area, cluster, cluster_name, count (по count значения сортируются в убывающем порядке, в остальных - по возрастающему).
7.     Количество переданных в исходных ключевых слов должно совпадать с количество слов в выходных данных (за исключением дублированных строк или строк с пустыми\неформатными значениями по ключевым показателям [перечислены в п. 1], если такие имеются).
8.     Никакие другие особенности оформления не должны учитываться при обработке данных (заливка и пр.)
9.     Выходные данные должны быть аккуратно оформлены (заголовки закреплены, включен фильтр)
Формат представления выходных данных: google spreadsheet-таблица.
Выполнение данной работы желательно с помощью одной из библиотек:
* data.table ( R )
* pandas  (Python)

[оглавление](#оглавление)

<a name="Решение_Задания_№1"></a>
### Решение задания №1
Для решения используются библиотеки: **pandas, httplib2, discovery, ServiceAccountCredentials, csv, time, datetime, random**
1. Делаем себе [копию](https://docs.google.com/spreadsheets/d/18Pzfrg0VEoHBcZqB19Nl7SrcSZ4ivOnQgAQOfYCwe30/edit#gid=1439079331) Google Sheets, выдаем права на редактирование документа.
2. Читаем данные из нашей копии Google Sheets, вызвав функцию _google_API_get()_
```shell
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='tz_data',
        majorDimension='ROWS').execute()
```
3. Для удобного чтения полученных данных и дальнейшей обработки формируем файл "csv_data.csv", через функцию _csv_data()_
4. Вызвав функцию _analyst_data()_ приступаем к анализу и обработке данных:
* загрузка файла .csv в pandas DataFrame(двухмерная структура данных)
```shell
data = pd.read_csv('csv_data.csv', encoding="Windows-1251")  # encoding для чтения русских символов
```
* добавляем столбец color:
```shell
data.insert(8, 'color', None)  
```
* Преобразовываем аргументы(string) (значения в колонке _'count'_) в числовую форму, для дальнейшей сортировки значений по _'count'_:
```shell
    data['count'] = pd.to_numeric(arg=data['count'], errors='coerce', downcast='integer')
```
* Объявляем словарь "_d1_", Для предварительной записи "color", "keyword", что бы избежать повторов:
```shell
d1 = dict() 
``` 
* Через цикл _for_ добавляем в колонку color цвет в соответствии с условием, удаляем повтор "keyword" в одной области area:
```shell
for row in data.itertuples():  # получаем кортеж из строки по всем столбцам 
         # если значение count не число, то удаляем строку
         if ((type(row[6]) == str and (row[6] == '-') or (row[6] == 'N\\A') or (math.isnan(row[6])))):  # isnan проверяет, что бы count != nan
            data = data.drop(index=row[0])
            continue    
         # если область "area" (row[1]) нет в словаре, то добавляем его и его первый кластер (row[2]) + цвет (col)        
         if row[1] not in d1: 
            col = random.choice(color) # цвет выбираем из ранее созданного списка "color"
             # Добавляем в словарь: row[1] - область, row[2] - название кластера, row[4] - словосочетание
            d1[row[1]] = {row[2]: col, 'keyword':[row[4]]}]
            data.loc[row[0], 'color'] = col  # добавляем в колонку таблицы цвет
         
         # если "area" есть в словаре и "keyword" в этой области тоже есть, то удаляем новый повтор
         elif row[1] in d1 and row[4] in d1[row[1]]['keyword']:
            data = data.drop(index=row[0])
         
         # если в словаре есть "area" и есть кластер, то просто назначаем цвет ранее добавленного кластера
         elif row[1] in d1 and row[2] in d1[row[1]]:  
            data.loc[row[0], 'color'] = d1[row[1]][row[2]]  # добавляем в колонку таблицы цвет 
            d1[row[1]]['keyword'].append(row[4])  # добавляем в словарь словосочетание для выбранной области
        
         # если в словаре есть "area", но нет кластера, прибавляем кластер + новый цвет
         elif row[1] in d1 and row[2] not in d1[row[1]]:  
            col = random.choice(color)
            while col in d1[row[1]].values():  # смотрим, что бы не было повторов цветов у "area" 
                col = random.choice(color)
            d1[row[1]][row[2]] = col  
            d1[row[1]]['keyword'].append(row[4])
            data.loc[row[0], 'color'] = col  # добавляем в колонку таблицы цвет
```
* Сортировка по столбцам в порядке возрастания: 'area', 'cluster', 'cluster_name', в порядке убвания: 'count'
```shell
sort_data = data.sort_values(by=['area', 'cluster', 'cluster_name', 'count'],
                                 ascending=[True, True, True, False])  # сортировка по столбцам
```
5. Удаляем, через функцию _del_tab()_ ранее занесенные данные в нашем новом документе Google Sheets:
```shell
rangeAll = '{0}!A1:Z'.format("Лист1")
        body = {}
        resultClear = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=rangeAll,
                                                            body=body).execute()
```
6. В новом документе Google Sheets меняем ширину столбцов и применяем форматирование текста, через функции:
* tab_column_siz(startI, endI, size)
* tab_text_format_main(startRowIndex=0, endRowIndex=0, startColumnIndex=0, endColumnIndex=0, bold=False, fontSize=10 )

7. Вызываем функцию _tab_send_data()_ и начинаем процесс переноса обработанных и отсортированных данных:
```shell
total = 2  # начинаем со второй строки
    for row in data.itertuples():  # получаем кортеж из строки по всем столбцам 
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body={
            "valueInputOption": "USER_ENTERED",
            # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            # row[1] - "area", row[2] - 'cluster', row[3] - 'cluster_name', row[4] - 'keyword',
            # row[6] - 'count', row[7] - 'x', row[8] - 'y', row[9] - 'color'
            "data": [
                {"range": f"A{total}:H{total}",
                 "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                 "values": [
                     [f'{row[1]}', f'{row[2]}', f'{row[3]}', f'{row[4]}', f'{row[6]}', f'{row[7]}', f'{row[8]}', f'{row[9]}'],  # Заполняем строку

                 ]}
            ]
        }).execute()
        total += 1
        
        # API quota limitations из-за ограничения делаем паузу на 60сек после каждых 50 запросов
        if total % 50 == 0:  
            time.sleep(60)
            continue
```
[оглавление](#оглавление)
<a name="Задание_№2"></a>
### Задание №2 — Построение графиков
На основании обработанных данных постройте по одной диаграмме рассеяния для каждой области (_area_) (пример внешнего вида см. в приложенном [svg-файле](https://drive.google.com/file/d/1uxxkyPipGoR4ZLluxV7S1acLZw3Y4VuS/view?usp=sharing)).

**Требования к визуализации:**
* Наличие Footer-подписи на изображении
* Наличие легенды цветов и кластеров
* Перенос слишком длинных словосочетаний (например, слова длиннее 15 символов, можно разбить на "solar\n cell")
* Минимизация наложения (слепливания) подписей к друг на друга (постарайтесь сделать так, чтобы наложение было минимальным)
* Обводка точек.

Формат представления выходных данных: png-файлы размером не менее 1500х1500 пикселей с визуализациями  для каждой области (area).

Выполнение данной работы желательно с помощью одной из библиотек:
* ggplot2 ( R )
* Matploptlib  (Python)
* plotly (Python) и т.п.

[оглавление](#оглавление)
<a name="Решение_Задания_№2"></a>
### Решение задания №2
Для решения используются библиотеки: **pandas, matplotlib, seaborn**
1. Получаем значение строк по столбцу _area_:
```shell
area = sorted(list(set(data['area'].tolist())))  # set - чтобы не было повторов, list - чтобы применить сортировку по алфавиту
```
2. Через цикл _for_ формируем _data_area_ со всеми данными из таблицы по выбранной области _area_:
```shell
for ar in area:
    data_area = data.loc[data['area'] == f'{ar}']
    plot(data_area, ar.replace('\\', '.'), "_1")  # вызываем функцию plot
```
3. Вызываем функцию _plot(data=None, file_name="area", copy="")_ и создаем график рассеяния по выбранной области:
```shell
 plt.figure(figsize=(9, 7))  # размеры графика 1500х1500px
    ax = sns.lmplot(
               col="area",
               hue="cluster",
               x='x',  # Horizontal axis
               y='y',  # Vertical axis
               data=data,  # Data source
               fit_reg=False,  # Don't fix a regression line
               height = 15,
               aspect = 1)  # size and dimension 2
    sns.set(font_scale=1.1)   # размер надписей к осям
    plt.title(f'{file_name}')
    # Set x-axis label
    plt.xlabel('x')
    # Set y-axis label
    plt.ylabel('y')
```
4. Для того, что бы каждая точка на графике рассеяния была подписана нашим словосочетанием из keyword и для форматирования расположения текста подписи точек (во избежании наложении текста друг на друга) внутри функции _plot()_ вызываем функцию  *label_point(data.x, data.y, data.keyword, plt.gca())*:
```shell
    def label_point(x, y, val, ax):  # добавляем к каждой точке текстовую метку
        x_cord = list()  # лист х координат, что бы отслеживать близко лежащие точки
        y_cord = list()  # лист y координат, что бы отслеживать близко лежащие точки
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)  # формируем данные текущей области по колонкам: 'x', 'y', 'val'

        for i, point in a.iterrows():   # перебираем кортеж со значениями по строке 
            x_point = point['x']  # координата х
            y_point = point['y']  # координата y
            keyword_text = str(point['val'])  # текст над точкой из колонки ('keyword')
            if len(keyword_text) > 15:  # если длина текста больше 15
                keyword_text = "\n".join(keyword_text.split())  # разделяем каждое слово "\n"
                y_point -= 0.5  # смещение по y координате
            
            # для избежания наложения текста подписи точек выполняем условия:
            # если x координата лежит в диапазоне  x-0.7 >= x >= x+0.7 и 
            # если y координата лежит в диапазоне  y-0.3 >= y >= y+0.3 и 
            # если текст содержит (keyword_text) >= 1 символ переноса строки ('\n')
            if (round(float(point['x']), 1) in x_cord and round(float(point['y']), 1) in y_cord):
                if keyword_text.count('\n') >= 1:  # если слова с переносом
                    x_point -= 1.1  # смещение по x координате
                    y_point += 0.8  # смещение по y координате
            # если выше условие не выполняется, то заносим в лист x_cord значение x_point с шагом 0.1 в диапазоне от -0.7 до +0.7
            # тоже самое в лист y_cord значение y_point с шагом 0.1 в диапазоне от -0.3 до +0.3
            else:
                x_cord.extend([round(round(float(point['x']), 1) + (i / 10), 1) for i in range(-7, 8, 1)])
                y_cord.extend([round(round(float(point['y']), 1) + (i / 10), 1) for i in range(-3, 4, 1)])

            vv = ax.text(x_point + .1 ,  y_point, keyword_text)  # отображаем словосочетание keyword на графике

```
5. Сохраняем график рассеяния выбранной области в '.png"
```shell
ax.figure.savefig(f"plot/{file_name}{copy}.png")
```


[оглавление](#оглавление)

<a name="Инструкция_по_запуску_скрипта">**Инструкция по запуску скрипта**</a>
1. перейти в папку \Pandas_Matplotlib\script_run
2. в терминале находясь в папке "script_run" ввести следующую команду:
```shell
python data_plot.py run
```
После запуска скрипта в терминале будут приходить сообщения о ходе выполнения программы:
```shell
...
[19.09.2022 13:34:40] Чтение исходных данных Google Sheets - успешно завершено
[19.09.2022 13:34:40] Cоздан файл исходных данных Google Sheets: "csv_data.csv" 
[19.09.2022 13:34:40] Анализ данных, сортировка данных, добавление "color" - успешно завершено
[19.09.2022 13:34:40] Начат процесс переноса данных в новый Google Sheets
[19.09.2022 13:34:53] Перенесено: 50 - строк. Делаем паузу 60сек. (не перегружаем API)
..
[19.09.2022 13:39:40] Перенос данных в Google Sheets(ссылка ниже) - успешно завершено
[19.09.2022 13:39:40] https://docs.google.com/spreadsheets/d/19WU-rV31bktdBMZR1RM-ODJuuHamwcKaplPAJ-LEItY/edit#gid=0
[19.09.2022 13:39:40] Приступаем к созданию графиков
[19.09.2022 13:39:41] График для области ar\vr - успешно создан
...

```
[Таблица с обработанными данными в Google Sheets](https://docs.google.com/spreadsheets/d/19WU-rV31bktdBMZR1RM-ODJuuHamwcKaplPAJ-LEItY/edit#gid=0)

[Графики рассеяния доступны на Яндекс Диске](https://disk.yandex.ru/d/egxzcGJrNBtVNg)


[оглавление](#оглавление)

______
<a name="Графики_рассеяния">**Графики рассеяния**</a>

![Screenshot](/script_run/plot/ar.vr_1.png)

![Screenshot](/script_run/plot/available_1.png)

![Screenshot](/script_run/plot/capability_1.png)

![Screenshot](/script_run/plot/dialog_1.png)

![Screenshot](/script_run/plot/eligibility_1.png)

![Screenshot](/script_run/plot/except_1.png)

![Screenshot](/script_run/plot/greetings_1.png)

![Screenshot](/script_run/plot/housewives_1.png)

![Screenshot](/script_run/plot/lithuania_1.png)

![Screenshot](/script_run/plot/locator_1.png)

![Screenshot](/script_run/plot/personnel_1.png)

![Screenshot](/script_run/plot/protein_1.png)

![Screenshot](/script_run/plot/twisted_1.png)

![Screenshot](/script_run/plot/winner_1.png)

![Screenshot](/script_run/plot/worlds_1.png)

[оглавление](#оглавление)