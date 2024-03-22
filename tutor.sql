-- Групповые запросы Group BY/Having: GROUP BY используется для группировки строк, которые имеют одинаковые значения в указанных столбцах. 
-- HAVING используется для фильтрации значений после выполнения GROUP BY. Например:
SELECT Department, COUNT(EmployeeID) as EmployeeCount
FROM Employees
GROUP BY Department
HAVING COUNT(EmployeeID) > 5;
 /* 
 Виды JOIN: JOIN используется для объединения строк из двух или более таблиц на основе связанного столбца между ними. Виды JOIN:
INNER JOIN: Возвращает строки, когда есть совпадение в обеих таблицах.
LEFT JOIN (или LEFT OUTER JOIN): Возвращает все строки из левой таблицы и совпадающие строки из правой таблицы.
RIGHT JOIN (или RIGHT OUTER JOIN): Возвращает все строки из правой таблицы и совпадающие строки из левой таблицы.
FULL JOIN (или FULL OUTER JOIN): Возвращает строки, когда есть совпадение в одной из таблиц.
CROSS JOIN: Возвращает комбинацию каждой строки левой таблицы с каждой строкой правой таблицы.
 */

 /* 
 Оператор UNION/UNION ALL: UNION используется для объединения результатов двух SELECT запросов. 
 Он удаляет дубликаты. UNION ALL также объединяет результаты двух SELECT запросов, но он не удаляет дубликаты.
 */
SELECT column_name(s) FROM table1
UNION
SELECT column_name(s) FROM table2;

/* 
Оператор INTERSECT: INTERSECT возвращает строки, которые совпадают в обоих SELECT запросах.
*/
SELECT column_name(s) FROM table1
INTERSECT
SELECT column_name(s) FROM table2;

/* 
Оператор EXCEPT: EXCEPT возвращает строки из первого SELECT запроса, которые не существуют во втором SELECT запросе.
*/
SELECT column_name(s) FROM table1
EXCEPT
SELECT column_name(s) FROM table2;

/* 
Подзапрос (вложенный запрос): 
Подзапрос - это запрос внутри другого запроса. Он может быть вложен в SELECT, INSERT, UPDATE или DELETE инструкции, а также в другой подзапрос. Например:
*/
SELECT EmployeeID, FirstName, LastName, Department
FROM Employees
WHERE Salary > (SELECT AVG(Salary) FROM Employees);

/* 
Работа с представлениями VIEW: VIEW - это виртуальная таблица, основанная на результате запроса. 
Она может содержать все строки и столбцы таблицы или определенные строки и столбцы таблицы. Создание представления:
*/
CREATE VIEW [IF NOT EXISTS] view_name AS
SELECT column1, column2
FROM table_name
WHERE condition;

/* 
Порядок обработки инструкции SELECT: Порядок обработки инструкции SELECT следующий:
FROM и JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT и OFFSET
*/

/* 
Create or Alter Procedure, Function: Создание и изменение процедуры:
*/
CREATE PROCEDURE MyProcedure
AS
SELECT column_name(s) FROM table_name;

ALTER PROCEDURE MyProcedure
AS
SELECT column_name(s) FROM another_table_name;

CREATE FUNCTION MyFunction (@param1 datatype, @param2 datatype)
RETURNS datatype
AS
BEGIN
   -- function body
   RETURN @result;
END;

ALTER FUNCTION MyFunction (@param1 datatype, @param2 datatype)
RETURNS datatype
AS
BEGIN
   -- new function body
   RETURN @new_result;
END;

/*
Работа с данными безопасный INSERT/UPDATE/DELETE:
 */
--  Добавление данных:
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);
-- Обновление данных:
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
-- Удаление данных:
DELETE FROM table_name WHERE condition;

-- Команды условного выполнения IF/CASE/BEGIN/END/GOTO:
IF condition
BEGIN
   -- code to be executed if condition is TRUE
END
ELSE
BEGIN
   -- code to be executed if condition is FALSE
END

-- CASE используется для выполнения различных действий на основе различных условий.
CASE
   WHEN condition1 THEN result1
   WHEN condition2 THEN result2
   ...
   ELSE result
END;

-- Циклы в T-SQL WHILE /CURSOR:

WHILE condition
BEGIN
   -- code to be executed
END

-- CURSOR используется для обработки результатов запроса по одной строке за раз.
DECLARE @MyVariable VARCHAR(255);
DECLARE MyCursor CURSOR FOR
SELECT MyColumn FROM MyTable;

OPEN MyCursor;
FETCH NEXT FROM MyCursor INTO @MyVariable;

WHILE @@FETCH_STATUS = 0
BEGIN
   PRINT @MyVariable;
   FETCH NEXT FROM MyCursor INTO @MyVariable;
END;

CLOSE MyCursor;
DEALLOCATE MyCursor;

/* 
Конструкция BEGIN TRY CATCH. Команды RAISERROR, THROW:
*/

BEGIN TRY
   -- code that might cause an error
END TRY
BEGIN CATCH
   -- code to handle the error
END CATCH

-- RaiseError
BEGIN TRY
   -- Generate a divide-by-zero error
   SELECT 1/0;
END TRY
BEGIN CATCH
   -- RAISERROR with severity 16 will be caught
   RAISERROR ('Error raised in TRY block.', -- Message text.
               16, -- Severity.
               1 -- State.
   );
END CATCH;
-- THROW используется для повторного вызова исключения, которое было перехвачено в блоке CATCH.
BEGIN TRY
   -- Generate a divide-by-zero error
   SELECT 1/0;
END TRY
BEGIN CATCH
   THROW;
END CATCH;

-- Циклы For/Do loop until/ While WEND:

FOR i = 1 TO 10
BEGIN
   -- code to be executed for each iteration
END;

-- Do until
/*
Dim counter As Integer = 0
Do Until counter = 10
   ' Code to be executed for each iteration
   counter = counter + 1
Loop
*/
-- WHILE WEND:
/*
Dim counter As Integer = 0
While counter < 10
   ' Code to be executed for each iteration
   counter = counter + 1
Wend
*/

-- Обработчик ошибок ON ERROR: В SQL Server используется конструкция TRY...CATCH для обработки ошибок:
BEGIN TRY
   -- код, который может вызвать ошибку
END TRY
BEGIN CATCH
   -- код для обработки ошибки
END CATCH

-- Уметь задавать переменные для Скрипта/процедуры:
DECLARE @MyVariable INT;
SET @MyVariable = 10;

-- Знать основные ограничения на таблицы: a. Primary/Foreign KEY: Определяют отношения между таблицами.
/* 
Primary Key (Первичный ключ):
Это уникальный идентификатор для записи в таблице.
Каждая таблица может иметь только один первичный ключ.
Первичный ключ не может содержать NULL значения.
Он обеспечивает способ уникальной идентификации каждой строки в таблице.

Foreign Key (Внешний ключ):
Это поле (или набор полей) в таблице, которое ссылается на первичный ключ другой таблицы.
Таблица может иметь несколько внешних ключей, в зависимости от ее отношений с другими таблицами.
Внешний ключ может содержать NULL значения, если только не указано иное.
Он используется для создания связи между таблицами и обеспечения целостности данных.
*/
CREATE TABLE Orders (
    OrderID int NOT NULL,
    OrderNumber int NOT NULL,
    PersonID int,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
);
-- UNIQUE: Гарантирует, что все значения в столбце уникальны.
CREATE TABLE Persons (
    ID int NOT NULL UNIQUE,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int
);
-- CHECK: Гарантирует, что все значения в столбце удовлетворяют определенному условию.
CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int CHECK (Age>=18)
);
-- DEFAULT: Устанавливает значение по умолчанию для столбца.
CREATE TABLE Orders (
    ID int NOT NULL,
    OrderNumber int NOT NULL DEFAULT 1
);

-- PRINT: Выводит сообщение.
PRINT 'Hello, World!';

-- RETURN: Завершает выполнение хранимой процедуры и возвращает значение.
CREATE PROCEDURE MyProcedure
AS
RETURN 123;

-- GOTO: Переходит к метке внутри хранимой процедуры.
GOTO MyLabel;
...
MyLabel:
PRINT 'Hello, World!';

-- WAITFOR: Приостанавливает выполнение запроса на определенное время.
WAITFOR DELAY '00:00:05';
PRINT 'Hello, World!';

/* 
Знать и использовать шаблон процедуры crtprc и crtfn. 
Понимать обработчик ошибок TRY CATCH в шаблоне: crtprc и crtfn могут быть шаблонами для создания процедур и функций в вашей конкретной среде. 
Обычно они включают в себя определенные стандарты и практики, которые следует соблюдать. 
Обработчик ошибок TRY CATCH используется для перехвата и обработки ошибок в SQL Server.
*/

/* 
Знать функционал логирования запуска процедур: 
Логирование запуска процедур обычно включает в себя запись информации о каждом запуске процедуры, включая время запуска, параметры и возможные ошибки.
*/

/* 
Знать стандарт логирования ошибок и применять его: 
Стандарт логирования ошибок обычно включает в себя запись информации об ошибках, которые происходят во время выполнения запросов или процедур.
*/

-- Транзакции BEGIN TRAN COMMIT/ROLLBACK:
-- BEGIN TRAN начинает транзакцию, COMMIT сохраняет изменения, сделанные в транзакции, а ROLLBACK отменяет изменения.
BEGIN TRAN;
-- SQL statements
IF @error = 0
   COMMIT;
ELSE
   ROLLBACK;

/* 
Понимать разницу между PROCEDURE/FUNCTION: 
PROCEDURE - это подпрограмма, которая выполняет действие, в то время как FUNCTION - это подпрограмма, которая возвращает значение.
*/
-- Процедура
CREATE PROCEDURE MyProcedure
AS
PRINT 'Hello, World!';
GO

-- Функция
CREATE FUNCTION MyFunction (@x INT, @y INT)
RETURNS INT
AS
BEGIN
   RETURN @x + @y;
END;
GO

/* 
Знать системные функции работы со строками: 
SQL Server предоставляет множество функций для работы со строками, таких как LEN, SUBSTRING, CHARINDEX, REPLACE и т.д.
*/
SELECT LEN('Hello, World!'); -- Возвращает длину строки
SELECT SUBSTRING('Hello, World!', 1, 5); -- Возвращает подстроку
SELECT CHARINDEX('o', 'Hello, World!'); -- Возвращает позицию символа в строке
SELECT REPLACE('Hello, World!', 'World', 'SQL'); -- Заменяет часть строки

/* 
Знать системные функции работы со строками: 
SQL Server предоставляет множество функций для работы со строками, таких как LEN, SUBSTRING, CHARINDEX, REPLACE и т.д.
*/
SELECT GETDATE(); -- Возвращает текущую дату и время
SELECT DATEADD(DAY, 1, GETDATE()); -- Добавляет интервал к дате
SELECT DATEDIFF(DAY, '2022-01-01', GETDATE()); -- Возвращает разницу между двумя датами
SELECT DAY(GETDATE()), MONTH(GETDATE()), YEAR(GETDATE()); -- Возвращает день, месяц и год даты

/* 
Знать системные функции работы с датами: 
SQL Server предоставляет множество функций для работы с датами, таких как GETDATE, DATEADD, DATEDIFF, DAY, MONTH, YEAR и т.д.
*/
SELECT GETDATE(); -- Возвращает текущую дату и время
SELECT DATEADD(DAY, 1, GETDATE()); -- Добавляет интервал к дате
SELECT DATEDIFF(DAY, '2022-01-01', GETDATE()); -- Возвращает разницу между двумя датами
SELECT DAY(GETDATE()), MONTH(GETDATE()), YEAR(GETDATE()); -- Возвращает день, месяц и год даты

/* 
Знать системные математические функции: 
SQL Server предоставляет множество математических функций, таких как ABS, CEILING, FLOOR, ROUND, SQRT и т.д.
*/
SELECT ABS(-1); -- Возвращает абсолютное значение числа
SELECT CEILING(1.5); -- Возвращает наименьшее целое число, которое больше или равно указанному числу
SELECT FLOOR(1.5); -- Возвращает наибольшее целое число, которое меньше или равно указанному числу
SELECT ROUND(1.5, 0); -- Округляет число до указанного количества десятичных знаков
SELECT SQRT(4); -- Возвращает квадратный корень числа


/* 
Знать агрегатные системные функции: 
SQL Server предоставляет множество агрегатных функций, таких как COUNT, SUM, AVG, MIN, MAX и т.д.
*/
SELECT COUNT(*) FROM MyTable; -- Возвращает количество строк в таблице
SELECT SUM(MyColumn) FROM MyTable; -- Возвращает сумму значений в столбце
SELECT AVG(MyColumn) FROM MyTable; -- Возвращает среднее значение столбца
SELECT MIN(MyColumn) FROM MyTable; -- Возвращает минимальное значение столбца
SELECT MAX(MyColumn) FROM MyTable; -- Возвращает максимальное значение столбца


/* 
Знать оконные функции уметь использовать (RANK/LAG/LEAD/TOP 1 WITH TIES): 
Оконные функции выполняют вычисление для набора строк, некоторым образом связанных с текущей строкой. 
Примеры включают RANK, DENSE_RANK, ROW_NUMBER, LAG, LEAD.
*/
SELECT RANK() OVER (ORDER BY MyColumn) FROM MyTable; -- Возвращает ранг каждой строки в окне
SELECT LAG(MyColumn) OVER (ORDER BY MyColumn) FROM MyTable; -- Возвращает значение предыдущей строки в окне
SELECT LEAD(MyColumn) OVER (ORDER BY MyColumn) FROM MyTable; -- Возвращает значение следующей строки в окне
SELECT TOP 1 WITH TIES MyColumn FROM MyTable ORDER BY MyColumn; -- Возвращает верхние строки, которые связаны с последней включенной строкой


/* 
Порядок обработки инструкции SELECT: Порядок обработки инструкции SELECT следующий:
FROM и JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT и OFFSET
*/

/* 
функция COALESCE существует в T-SQL. 
Она принимает список значений и возвращает первое из них, которое не равно NULL. Если все аргументы равны NULL, COALESCE возвращает NULL1.
*/
select name 
from Customer
where Coalesce(referee_id,0) <> 2
