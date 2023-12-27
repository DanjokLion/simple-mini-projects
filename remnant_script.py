text_to_faq = """
Метод работы:
 1. Нужно выгрузить два отчета: 
    Назвать остатки.xlsx - формируется в 1c торг => запасы(склад) => ведомость по товарам на складах
    Вместе с ним, одновременно, поставив время через минуту должен формироваться следующий отчет
    Назвать продажи.xlsx - формируется в 1с торг => продажи => продажи с комиссией 
        настройка к нему находится по ссылке к файловому менеджеру, ее можно скопировать и перейти к ней => \\\\slv-fs01.obr.local\\Отдел А и П\\1_ ОТЧЕТЫ\\22. Анализ остатков для производства\\инструкция

 2. Данный код будет работать только если в папке с этим кодом находятся файлы из списка далее:
    Остаток на 12.12.xlsx - в данном случае датой выступает дата файла сделанного ровно неделю назад;
    остатки.xlsx - выгрузка, файл должен быть отредактирован макросом 'обработка выгрузок из 1с';
    продажи.xlsx - выгрузка, файл должен быть отредактирован макросом 'обработка выгрузок из 1с';
    Итог - файл, который будет внедрен в итоговый массив данных, 
        он не читается методами, которые здесь были использованы
 
 3. Файлы которые создает этот скрипт:
    Остаток на 20.12.xlsx - Создается копия исходного файла с прошлой недели с сегодняшней датой,
        чтобы не менять исходный файл, потому что прошлые файлы могут понадобиться людям и является отчетностью
    Остатки 20.12.xlsx - Создает для того, 
        чтобы внедрить его в основной excel файл и изменить исходные данные в сводных таблица 
    Продажи 20.12.xlsx - Создает для работы других сотрудником с этим файлом, если это того потребует
 
 4. После выполнения программы нужно проверить нет ли Н/Д в столбце 'склад рез', из-за него могут пойти несостыковки в остальных столбцах, если есть нужно доделать по аналогии с остальными

 5. Дальше Добавляем новые сгенерированные файлы Остаток и Продажи сегодняшнего числа в основной сформированный файл Остатки на сегодняшнее число

 6. Обновляем и меняем исходную таблицу у всех сводных таблиц с 1 по 4, в 2 и 3 листе находится по 2 таблицы

 7. После обновления нужно подкорректировать так, чтобы таблицы соответствовали шаблону, шаблон находится на листе 'Итог'

 8. Выделяем готовые таблицы, удаляем такие же на листе 'Итог' и вставляем как картинку

 9. Готово! Можем печатать первый лист к дирекции

  """

from customtkinter import *
from datetime import *
from time import *
import pandas as pd
import shutil
import os
import xlsxwriter

global months
global link_to_repos
global old_link

months = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}

months_abb = {
    1: 'Янв',
    2: 'Фев',
    3: 'Мар',
    4: 'Апр',
    5: 'Май',
    6: 'Июн',
    7: 'Июл',
    8: 'Авг',
    9: 'Сен',
    10: 'Окт',
    11: 'Ноя',
    12: 'Дек'
}

def main():
    # Внешняя оболочка программы
    set_appearance_mode('dark')
    set_default_color_theme('dark-blue')

    root = CTk()
    root.title('Формирование остатков')
    root.geometry('450x450')
    # Всплывающие окна-уведомления
    def show_popup(name, message):
        popup = CTkToplevel(root)

        popup.title(name)

        label = CTkLabel(popup, text=message, wraplength=250)
        label.pack(anchor=NW, padx=6, pady=6)

        btn = CTkButton(popup, text="OK", command=popup.destroy)
        btn.pack(side='bottom', anchor='center', padx=6, pady=6)

    def get_link():
        # Получение ссылки из формы
        global link_to_repos
        global old_link
        try:
            old_link = entry.get()
            link_to_repos = entry.get()
            os.startfile(link_to_repos)
            show_popup('Подтверждение', """Сейчас откроется папка с файлом
    переместите туда файлы нужные для работы""")
        except:
            old_link = f'\\\\slv-fs01.obr.local\\Отдел А и П\\1_ ОТЧЕТЫ\\22. Анализ остатков для производства\\{datetime.now().year} г\\{((datetime.now()) - timedelta(days=30)).strftime("%m. %B")}'
            os.mkdir(f'\\\\slv-fs01.obr.local\\Отдел А и П\\1_ ОТЧЕТЫ\\22. Анализ остатков для производства\\{datetime.now().year} г\\{datetime.now().month}. {months[datetime.now().month]}') 
            link_to_repos = entry.get()
            os.startfile(link_to_repos)
            show_popup('Подтверждение', 'Была создана новая папка, т.к. предыдущий отчет был в папке за прошлый месяц')

    def start_form():
        try:
            start_all()
            show_popup('Выполнено!', 'Отчет сформировался, дело за малым')
        except Exception as e:
            show_popup('Ошибка', 'Возникла ошибка при выполнении, обратитесь к документации')
            print('Произошла ошибка ', type(e))
            print('Сообщение об ошибке ', e)

    def faq_show():
        # Показ окна с инстуркцией и описание программы
        def scroll_text(event):
            label.yview_scroll(-1*(event.delta),'units')

        popup = CTkToplevel(root)
        popup.geometry('500x600')

        popup.title('Инструкция к программе и возможные возникшие вопросы')

        label = CTkTextbox(popup)
        label.pack(side='left', fill='both', expand=True)

        label.insert('end', text_to_faq)
        label.bing('<MouseWheel>', scroll_text)
        btn = CTkButton(popup, text="Close", command=popup.destroy)
        btn.pack(side='bottom', anchor='center', pady=10)

        popup.mainloop()
        

    def get_remnant():
        try:
            show_popup('Успешно', 'Выгрузка остатков выполнена успешно, продолжайте работу')
        except:
            show_popup('Ошибка','Произошла неизвестная ошибка, попробуйте выгрузить самостоятельно')

    def get_sales():
        try:
            show_popup('Успешно', 'Выгрузка продаж выполнена успешно, продолжайте работу')
        except:
            show_popup('Ошибка','Произошла неизвестная ошибка, попробуйте выгрузить самостоятельно')


    label_entry = CTkLabel(root, text="""Введите новый путь к папке, если ссылка по умолчанию некорректна
    Формат ссылки должен быть таким, слеши дублировать: 'C:\\Users\\azhilenkov\\Desktop\\' """, wraplength=450)
    label_entry.pack(anchor=NW, padx=6, pady=6)

    entry = CTkEntry(root, width=450)
    entry.insert(0, f'\\\\slv-fs01.obr.local\\Отдел А и П\\1_ ОТЧЕТЫ\\22. Анализ остатков для производства\\{datetime.now().year} г\\{datetime.now().month}. {months[datetime.now().month]}')
    entry.pack(anchor=NW, padx=8, pady=8)


    btn = CTkButton(root, text='Подтвердить ссылку', command=get_link, width=60)
    btn.pack(anchor=NW, padx=6, pady=6)

    btn = CTkButton(root, text='Сформировать массив остатков', command=get_remnant, width=60)
    btn.pack(anchor=NW, padx=6, pady=6)

    btn = CTkButton(root, text='Сформировать массив продаж', command=get_sales, width=60)
    btn.pack(anchor=NW, padx=6, pady=6)

    btn = CTkButton(root, text='Подговить фабричный прогноз для подклейки', command=update_glay, width=60)
    btn.pack(anchor=NW, padx=6, pady=6)

    btn = CTkButton(root, text='Начать формирование Остатков', command=start_form, width=60)
    btn.pack(side='bottom', padx=6, pady= 40 )


    btn = CTkButton(root, text='?', command=faq_show, corner_radius=50, width=2)
    btn.place(relx=1.0, rely=1.0, anchor='se')


    root.mainloop()


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
    file_info = datetime.fromtimestamp((os.stat(f'{link_to_repos}\\продажи.xlsx')).st_ctime)
    h, m = file_info.hour, file_info.minute
    print('программа выполнялась ' + str(time() - startP))

def copy_files():
    # Копирование файлов и сохранение используемых для сравнения таблиц
    startP = time()
    global remnant_ago
    global sales_ago 
    # global glay
    global prod_line

    # Копирование файла с прошлой недели в настоящую
    source = f'{old_link}\\Остаток на {one_week_ago}.xlsx'
    new_file = f'{link_to_repos}\\Остаток на {now_date}.xlsx'
    shutil.copyfile(source, new_file)

    # Объявление файлов
    remnant_ago = pd.read_excel(f'{link_to_repos}\\Остаток на {now_date}.xlsx', sheet_name=f'Остатки {one_week_ago}')
    sales_ago = pd.read_excel(f'{link_to_repos}\\Остаток на {now_date}.xlsx', sheet_name=f'Продажи {one_week_ago}')
    # glay = pd.read_excel(f'{link_to_repos}\\Остаток на {now_date}.xlsx', sheet_name='Подклеить')
    prod_line = pd.read_excel(f'{link_to_repos}\\Остаток на {now_date}.xlsx', sheet_name='Линии')

    print('программа выполнялась ' + str(time() - startP))

def copy_edit():
    # Создание переменных с таблицами, которые будут редактироваться в этом файле
    startP = time()
    global remnant
    global sales

    # Объявление файлов из других книг, для внедрения их в основную таблицу
    remnant = pd.read_excel(f'{link_to_repos}\\остатки.xlsx', sheet_name='Лист1')
    remnant = remnant.drop(remnant.index[-1])
    sales = pd.read_excel(f'{link_to_repos}\\продажи.xlsx', sheet_name='Лист1')
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
    new_sales = sales.drop(['Код', 'Клиент для аналитики.Регион продаж', 'Клиент для аналитики.Канал сбыта главный', 'Клиент для аналитики.Группа дистрибьютеров', 'Код.1', 'Номенклатура.Тип фасовки', f'{months[datetime.now().month]} {datetime.now().year}', f'{months[datetime.now().month + 6]} {datetime.now().year}', 'Итого'], axis=1)
    
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
    

def update_glay():
    global glay
    date_day = datetime.now().day
    date_month = datetime.now().month

    # df = pd.read_excel(f'Остаток на {date_day}.{date_month}.xlsx', sheet_name=f'Остаток на {date_day}.{date_month}')
    df = pd.read_excel(f'Остаток на 25.12.xlsx', sheet_name='Остатки 25.12') # Раскоментить при запуске

    # forecast = pd.read_excel(f'Остаток на {date_day}.{date_month}.xlsx', sheet_name=f'прогноз м1')
    forecast = pd.read_excel(f'Остаток на 25.12.xlsx', sheet_name='прогноз м1') # Раскоментить при запуске

    glay = pd.DataFrame(columns = df.columns)


    # Добавляет столбцы на основе фабричного прогноза
    tuple_glay = [['признак основной', 'канал сбыта'], ['Brand SKU', 'Brand'], ['прогноз на месяц', f'Прогноз 2023 {months_abb[date_month]}'],
                ['цех', 'цех'], ['Линия производства с приоритета1', 'Линия производства с приоритета1'], 
                ['взаимозаменяемость линии', 'взаимозаменяемость линии'], ['площадка производства', 'Площадка']]

    for i in tuple_glay:
        glay[i[0]] = forecast[i[1]]

    glay = glay[glay['прогноз на месяц'].notna()]
    glay = glay[glay['прогноз на месяц'] != 0]

    # Удаляет остатки из фабричного прогноза
    df = df[df['признак доп'].notna()]

    # print(glay)
    

def integrate():
    # Создание файлов для дальнейшей работы
    startP = time()
    global sales
    global remnant
    global now_date

    # with pd.ExcelWriter(f'{link_to_repos}\\Остаток на {now_date}.xlsx', mode='a', if_sheet_exists='new') as excel_writer:    
    remnant.to_excel(f'{link_to_repos}\\Remnant.xlsx', sheet_name=f'Остатки {now_date}', index=False)
    sales.to_excel(f'{link_to_repos}\\Sales.xlsx', sheet_name=f'Продажи {now_date}', index=False)

    print('программа выполнялась ' + str(time() - startP))


def start_all():
    # Запуск всех функций
    startP = time()
    create_time()
    copy_files()
    copy_edit()
    filling_cells_rem()
    filling_cells_sales()
    append_tables()
    normals()
    integrate()
    print('программа выполнялась ' + str(time() - startP))


if __name__ == "__main__":
    main()

# У Насти в сводке есть макрос по обновлению сводных таблиц, Викли репорт выгрузка из 1с
