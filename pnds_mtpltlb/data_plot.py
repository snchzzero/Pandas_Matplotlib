#графики
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from data_analyst import analyst_data

# plt.figure(figsize=(40, 10))
# grid = sns.FacetGrid(analyst_data(), col="area", hue="cluster", col_wrap=5, legend_out=True)
#
# grid.map(sns.scatterplot, "x", "y")
# grid.add_legend()
# grid.figure.savefig("output_5.png")

def plot(data=None, file_name="area", copy=""):
    #data = analyst_data()
    plt.figure(figsize=(40, 10))
    ax = sns.lmplot(
               col="area",
               hue="cluster",
               x='x', # Horizontal axis
               y='y', # Vertical axis
               data=data, # Data source
               fit_reg=False, # Don't fix a regression line
               height = 5,
               aspect =2 ) # size and dimension

    plt.title('Example Plot')
    # Set x-axis label
    plt.xlabel('Sepal Length')
    # Set y-axis label
    plt.ylabel('Sepal Width')


    def label_point(x, y, val, ax):
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
        for i, point in a.iterrows():
            ax.text(point['x']+.02, point['y'], str(point['val']))

    label_point(data.x, data.y, data.keyword, plt.gca())
    ax.figure.savefig(f"plot/{file_name}{copy}.png")

data = analyst_data()
area = sorted(list(set(data['area'].tolist())))  # получаем значение строк по столбцу area, set - чтобы небыло повторов, list - чтобы применить сортировку по алфавиту

for ar in area:
    data_area = data.loc[data['area'] == f'{ar}']
    plot(data_area, ar.replace('\\', '.'), "_2")
    # for row in data_area.itertuples():
    #     print(row)
    # print()
    # print()
