from random import randint, choice
import matplotlib.pyplot as plt
from SourceData import *


if __name__ == '__main__':
    print('Now loading workbooks...')
    workbooks = WBS("sDataF_P1XYZ_0208_1", "sDataF_P2XYZ_0208_1", "sDataF_P3XYZ_0208_1")

    for state in ['1', '3', '9', '13', '15']:
        print('Workbooks loaded, now processing data...')
        dataframe = SensorData(workbooks, state).dataframing()
        # column = choice(dataframe.columns)
        column = 'x1'
        column_data = dataframe[column]
        avg_val = column_data.mean()
        std_val = column_data.std()
        skew_val = column_data.skew()
        kurt_val = column_data.kurtosis()

        print('All set, now ploting...')
        plt.figure(figsize=(10, 6))
        plt.scatter(column_data.index, column_data.values, label=column, color='black', s=1)
        plt.axhline(y=avg_val, color='red', linestyle='--', label=f'Mean: {avg_val:.2f}')
        plt.axhline(y=std_val, color='green', linestyle='--', label=f'Std: {std_val:.2f}')
        plt.axhline(y=skew_val, color='blue', linestyle='--', label=f'Skew: {skew_val:.2f}')
        plt.axhline(y=kurt_val, color='yellow', linestyle='--', label=f'Kurtosis: {kurt_val:.2f}')
        plt.title(f'Data Plot for state {state}, column {column}')
        plt.xlabel('Index')
        plt.ylabel('G-value')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'../Factory/Assets/{state}-{column}-{randint(10000, 99999)}_.png')

    workbooks.wclose()
