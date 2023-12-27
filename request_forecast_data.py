import datetime as dtm
from calendar import monthrange
import os

from dateutil.relativedelta import relativedelta
from com_1c import CManager
from com_1c.util import get_month_start, get_month_end, get_today, pywin_to_dt
from com_1c.c_util import torg_1c_sales_confictionary_filter

import numpy as np
import pandas as pd

# Выгрузка в мае 2020 заняла 9700 секунд.
Q_OUT_SALES = """ВЫБРАТЬ
	УзлыПодключений.Наименование КАК Firm,
	УзлыПодключений.ГруппаДистрибьюторов.Код КАК Distributor_code,
	УзлыПодключений.ГруппаДистрибьюторов.Наименование КАК Distributor,
	ПродажиОбороты.Номенклатура.НоменклатураТорг.Product.BrandSKU.Код КАК Brand_code,
	ПродажиОбороты.Номенклатура.НоменклатураТорг.ТипФасовки КАК Tip_fas,
	НАЧАЛОПЕРИОДА(ПродажиОбороты.Период, МЕСЯЦ) КАК Month,
	СУММА(ПродажиОбороты.КоличествоОборот * ПродажиОбороты.Номенклатура.ЕдиницаХраненияОстатков.Вес) КАК Sales_kg
ИЗ
	РегистрНакопления.Продажи.Обороты(
		&НачалоПериода, &КонецПериода, Регистратор,
		НЕ ДокументПродажи.Грузополучатель.Субдистрибьютор
	) КАК ПродажиОбороты
		ЛЕВОЕ СОЕДИНЕНИЕ Справочник.УзлыПодключений КАК УзлыПодключений
		ПО (ПОДСТРОКА(ПродажиОбороты.Номенклатура.Код, 1, 3) = ПОДСТРОКА(УзлыПодключений.Обозначение, 1, 3))
			И (ПОДСТРОКА(ПродажиОбороты.ДокументПродажи.Грузополучатель.Код, 1, 3) = ПОДСТРОКА(УзлыПодключений.Обозначение, 1, 3))
ГДЕ
УзлыПодключений.Ссылка.Активность

СГРУППИРОВАТЬ ПО
	НАЧАЛОПЕРИОДА(ПродажиОбороты.Период, МЕСЯЦ),
	ПродажиОбороты.Номенклатура.НоменклатураТорг.ТипФасовки,
	ПродажиОбороты.Номенклатура.НоменклатураТорг.Product.BrandSKU.Код,
	УзлыПодключений.Наименование,
	УзлыПодключений.ГруппаДистрибьюторов.Код,
	УзлыПодключений.ГруппаДистрибьюторов.Наименование"""
	# И УзлыПодключений.Ссылка.Наименование ПОДОБНО "Роскондитер"

Q_OUT_SALES_FIELDS = ('Firm', 'Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas', 'Month', 'Sales_kg')


TEMP_FOLDER = 'temp'
OUTPUT_FOLDER = 'output'
FULL_OUTPUT_FOLDER = OUTPUT_FOLDER

def download_out_sales(CURRENT_YEAR, CURRENT_MONTH):
	c = CManager(db_name='crm')
	parameters = {
		'НачалоПериода': get_month_start(CURRENT_YEAR-2, CURRENT_MONTH), # year - 2
		'КонецПериода': get_month_end(CURRENT_YEAR, CURRENT_MONTH)
	}

	sales_query = c.query(Q_OUT_SALES, Q_OUT_SALES_FIELDS, parameters=parameters, formats_dict={'Month': pywin_to_dt})
	sales_query.save_as_xlsx(f'{FULL_TEMP_FOLDER}/forecast_out_sales.xlsx')

	sales_df = sales_query.dataframe
	# Убираем уникальные коды CRM
	sales_df.loc[sales_df['Distributor_code']=='C962К', 'Distributor_code'] = 'C962'
	sales_df.loc[sales_df['Distributor']=='КОРОБОВ ВАЛЕРИЙ ЮРЬЕВИЧ ИП (Курск)', 'Distributor'] = 'КОРОБОВ ВАЛЕРИЙ ЮРЬЕВИЧ ИП'
	# Корс-Трейд Барнаул
	sales_df.loc[sales_df['Distributor_code']=='C2506Б', 'Distributor_code'] = 'C2506'
	sales_df.loc[sales_df['Distributor']=='КОРС ТРЕЙД (Барнаул)', 'Distributor'] = 'КОРС ТРЕЙД'
	# Райнер Якутия
	sales_df.loc[sales_df['Distributor_code']=='18629Я', 'Distributor_code'] = '18629'
	sales_df.loc[sales_df['Distributor']=='Райнер (Якутия)', 'Distributor'] = 'Райнер'
	# Райнер Хабаровск
	sales_df.loc[sales_df['Distributor_code']=='18629Х', 'Distributor_code'] = '18629'
	sales_df.loc[sales_df['Distributor']=='Райнер (Хабаровск)', 'Distributor'] = 'Райнер'
	# НТК Сибирь Кемерово
	sales_df.loc[sales_df['Distributor_code']=='С460', 'Distributor_code'] = 'С275'
	sales_df.loc[sales_df['Distributor']=='НТК Сибирь Кемерово', 'Distributor'] = 'НТК Сибирь Новосибирск'
	# НТК Сибирь Томск
	sales_df.loc[sales_df['Distributor_code']=='9409', 'Distributor_code'] = 'С275'
	sales_df.loc[sales_df['Distributor']=='НТК Сибирь Томск', 'Distributor'] = 'НТК Сибирь Новосибирск'

	sales_df = sales_df.fillna(0)
	sales_df = sales_df.pivot_table(
		index=['Firm', 'Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas'],
		columns=['Month'],
		values=['Sales_kg'],
		aggfunc=np.sum
	)
	sales_df.columns = sales_df.columns.droplevel()
	sales_df = sales_df.reset_index()


	sales_df.to_excel(f'{FULL_OUTPUT_FOLDER}/Forecast OUT.xlsx', index=False)



Q_IN_SALES = """ВЫБРАТЬ
	Distributor_code,
	Distributor,
	Brand_code,
	Tip_fas,
	Month,
	СУММА(Sales_kg)
ИЗ 	
(
	ВЫБРАТЬ
		Контрагенты.ГруппаДистрибьютеров.Код КАК Distributor_code,
		Контрагенты.ГруппаДистрибьютеров.Наименование КАК Distributor,
		ЗакупкиОбороты.Номенклатура.Product.BrandSKU.Код КАК Brand_code,
		ЗакупкиОбороты.Номенклатура.ТипФасовки КАК Tip_fas,
		НАЧАЛОПЕРИОДА(ЗакупкиОбороты.Период, МЕСЯЦ) КАК Month,
		-СУММА(ЗакупкиОбороты.КоличествоОборот * ЗакупкиОбороты.Номенклатура.ЕдиницаХраненияОстатков.Вес) КАК Sales_kg
	ИЗ
		РегистрНакопления.Закупки.Обороты(
				&НачалоПериода,
				&КонецПериода,
				Регистратор,
				НЕ Номенклатура.Услуга
					И НЕ ДоговорКонтрагента.Наименование ПОДОБНО "%рек%"
					// 00102, 00023, 00134, 00101; ЕСТЬ NULL - для Ульяновска
					И (НЕ ДокументЗакупки.НеУчитыватьВиртуальныйСклад ИЛИ ДокументЗакупки.СкладОрдер ЕСТЬ NULL)
					// У0001, С0001, ТВ001, К4059, У0006, КЭ13, ПР0000167
					И НЕ Номенклатура В ИЕРАРХИИ (&НоменклатураИсключения)) КАК ЗакупкиОбороты
			ЛЕВОЕ СОЕДИНЕНИЕ Справочник.Контрагенты КАК Контрагенты
			ПО ЗакупкиОбороты.ДоговорКонтрагента.Владелец = Контрагенты.Ссылка
	ГДЕ
		НЕ Контрагенты.ГруппаДистрибьютеров В (&ДистрибьюторыИсключения) //4502
		И НЕ Контрагенты.ФТТ
		И Контрагенты.КаналСбытаГлавный <> "Сети"

	СГРУППИРОВАТЬ ПО
		Контрагенты.ГруппаДистрибьютеров.Код,
		Контрагенты.ГруппаДистрибьютеров.Наименование,
		ЗакупкиОбороты.Номенклатура.Product.BrandSKU.Код,
		ЗакупкиОбороты.Номенклатура.ТипФасовки,
		НАЧАЛОПЕРИОДА(ЗакупкиОбороты.Период, МЕСЯЦ)

	ОБЪЕДИНИТЬ ВСЕ // а не ОБЪЕДИНИТЬ, иначе удалятся дубликаты

	ВЫБРАТЬ
		Контрагенты.ГруппаДистрибьютеров.Код КАК Distributor_code,
		Контрагенты.ГруппаДистрибьютеров.Наименование КАК Distributor,
		ПродажиОбороты.Номенклатура.Product.BrandSKU.Код КАК Brand_code,
		ПродажиОбороты.Номенклатура.ТипФасовки КАК Tip_fas,
		НАЧАЛОПЕРИОДА(ПродажиОбороты.Период, МЕСЯЦ) КАК Month,
		СУММА(ПродажиОбороты.КоличествоОборот * ПродажиОбороты.Номенклатура.ЕдиницаХраненияОстатков.Вес) КАК Sales_kg
	ИЗ
		РегистрНакопления.Продажи.Обороты(
				&НачалоПериода,
				&КонецПериода,
				Регистратор,
				НЕ Номенклатура.Услуга
					И НЕ ДоговорКонтрагента.Наименование ПОДОБНО "%рек%"
					// ЕСТЬ NULL - для Ульяновска
					И (НЕ ДокументПродажи.НеУчитыватьВиртуальныйСклад ИЛИ ДокументПродажи.Склад ЕСТЬ NULL)
					// У0001, С0001, ТВ001, К4059, У0006, КЭ13, ПР0000167
					И НЕ Номенклатура В ИЕРАРХИИ (&НоменклатураИсключения)) КАК ПродажиОбороты
			ЛЕВОЕ СОЕДИНЕНИЕ Справочник.Контрагенты КАК Контрагенты
			ПО (ВЫБОР
                   КОГДА (ПродажиОбороты.ДоговорКонтрагента.ВидДоговора = ЗНАЧЕНИЕ(Перечисление.ВидыДоговоровКонтрагентов.СКомиссионером)
                       И ПродажиОбороты.ДокументПродажи.Грузополучатель.КаналСбыта = "Прямые продажи")
                       ТОГДА ПродажиОбороты.ДокументПродажи.Грузополучатель
					КОГДА ПродажиОбороты.ДокументПродажи.Грузополучатель.УчитыватьДляПрогноза = ИСТИНА
						ТОГДА ПродажиОбороты.ДокументПродажи.Грузополучатель
					ИНАЧЕ ПродажиОбороты.ДоговорКонтрагента.Владелец
				КОНЕЦ = Контрагенты.Ссылка)
	ГДЕ
		НЕ Контрагенты.ГруппаДистрибьютеров В (&ДистрибьюторыИсключения) //4502
		И НЕ Контрагенты.ФТТ
		И Контрагенты.КаналСбытаГлавный <> "Сети"

	СГРУППИРОВАТЬ ПО
		Контрагенты.ГруппаДистрибьютеров.Код,
		Контрагенты.ГруппаДистрибьютеров.Наименование,
		ПродажиОбороты.Номенклатура.Product.BrandSKU.Код,
		ПродажиОбороты.Номенклатура.ТипФасовки,
		НАЧАЛОПЕРИОДА(ПродажиОбороты.Период, МЕСЯЦ)
) КАК ОбщийЗапрос

СГРУППИРОВАТЬ ПО
	Distributor_code,
	Distributor,
	Brand_code,
	Tip_fas,
	Month
"""

Q_IN_SALES_FIELDS = ('Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas', 'Month', 'Sales_kg')

def download_sales_in(CURRENT_YEAR, CURRENT_MONTH):
	c = CManager(db_name='torg')
	parameters = {
		'НачалоПериода':  get_month_start(CURRENT_YEAR-1, CURRENT_MONTH) - relativedelta(months=1),
		'КонецПериода': min(get_month_end(CURRENT_YEAR, CURRENT_MONTH), get_today()-dtm.timedelta(seconds=1))
	}
	parameters.update(torg_1c_sales_confictionary_filter(c))
	sales_query = c.query(Q_IN_SALES, Q_IN_SALES_FIELDS, parameters=parameters, formats_dict={'Month': pywin_to_dt, 'Start_date':pywin_to_dt, 'End_date':pywin_to_dt})
	sales_query.save_as_xlsx(f'{FULL_TEMP_FOLDER}/forecast_in_sales.xlsx')

	sales_df = sales_query.dataframe

	# НТК Сибирь Кемерово
	sales_df.loc[sales_df['Distributor_code']=='С460', 'Distributor_code'] = 'С275'
	sales_df.loc[sales_df['Distributor']=='НТК Сибирь Кемерово', 'Distributor'] = 'НТК Сибирь Новосибирск'
	# НТК Сибирь Томск
	sales_df.loc[sales_df['Distributor_code']=='9409', 'Distributor_code'] = 'С275'
	sales_df.loc[sales_df['Distributor']=='НТК Сибирь Томск', 'Distributor'] = 'НТК Сибирь Новосибирск'

	sales_df = sales_df.fillna(0)
	sales_df = sales_df.pivot_table(
		index=['Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas'],
		columns=['Month'],
		values=['Sales_kg'],
		aggfunc=np.sum
	)
	sales_df.columns = sales_df.columns.droplevel()
	sales_df = sales_df.reset_index()


	sales_df.to_excel(f'{FULL_OUTPUT_FOLDER}/Forecast IN.xlsx', index=False)


Q_IN_FTT_SALES = """ВЫБРАТЬ
	Client,
	Client_code,
	Distributor_code,
	Distributor,
	Brand_code,
	Tip_fas,
	Month,
	СУММА(Sales_kg)
ИЗ 	
(
	ВЫБРАТЬ
		Контрагенты.Ссылка.Наименование КАК Client,
		Контрагенты.Код как Client_code,
		Контрагенты.ГруппаДистрибьютеров.Код КАК Distributor_code,
		Контрагенты.ГруппаДистрибьютеров.Наименование КАК Distributor,
		ЗакупкиОбороты.Номенклатура.Product.BrandSKU.Код КАК Brand_code,
		ЗакупкиОбороты.Номенклатура.ТипФасовки КАК Tip_fas,
		НАЧАЛОПЕРИОДА(ЗакупкиОбороты.Период, МЕСЯЦ) КАК Month,
		-СУММА(ЗакупкиОбороты.КоличествоОборот * ЗакупкиОбороты.Номенклатура.ЕдиницаХраненияОстатков.Вес) КАК Sales_kg
	ИЗ
		РегистрНакопления.Закупки.Обороты(
				&НачалоПериода,
				&КонецПериода,
				Регистратор,
				НЕ Номенклатура.Услуга
					И НЕ ДоговорКонтрагента.Наименование ПОДОБНО "%рек%"
					// 00102, 00023, 00134, 00101; ЕСТЬ NULL - для Ульяновска
					И (НЕ ДокументЗакупки.НеУчитыватьВиртуальныйСклад ИЛИ ДокументЗакупки.СкладОрдер ЕСТЬ NULL)
					// У0001, С0001, ТВ001, К4059, У0006, КЭ13, ПР0000167
					И НЕ Номенклатура В ИЕРАРХИИ (&НоменклатураИсключения)) КАК ЗакупкиОбороты
			ЛЕВОЕ СОЕДИНЕНИЕ Справочник.Контрагенты КАК Контрагенты
			ПО ЗакупкиОбороты.ДоговорКонтрагента.Владелец = Контрагенты.Ссылка
	ГДЕ
		НЕ Контрагенты.ГруппаДистрибьютеров В (&ДистрибьюторыИсключения) //4502
		И Контрагенты.ФТТ
		
	СГРУППИРОВАТЬ ПО
		Контрагенты.Ссылка,
		Контрагенты.ГруппаДистрибьютеров.Код,
		Контрагенты.ГруппаДистрибьютеров.Наименование,
		ЗакупкиОбороты.Номенклатура.Product.BrandSKU.Код,
		ЗакупкиОбороты.Номенклатура.ТипФасовки,
		НАЧАЛОПЕРИОДА(ЗакупкиОбороты.Период, МЕСЯЦ)

	ОБЪЕДИНИТЬ ВСЕ // а не ОБЪЕДИНИТЬ, иначе удалятся дубликаты

	ВЫБРАТЬ
		Контрагенты.Ссылка.Наименование КАК Client,
		Контрагенты.Код КАК Client_code,
		Контрагенты.ГруппаДистрибьютеров.Код КАК Distributor_code,
		Контрагенты.ГруппаДистрибьютеров.Наименование КАК Distributor,
		ПродажиОбороты.Номенклатура.Product.BrandSKU.Код КАК Brand_code,
		ПродажиОбороты.Номенклатура.ТипФасовки КАК Tip_fas,
		НАЧАЛОПЕРИОДА(ПродажиОбороты.Период, МЕСЯЦ) КАК Month,
		СУММА(ПродажиОбороты.КоличествоОборот * ПродажиОбороты.Номенклатура.ЕдиницаХраненияОстатков.Вес) КАК Sales_kg
	ИЗ
		РегистрНакопления.Продажи.Обороты(
				&НачалоПериода,
				&КонецПериода,
				Регистратор,
				НЕ Номенклатура.Услуга
					И НЕ ДоговорКонтрагента.Наименование ПОДОБНО "%рек%"
					// ЕСТЬ NULL - для Ульяновска
					И (НЕ ДокументПродажи.НеУчитыватьВиртуальныйСклад ИЛИ ДокументПродажи.Склад ЕСТЬ NULL)
					// У0001, С0001, ТВ001, К4059, У0006, КЭ13, ПР0000167
					И НЕ Номенклатура В ИЕРАРХИИ (&НоменклатураИсключения)) КАК ПродажиОбороты
			ЛЕВОЕ СОЕДИНЕНИЕ Справочник.Контрагенты КАК Контрагенты
			ПО (ВЫБОР
                   КОГДА (ПродажиОбороты.ДоговорКонтрагента.ВидДоговора = ЗНАЧЕНИЕ(Перечисление.ВидыДоговоровКонтрагентов.СКомиссионером)
                       И ПродажиОбороты.ДокументПродажи.Грузополучатель.КаналСбыта = "Прямые продажи")
                       ТОГДА ПродажиОбороты.ДокументПродажи.Грузополучатель
					КОГДА ПродажиОбороты.ДокументПродажи.Грузополучатель.УчитыватьДляПрогноза = ИСТИНА
						ТОГДА ПродажиОбороты.ДокументПродажи.Грузополучатель
					ИНАЧЕ ПродажиОбороты.ДоговорКонтрагента.Владелец
				КОНЕЦ = Контрагенты.Ссылка)
	ГДЕ
		НЕ Контрагенты.ГруппаДистрибьютеров В (&ДистрибьюторыИсключения) //4502
		И Контрагенты.ФТТ

	СГРУППИРОВАТЬ ПО
		Контрагенты.Ссылка,
		Контрагенты.ГруппаДистрибьютеров.Код,
		Контрагенты.ГруппаДистрибьютеров.Наименование,
		ПродажиОбороты.Номенклатура.Product.BrandSKU.Код,
		ПродажиОбороты.Номенклатура.ТипФасовки,
		НАЧАЛОПЕРИОДА(ПродажиОбороты.Период, МЕСЯЦ)
) КАК ОбщийЗапрос
СГРУППИРОВАТЬ ПО
	Client,
	Client_code,
	Distributor_code,
	Distributor,
	Brand_code,
	Tip_fas,
	Month
"""

Q_IN_FTT_SALES_FIELDS = ('Client', 'Client_code', 'Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas', 'Month', 'Sales_kg')

def download_sales_in_ftt(CURRENT_YEAR, CURRENT_MONTH):
	c = CManager(db_name='torg')
	parameters = {
		'НачалоПериода': get_month_start(CURRENT_YEAR-1, CURRENT_MONTH) - relativedelta(months=1),
		'КонецПериода': min(get_month_end(CURRENT_YEAR, CURRENT_MONTH), get_today()-dtm.timedelta(seconds=1))
	}
	parameters.update(torg_1c_sales_confictionary_filter(c))
	sales_query = c.query(Q_IN_FTT_SALES, Q_IN_FTT_SALES_FIELDS, parameters=parameters, formats_dict={'Month': pywin_to_dt, 'Start_date':pywin_to_dt, 'End_date':pywin_to_dt})
	sales_query.save_as_xlsx(f'{FULL_TEMP_FOLDER}/forecast_in_ftt_sales.xlsx')

	sales_df = sales_query.dataframe
	sales_df = sales_df.fillna(0)
	sales_df = sales_df.pivot_table(
		index=['Client', 'Client_code', 'Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas'],
		columns=['Month'],
		values=['Sales_kg'],
		aggfunc=np.sum
	)
	sales_df.columns = sales_df.columns.droplevel()
	sales_df = sales_df.reset_index()


	sales_df.to_excel(f'{FULL_OUTPUT_FOLDER}/Forecast IN FTT.xlsx', index=False)

Q_OUT_STOCK = """
	ВЫБРАТЬ
		УзлыПодключений.Наименование КАК Firm,
		УзлыПодключений.ГруппаДистрибьюторов.Код КАК Distributor_code,
		УзлыПодключений.ГруппаДистрибьюторов.Наименование КАК Distributor,
		ТоварыНаСкладахОстаткиИОбороты.Номенклатура.НоменклатураТорг.Product.BrandSKU.Код КАК Brand_code,
		ТоварыНаСкладахОстаткиИОбороты.Номенклатура.НоменклатураТорг.ТипФасовки КАК Tip_fas,
		&КонецПериода КАК Stock_date,
		СУММА(ТоварыНаСкладахОстаткиИОбороты.КоличествоКонечныйОстаток * ТоварыНаСкладахОстаткиИОбороты.Номенклатура.ЕдиницаХраненияОстатков.Вес) КАК Stock_kg
	ИЗ
		РегистрНакопления.ТоварыНаСкладах.ОстаткиИОбороты(
				&НачалоПериода, &КонецПериода, , , 
			) КАК ТоварыНаСкладахОстаткиИОбороты
			ВНУТРЕННЕЕ СОЕДИНЕНИЕ Справочник.УзлыПодключений КАК УзлыПодключений
			ПО (ПОДСТРОКА(ТоварыНаСкладахОстаткиИОбороты.Номенклатура.Код, 1, 3) = ПОДСТРОКА(УзлыПодключений.Обозначение, 1, 3))

	ГДЕ
		УзлыПодключений.Активность
		И ТоварыНаСкладахОстаткиИОбороты.КоличествоКонечныйОстаток > 0

	СГРУППИРОВАТЬ ПО
		УзлыПодключений.Наименование,
		УзлыПодключений.ГруппаДистрибьюторов.Код,
		УзлыПодключений.ГруппаДистрибьюторов.Наименование,
		ТоварыНаСкладахОстаткиИОбороты.Номенклатура.НоменклатураТорг.Product.BrandSKU.Код,
		ТоварыНаСкладахОстаткиИОбороты.Номенклатура.НоменклатураТорг.ТипФасовки
"""

Q_OUT_STOCK_FIELDS = ('Firm', 'Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas', 'Stock_date', 'Stock_kg')

def download_out_stock(CURRENT_YEAR, CURRENT_MONTH):
	c = CManager(db_name='crm')
	parameters = {
		'НачалоПериода': get_today(),
		'КонецПериода': get_today()
	}

	stock_query = c.query(Q_OUT_STOCK, Q_OUT_STOCK_FIELDS, parameters=parameters, formats_dict={'Stock_date': pywin_to_dt})
	stock_query.save_as_xlsx(f'{FULL_TEMP_FOLDER}/forecast_stock.xlsx')

	sales_df = stock_query.dataframe
	sales_df['Stock_date'] = get_month_start(CURRENT_YEAR, CURRENT_MONTH, tz='naive')

	# Убираем уникальные коды CRM
	# Коробов Курск
	sales_df.loc[sales_df['Distributor_code']=='C962К', 'Distributor_code'] = 'C962'
	sales_df.loc[sales_df['Distributor']=='КОРОБОВ ВАЛЕРИЙ ЮРЬЕВИЧ ИП (Курск)', 'Distributor'] = 'КОРОБОВ ВАЛЕРИЙ ЮРЬЕВИЧ ИП'
	# Корс-Трейд Барнаул
	sales_df.loc[sales_df['Distributor_code']=='C2506Б', 'Distributor_code'] = 'C2506'
	sales_df.loc[sales_df['Distributor']=='КОРС ТРЕЙД (Барнаул)', 'Distributor'] = 'КОРС ТРЕЙД'
	# Райнер Якутия
	sales_df.loc[sales_df['Distributor_code']=='18629Я', 'Distributor_code'] = '18629'
	sales_df.loc[sales_df['Distributor']=='Райнер (Якутия)', 'Distributor'] = 'Райнер'
	# Райнер Хабаровск
	sales_df.loc[sales_df['Distributor_code']=='18629Х', 'Distributor_code'] = '18629'
	sales_df.loc[sales_df['Distributor']=='Райнер (Хабаровск)', 'Distributor'] = 'Райнер'
	# НТК Сибирь Кемерово
	sales_df.loc[sales_df['Distributor_code']=='С460', 'Distributor_code'] = 'С275'
	sales_df.loc[sales_df['Distributor']=='НТК Сибирь Кемерово', 'Distributor'] = 'НТК Сибирь Новосибирск'
	# НТК Сибирь Томск
	sales_df.loc[sales_df['Distributor_code']=='9409', 'Distributor_code'] = 'С275'
	sales_df.loc[sales_df['Distributor']=='НТК Сибирь Томск', 'Distributor'] = 'НТК Сибирь Новосибирск'

	sales_df = sales_df.fillna(0)
	sales_df = sales_df.pivot_table(
		index=['Firm', 'Distributor_code', 'Distributor', 'Brand_code', 'Tip_fas'],
		columns=['Stock_date'],
		values=['Stock_kg'],
		aggfunc=np.sum
	)
	sales_df.columns = sales_df.columns.droplevel()
	sales_df = sales_df.reset_index()

	sales_df.to_excel(f'{FULL_OUTPUT_FOLDER}/Forecast STOCK.xlsx', index=False)

def aggregate():
	in_df = pd.read_excel(f'{FULL_OUTPUT_FOLDER}/Forecast IN.xlsx')
	in_ftt_df = pd.read_excel(f'{FULL_OUTPUT_FOLDER}/Forecast IN FTT.xlsx')
	out_df = pd.read_excel(f'{FULL_OUTPUT_FOLDER}/Forecast OUT.xlsx')
	stock_df = pd.read_excel(f'{FULL_OUTPUT_FOLDER}/Forecast STOCK.xlsx')

	in_df['source'] = 'IN'
	in_ftt_df['source'] = 'IN'
	out_df['source'] = 'OUT'
	stock_df['source'] = 'STOCK'

	final_df = pd.concat([in_df, in_ftt_df, out_df, stock_df])
	final_df = final_df.melt(
		id_vars=['source', 'Client', 'Client_code', 'Firm', 'Distributor', 'Distributor_code', 'Brand_code', 'Tip_fas'], 
		var_name='date')
	final_df.sort_values(by=['source', 'date'], ascending=False, inplace=True)

	final_df.fillna(0, inplace=True)
	final_df = pd.pivot_table(
		final_df,
		index=['Client', 'Client_code', 'Firm', 'Distributor', 'Distributor_code', 'Brand_code', 'Tip_fas'],
		columns=['source', 'date'],
		values=['value'],
		aggfunc=np.sum

	)
	final_df.sort_index(axis=1, level=['date'], ascending=True, inplace=True) # sort date in descending order
	# final_df.sort_index(axis=1, level=['source'], ascending=True, inplace=True, sort_remaining=False) # sortsource in ascending order
	final_df = final_df.reindex(['IN', 'OUT', 'STOCK'], axis=1, level=1) # rearrange columns as you please
	# final_df.reset_index(0, inplace=True)
	stock_columns_sums = final_df.xs(('value', 'STOCK'), level=0, axis=1).sum()
	stock_columns_drop = stock_columns_sums[stock_columns_sums <= 0].index

	columns_to_drop = [('value', 'STOCK', t) for t in stock_columns_drop]
	final_df.drop(columns_to_drop, axis=1, inplace=True)
	final_df.to_csv(f'{FULL_OUTPUT_FOLDER}/Forecast agregated.csv', encoding='cp1251', sep=';') # для 2 месяцев заняло 4 минуты

if __name__ == '__main__':
	# текущий месяц, т.е. месяц, когда формируются бланки прогнозов
	# y, m = 2021, 7 
	y, m = dtm.datetime.now().year, dtm.datetime.now().month

	FULL_OUTPUT_FOLDER = f'{os.environ["HOMEPATH"]}/Desktop/access/forecast {str(m).zfill(2)} {y}'
	FULL_TEMP_FOLDER = f'{TEMP_FOLDER}/forecast {str(m).zfill(2)} {y}'	
	
	if not os.path.exists(FULL_OUTPUT_FOLDER):
		os.makedirs(FULL_OUTPUT_FOLDER)
	if not os.path.exists(FULL_TEMP_FOLDER):
		os.makedirs(FULL_TEMP_FOLDER)

	download_sales_in(y, m)
	download_sales_in_ftt(y, m)
	download_out_stock(y, m)
	download_out_sales(y, m)
	aggregate()