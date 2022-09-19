import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from data_analyst import google_API_send, now



def plot(data=None, file_name="area", copy=""):

    plt.figure(figsize=(9, 7))  #1500х1500px
    ax = sns.lmplot(
               col="area",
               hue="cluster",
               x='x', # Horizontal axis
               y='y', # Vertical axis
               data=data, # Data source
               fit_reg=False, # Don't fix a regression line
               height = 15,
               aspect = 1) # size and dimension 2
    sns.set(font_scale=1.1)  # размер надписей к осям
    plt.title(f'{file_name}')
    # Set x-axis label
    plt.xlabel('x')
    # Set y-axis label
    plt.ylabel('y')


    def label_point(x, y, val, ax):  # добавляем к кажой точке текстовую метку
        x_cord = list()  #словарь, что бы остлеживать близко лежащие точки по координатам
        y_cord = list()
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)

        for i, point in a.iterrows():
            x_point = point['x']
            y_point = point['y']
            keyword_text = str(point['val'])  # текст над точкой из колонки ('keyword')
            if len(keyword_text) > 15:
                keyword_text = "\n".join(keyword_text.split())
                y_point -= 0.5
            if (round(float(point['x']), 1) in x_cord and round(float(point['y']), 1) in y_cord):
                if keyword_text.count('\n') >= 1:  # если слова с переносом
                    x_point -= 1.1
                    y_point += 0.8

            else:
                x_cord.extend([round(round(float(point['x']), 1) + (i / 10), 1) for i in range(-7, 8, 1)])
                y_cord.extend([round(round(float(point['y']), 1) + (i / 10), 1) for i in range(-3, 4, 1)])


            vv = ax.text(x_point + .1 ,  y_point, keyword_text)  # rotation=45 если надо повернуть текст
            #print(vv)

    label_point(data.x, data.y, data.keyword, plt.gca())
    ax.figure.savefig(f"plot/{file_name}{copy}.png")


data = google_API_send()
area = sorted(list(set(data['area'].tolist())))  # получаем значение строк по столбцу area, set - чтобы небыло повторов, list - чтобы применить сортировку по алфавиту

# plot(data.loc[data['area'] == 'available'], "available", "_1")

print(f'[{now()}] Приступаем к созданию графиков')
for ar in area:
    data_area = data.loc[data['area'] == f'{ar}']
    plot(data_area, ar.replace('\\', '.'), "_1")
    print(f'[{now()}] График для области {ar} - успешно создан')

print(f'[{now()}] Всего создано: {len(area)} - графиков')
print(f'[{now()}] Скрипт успешно завершил свою работу!')

