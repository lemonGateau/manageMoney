# -*- config: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt


def df_str_to_int(df):
    for column in df.columns:
        print(column)
        df[column] = df[column].str.replace('円', '')
        df[column] = df[column].str.replace(',', '').astype(int)

    return df

def df_int_to_str(df):
    for column in df.columns:
        for i in range(len(df[column])):
            try:
                df[column][i] = '{:,.0f}'.format(df[column][i]) + '円'
            except:
                pass

    return df

def df_to_png(df, plot_index=True, header=None, header_color="lightgray", png_path="pngs\\df1.png"):
    plt.rcParams["figure.subplot.left"] = 0
    plt.rcParams["figure.subplot.bottom"] = 0
    plt.rcParams["figure.subplot.right"] = 1
    plt.rcParams["figure.subplot.top"] = 1
    plt.rcParams["font.family"] = "meiryo"
    plt.rcParams["font.size"] = 16

    fig, ax = plt.subplots()
    ax.axis("off")

    if plot_index:
        df = df.reset_index()

    if header is None:
        table = ax.table(cellText=df.values, cellLoc="center", loc="center")
    else:
        if plot_index:
            header = header.insert(0, "_")

        table = ax.table(cellText=df.values, colLabels=header, cellLoc="center", loc="center")

        for i in range(df.shape[1]):
            table[0, i].set_facecolor(header_color)

    table.auto_set_font_size(False)

    if df.shape[0] < 10:
        cell_height = 1 / 10
    else:
        cell_height = 1 / df.shape[0]

    for pos, cell in table.get_celld().items():
        cell.set_height(cell_height)

    fig.savefig(png_path, dpi=800)

    # plt.show()
