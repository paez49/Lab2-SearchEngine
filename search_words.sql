SELECT courseURL
FROM courses
WHERE word = 'TOSEARCH';

SELECT DISTINCT courseURL
FROM courses
WHERE word LIKE '%est%';

SELECT DISTINCT courseURL
FROM courses
WHERE word LIKE 'c%';