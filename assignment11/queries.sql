-- Create tables

CREATE TABLE Publisher(
	id INT PRIMARY KEY,
	name TEXT NOT NULL,
    country TEXT,
	founding_year INT
 );

INSERT INTO Publisher (id, name, country, founding_year)
VALUES
(1, "Penguin classics", "UK", 1865),
(2, "Bloomsbury", "Scotland", 1976),
(3, "McGraw Hill", "USA", 2002),
(4, "Hachette Livre", "France", 1647);

CREATE TABLE Author(
	id INT PRIMARY KEY,
	name TEXT NOT NULL,
    country TEXT,
	year_of_birth INT,
	primary_publisher_id INT NOT NULL,
	FOREIGN KEY (primary_publisher_id) REFERENCES Publisher (id)
 );

INSERT INTO Author (id, name, country, year_of_birth, primary_publisher_id)
VALUES
(1, "JK Rowling", "UK", 1965, 1),
(2, "Yuval Noah Harari", "Israel", 1976, 2),
(3, "Alexandre Dumas", "France", 1802, 4),
(4, "Stephen King", "USA", 1947, 3),
(5, "Casey McQuinston", "USA", 1990, 3);

CREATE TABLE Book(
	id INT PRIMARY KEY,
	name TEXT NOT NULL,
	first_author_id INT NOT NULL,
	second_author_id INT,
	year_of_publication INT NOT NULL,
	publisher_id INT NOT NULL,
	FOREIGN KEY (first_author_id) REFERENCES Author (id),
	FOREIGN KEY (second_author_id) REFERENCES Author (id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher (id)
 );

INSERT INTO Book (id, name, first_author_id, second_author_id, year_of_publication, publisher_id)
VALUES
(1, "Harry Potter", 1, null, 1994, 1),
(2, "Sapiens", 2, 4, 2006, 2),
(3, "Count of Monte Cristo", 3, null, 1802, 4),
(4, "Zodiac", 4, 2, 2017, 1),
(5, "Red, White and Royal Blue", 5, 1, 2020, 3);

-- end of create table queries

-- Queries:

-- 1. Count of books per each publisher
SELECT p.name AS publisher, COUNT(*) AS books
FROM Publisher p INNER JOIN Book b ON p.id = b.publisher_id
GROUP BY 1;

-- 2. Top 3 authors with most books
SELECT a.name AS author, COUNT(*) AS books
FROM Author a INNER JOIN Book b ON b.first_author_id = a.id OR b.second_author_id = a.id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 3;

-- 3. Books which are not published by the Primary Publisher of the First Author
SELECT b.name AS book
FROM Book b INNER JOIN Author a on b.first_author_id = a.id
WHERE b.publisher_id != a.primary_publisher_id;

-- 4. The country with the most books "authored".
SELECT a.country, COUNT(*) AS books_authored
FROM Author a INNER JOIN Book b ON b.first_author_id = a.id OR b.second_author_id = a.id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;

-- 5. The publisher founded after the year 2000 with the most books publiished.
SELECT p.name AS publisher
FROM Publisher p INNER JOIN Book b ON b.publisher_id = p.id
WHERE p.founding_year > 2000
GROUP BY 1
ORDER BY COUNT(*) DESC
LIMIT 1;

-- 6. Number of authors below the age of 30 from each publisher started before 1985.
SELECT p.name AS publisher, COUNT(*) AS authors
FROM Publisher p INNER JOIN Author a ON p.id  = a.primary_publisher_id
WHERE p.founding_year < 1985 AND year_of_birth > 1991

-- 7. Which authors have the most number of books together?
SELECT x.name AS author1, y.name AS author2, COUNT(*) AS books_co_authored
FROM Book b
  INNER JOIN Author x ON b.first_author_id = x.id
  INNER JOIN Author y ON b.second_author_id = y.id
WHERE b.second_author_id IS NOT NULL
  GROUP BY
	CASE
		WHEN b.first_author_id < b.second_author_id THEN b.first_author_id || '-' || b.second_author_id
		ELSE b.second_author_id || '-' || b.first_author_id
		END
ORDER BY 3 DESC
LIMIT 1;

-- 8. Number of collaborations between each pair of countries
SELECT x.country AS country1, y.country AS country2, COUNT(*) AS books_co_authored
FROM Book b
  INNER JOIN Author x ON b.first_author_id = x.id
  INNER JOIN Author y ON b.second_author_id = y.id
WHERE b.second_author_id IS NOT NULL
  GROUP BY
	CASE
		WHEN x.country < y.country THEN x.country || '-' || y.country
		ELSE y.country || '-' || x.country
		END
ORDER BY 3 DESC;
