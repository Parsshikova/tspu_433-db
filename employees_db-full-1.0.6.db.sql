   --Получить список всех сотрудников с их именами и фамилиями, работающих в определенном департаменте
    SELECT first_name, last_name FROM employees WHERE emp_no = 3;
    --Найти всех сотрудников, чья дата найма позже 1 января 2020 года:
    SELECT * FROM employees WHERE hire_date > '2020-01-01';
   --Выбрать 10 самых высокооплачиваемых сотрудников
    SELECT first_name, last_name, salary FROM employees JOIN salaries ON employees.emp_no = salaries.emp_no ORDER BY salary DESC LIMIT 10;
   --Посчитать количество сотрудников в каждом департаменте
    SELECT emp_no, COUNT(*) AS employee_count FROM employees GROUP BY emp_no;
    --Получить список сотрудников, у которых фамилия начинается на букву "S"
    SELECT * FROM employees WHERE last_name LIKE 'S%';
    --Найти сотрудников, чья зарплата выше средней зарплаты по всем сотрудникам:
    SELECT * FROM employees WHERE emp_no IN (SELECT emp_no FROM salaries WHERE salary > (SELECT AVG(salary) FROM salaries));      
    
   