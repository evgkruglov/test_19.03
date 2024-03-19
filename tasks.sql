-- Необходимо написать запрос, который выводит все записи по сотрудникам, родившимся в
-- 1977 - 1983 годах
SELECT *
FROM SOTR
WHERE strftime('%Y', birth_date) BETWEEN '1977' AND '1983';

-- Написать запрос, который выводит содержимое таблицы SOTR по сотрудникам, у
-- которых пол – женский.
SELECT *
FROM SOTR
WHERE sex = 'W';

-- Написать запрос, который из таблиц SOTR и ZARP выводит информацию по сотруднику
-- Имя сотрудника; Адрес; Зарплата
SELECT s.name, s.address, z.zarp
FROM SOTR s
JOIN ZARP z ON s.name = z.name
WHERE s.name = ''


-- Написать запрос, который из таблиц SOTR и ZARP выводит следующую информацию:
-- Имя сотрудника; Адрес; Зарплата
-- Примечание. Если по одному из сотрудников зарплата не указана, то в результирующей
-- выборке в поле Зарплата указывать 0
SELECT s.name AS name,
       s.address AS address,
       COALESCE(z.zarp, 0) AS zarp
FROM SOTR s
JOIN ZARP z ON s.name = z.name

-- Написать запрос, который из таблиц SOTR и PAYMENTS выводит следующую
-- информацию:
-- Имя сотрудника; Общая выплаченная сумма
-- Примечание. Если по одному из сотрудников не было выплат, то в поле с общей
-- выплаченной суммой указывать 0
SELECT name, COALESCE(SUM(amount), 0) AS total_amount
FROM PAYMENTS
GROUP BY name;