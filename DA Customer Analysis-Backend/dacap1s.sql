select *from ['Customer Data 1$'];
select *from ['Customer Data 2$'];
---Inner Join on email.
select *from ['Customer Data 1$']
INNER JOIN ['Customer Data 2$']
ON ['Customer Data 2$'].[Customer Email]=['Customer Data 1$'].Email;
---Customers who have not made a Purchase last year.
SELECT
    ['Customer Data 1$'].Name,

    ['Customer Data 1$'].Email[dbo]
FROM
    ['Customer Data 1$']
LEFT JOIN
    ['Customer Data 2$']ON ['Customer Data 1$'].Email = ['Customer Data 2$'].[Customer Email]
WHERE
 --['Customer Data 2$'].[Purchases Count] IS NULL
     ['Customer Data 2$'].[Purchases Count] < DATEADD(YEAR, -1, GETDATE());
--Total Number of  Customers
SELECT COUNT(*) AS total_customers FROM [dbo].['Customer Data 1$'] , [dbo].['Customer Data 2$'];
--Total Spent by ALL Customers
SELECT SUM([Total Spent]) AS total_revenue FROM [dbo].['Customer Data 1$'],[dbo].['Customer Data 2$'];
--Average age of Customer
SELECT AVG(age) AS average_age FROM[dbo].['Customer Data 1$'] ;
---Oldest and Youngest Customer Age
SELECT MIN(c1.age) AS youngest_customer, MAX(c1.age) AS oldest_customer FROM [dbo].['Customer Data 1$'] c1
RIGHT JOIN [dbo].['Customer Data 2$'] c2
ON c1.[Email] = c2.[Customer Email] GROUP BY c1.[Customer Since];
--Total Purchases Made
SELECT SUM(c1.[Total Purchases]) AS total_purchases FROM [dbo].['Customer Data 1$'] c1
LEFT JOIN [dbo].['Customer Data 2$'] c2 ON c1.Name=c2.[Customer Name] ;
---Gender wise Total Spending
SELECT 
  c1.[Gender],
    SUM(c1.[Total Spent] + COALESCE(c2.[Amount Spent], 0)) AS total_spent_by_gender
FROM 
   [dbo].['Customer Data 1$']  c1
LEFT JOIN 
  [dbo].['Customer Data 2$']   c2 
ON 
    c1.email = c2.[Customer Email]
GROUP BY 
    c1.gender;
--Total Customer Count
SELECT 
    COUNT(DISTINCT c1.[Email]) AS total_customers
FROM 
   [dbo].['Customer Data 1$']  c1
LEFT JOIN 
    [dbo].['Customer Data 2$'] c2 
ON 
    c1.email = c2.[Customer Email];
--Total Purchase by each Customer
SELECT 
    c1.name AS customer_name,
    c1.email AS customer_email,
    c1.age AS age,
    c1.gender AS gender,
    (c1. [Total Purchases]+ COALESCE(c2.[Purchases Count], 0)) AS combined_total_purchases,
    (c1. [Total Spent]+ COALESCE(c2.[Amount Spent], 0)) AS combined_total_spent
FROM 
  [dbo].['Customer Data 1$']  c1
LEFT JOIN 
   [dbo].['Customer Data 2$']  c2 
ON 
    c1.email = c2.[Customer Email];













