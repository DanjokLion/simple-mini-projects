"""
Метод работы: 
 Данный код будет работать только если в папке с этим кодом находятся файлы из списка далее:
 
    Остаток на 12.12.xlsx - в данном случае датой выступает дата файла сделанного ровно неделю назад;
    остатки.xlsx - выгрузка, файл должен быть отредактирован макросом 'обработка выгрузок из 1с';
    продажи.xlsx - выгрузка, файл должен быть отредактирован макросом 'обработка выгрузок из 1с';
    Итог - файл, который будет внедрен в итоговый массив данных, 
        он не читается методами, которые здесь были использованы
 
 Файлы которые создает этот скрипт:
    Остаток на 20.12.xlsx - Создается копия исходного файла с прошлой недели с сегодняшней датой,
        чтобы не менять исходный файл, потому что прошлые файлы могут понадобиться людям и является отчетностью
    Остатки 20.12.xlsx - Создает для того, 
        чтобы внедрить его в основной excel файл и изменить исходные данные в сводных таблица 
    Продажи 20.12.xlsx - Создает для работы других сотрудником с этим файлом, если это того потребует
 """


from datetime import *

from openpyxl import *
from time import *
import pandas as pd
import shutil
import os

def create_time():
    # Создание используемых дат в файлах
    startP = time()
    global today, now_date, one_week_ago
    global h, m

    # Создание даты для создания, редактирования и удобства дальнейшей работы
    today = datetime.now()
    now_date = today.strftime('%d.%m')
    one_week_ago = (today - timedelta(days=7)).strftime('%d.%m')

    # Задание времени для именования Продаж
    file_info = datetime.fromtimestamp((os.stat('продажи.xlsx')).st_ctime)
    h, m = file_info.hour, file_info.minute
    print('программа выполнялась ' + str(time() - startP))

def copy_files(): 
    # Копирование файлов и сохранение используемых для сравнения таблиц
    startP = time()
    global remnant_ago
    global sales_ago 
    global glay
    global prod_line

    # Копирование файла с прошлой недели в настоящую
    source = f'C:\\Users\\azhilenkov\\Desktop\\try\\Остаток на {one_week_ago}.xlsx'
    new_file = f'C:\\Users\\azhilenkov\\Desktop\\try\\Остаток на {now_date}.xlsx'
    shutil.copyfile(source, new_file)

    # Объявление файлов
    remnant_ago = pd.read_excel(f'Остаток на {now_date}.xlsx', sheet_name=f'Остатки {one_week_ago}')
    sales_ago = pd.read_excel(f'Остаток на {now_date}.xlsx', sheet_name=f'Продажи {one_week_ago}')
    glay = pd.read_excel(f'Остаток на {now_date}.xlsx', sheet_name='Подклеить')
    prod_line = pd.read_excel(f'Остаток на {now_date}.xlsx', sheet_name='Линии')

    print('программа выполнялась ' + str(time() - startP))

def copy_edit():
    # Создание переменных с таблицами, которые будут редактироваться в этом файле
    startP = time()
    global remnant
    global sales

    # Объявление файлов из других книг, для внедрения их в основную таблицу
    remnant = pd.read_excel(f'остатки.xlsx', sheet_name='Лист1')
    remnant = remnant.drop(remnant.index[-1])
    sales = pd.read_excel(f'продажи.xlsx', sheet_name='Лист1')
    sales = sales.drop(0)
    sales = sales.drop(sales.index[-1])

    # Функции добавления новых ПУСТЫХ столбцов в используемые таблицы
    def remnant_add():
        # Добавление новых столбцов в таблицу Остатков
        add_list_remnant = [[0, 'склад рез', ''],[1, 'склад', ''],[2, 'признак основной', ''],
                            [3, 'признак доп', ''],[9, 'Список ассортимента рез', ''],[12, 'норматив для производства, дней', ''],
                            [13, 'норм-в сетевого резерва, дней', ''],[14, 'прогноз на месяц', ''],[19, 'цех', ''],[20, 'Линия производства с приоритета1', ''],
                            [21, 'взаимозаменяемость линии', ''], [22, 'площадка производства', '']]
        for value in add_list_remnant:
            remnant.insert(*value)
        

    def sales_add():
        # Добавление новых столбцов в таблицу Продаж
        add_list_sale = [[0, 'склад рез', ''],[1, 'склад', ''],[2, 'признак основной', ''],
                            [3, 'признак доп', ''],[4, 'Площадка', ''],[5, 'Склад компании', ''],
                            [9, 'Список ассортимента рез', ''],[12, 'норматив для производства, дней', ''],
                            [13, 'норм-в сетевого резерва, дней', ''],[14, 'прогноз на месяц', ''],
                            [15, 'Начальный остаток', ''],[16, 'Приход', ''],[17, 'Расход', ''],[18, 'Конечный остаток', ''],[19, 'цех', ''],[20, 'Линия производства с приоритета1', ''],
                            [21, 'взаимозаменяемость линии', ''],[22, 'площадка производства', '']]
        for value in add_list_sale:
            sales.insert(*value)
    
    remnant_add()
    sales_add()
    print('программа выполнялась ' + str(time() - startP))


def filling_cells_rem():
    # Полное обновление файла остатков в соответсвии с инструкцией
    startP = time()
    global remnant

    def update_comp(row):
        # Обновление Складов компании в соответсвии сладам компании из старого файла, аналог ВПР
        global remnant
        old_comp = remnant_ago['Склад компании'].tolist()
        
        if row['Склад компании'] in old_comp:
            index_ago = remnant_ago.index[remnant_ago['Склад компании'] == row['Склад компании']].tolist()
            value = remnant_ago.loc[index_ago[0], 'склад рез']
            row['склад рез'] = value
        elif 'Накопление' in row['Склад компании']:
            row['склад рез'] = 'накопления'
        elif 'НЗ' in row['Склад компании']:
            row['склад рез'] = 'НЗ'
        elif 'Склад материалов' in row['Склад компании']:
            row['склад рез'] = 'проч'
        elif 'Склад' in row['Склад компании']:
            row['склад рез'] = 'в пути'
        else:
            row['склад рез'] = '#Н/Д'
        return row
    
    def update_sign_addit(row):
        # Обновление Признак доп
        if row['признак доп'] in ['дистр', 'сети']:
            row['признак доп'] = 'доступный'
        return row

    def update_sign_main(row):
        # Обновление признак основной
        match row['склад']:
            case 'дистр':
                row['признак основной'] = 'дистр/эксп'
            case 'сети':
                row['признак основной'] = 'сети'
            case _:
                row['признак основной'] = 'замороженный'
        return row

    # Основные обновления таблицы
    remnant = remnant.apply(update_comp, axis=1)
    remnant['склад'] = remnant['склад рез'].copy()

    remnant['Список ассортимента рез'] = remnant['Список ассортимента'].copy()
    remnant['Список ассортимента'] = remnant['Список ассортимента'].replace('Группа1 A', 'Группа1') 

    remnant.loc[(remnant['АналитическоеНаименование'].str.contains('SRP')) & (remnant['склад рез'] == 'дистр'), 'склад'] = 'сети'
    
    remnant['признак доп'] = remnant['склад'].copy()
    remnant = remnant.apply(update_sign_addit, axis=1)

    remnant = remnant.apply(update_sign_main, axis = 1)
    # remnant.to_excel('test_remnant.xlsx', sheet_name='Лист1', index=False)
    print('программа выполнялась ' + str(time() - startP))



def filling_cells_sales():
    # Полное обновление файла продаж в соответствии с инструкцией
    startP = time()
    global sales
    global new_sales 

    def update_sign_main(row):
        # Обновление признак основной в соответствии с столбцов канала сбыта

        match row['Клиент для аналитики.Канал сбыта главный']:
            case 'Дистрибьютор':
                row['признак основной'] = 'дистр/эксп'
            case 'Экспорт':
                row['признак основной'] = 'дистр/эксп'
            case'Сети':
                row['признак основной'] = 'сети'
            case _:
                row['признак основной'] = '#Н/Д'
        return row


    # Основные обновления таблицы
    sales['Список ассортимента рез'] = sales['Список ассортимента'].copy()
    sales['Список ассортимента'] = sales['Список ассортимента'].replace('Группа1 A', 'Группа1') 
    
    sales['Конечный остаток'] = sales['Итого'].copy()

    sales['признак доп'] = sales['признак доп'].apply(lambda x: 'в накладных') 

    sales = sales.apply(update_sign_main, axis = 1)
    new_sales = sales.drop(['Код', 'Клиент для аналитики.Регион продаж', 'Клиент для аналитики.Канал сбыта главный', 'Клиент для аналитики.Группа дистрибьютеров', 'Код.1', 'Номенклатура.Тип фасовки', 'Декабрь 2023', 'Итого'], axis=1)
    
    # Приравниваем названия столбцов к тем, что нам нужны
    new_sales.columns = remnant.columns

    print('программа выполнялась ' + str(time() - startP))
    # sales.to_excel('test_sales.xlsx', sheet_name='Лист1', index=False)


def append_tables():
    # Слияние таблиц, для общего итога
    startP = time()
    global remnant
    global new_sales
    global glay
    remnant = pd.concat([remnant, new_sales])
    remnant = pd.concat([remnant, glay])
    print('программа выполнялась ' + str(time() - startP))

    
def normals():
    # Слияние с нормами производства
    startP = time()
    global remnant

    def update_of_brand(row):
        # Обновление норм производства в соответсвии с прошлым файлом
        global remnant

        old_comp = remnant_ago['Brand SKU'].tolist()

        if row['Brand SKU'] in old_comp:
            index_ago = remnant_ago.index[remnant_ago['Brand SKU'] == row['Brand SKU']].tolist()
            if index_ago:
                value = remnant_ago.loc[index_ago[0], 'норматив для производства, дней']
                row['норматив для производства, дней'] = value
                value = remnant_ago.loc[index_ago[0], 'норм-в сетевого резерва, дней']
                row['норм-в сетевого резерва, дней'] = value
            else:
                row['норматив для производства, дней'] = 15
                row['норм-в сетевого резерва, дней'] = 14
        else:
            row['норматив для производства, дней'] = 15
            row['норм-в сетевого резерва, дней'] = 14
        
        return row
    
    def update_workshop(row):
        # Обновление линий производства в соответствии с закреплением линий производства
        global remnant

        prod_line_brand = prod_line['Brand'].tolist()
        list_cells = ['цех','Линия производства с приоритета1',
                      'взаимозаменяемость линии','площадка производства']

        if row['Brand SKU'] in prod_line_brand:
            index_ago = prod_line.index[prod_line['Brand'] == row['Brand SKU']].tolist()
            for valCell in list_cells:
                if index_ago:
                    value = prod_line.loc[index_ago[0], valCell]
                    row[valCell] = value
                else:
                    row[valCell] = 0
        else: 
            row['цех'] = 0
            row['Линия производства с приоритета1'] = 0
            row['взаимозаменяемость линии'] = 0
            row['площадка производства'] = 0

        return row

    remnant = remnant.apply(update_of_brand, axis = 1)
    remnant = remnant.apply(update_workshop, axis = 1)

    # remnant.to_excel('test_final.xlsx', sheet_name='Лист1', index=False)
    print('программа выполнялась ' + str(time() - startP))
    

def integrate():
    # Создание файлов для дальнейшей работы
    startP = time()
    global sales
    global remnant
    global now_date

    remnant.to_excel(f'Остатки {now_date}.xlsx', sheet_name=f'Остатки {now_date}')
    sales.to_excel(f'Продажи {now_date}.xlsx', sheet_name=f'Продажи {now_date}')

    print('программа выполнялась ' + str(time() - startP))


def start_all():
    # Запуск всех функций
    create_time()
    copy_files()
    copy_edit()
    filling_cells_rem()
    filling_cells_sales()
    append_tables()
    normals()
    integrate()


start_all()