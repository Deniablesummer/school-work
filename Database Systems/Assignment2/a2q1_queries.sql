-- CSC 370 - Spring 2018
-- Assignment 2: Queries for Question 1 (imdb)
-- Name: James Ryan
-- Student ID: V00830984

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 1x --' header before
-- each question.


-- Question 1a --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select primary_name, year, title_id from titles
	natural join primary_names
		where year = 1989 and length_minutes = 180  and title_type = 'tvSpecial';
-- Question 1b --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select primary_name, year, length_minutes from titles
	natural join primary_names
		where length_minutes >= 4320 and title_type = 'movie';
-- Question 1c --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select primary_name, year, length_minutes from titles
	natural join cast_crew
	natural join primary_names
	natural join
			(select name, person_id from people) as actor_names
		where year <= 1985 and title_type = 'movie' and name = 'Meryl Streep';
-- Question 1d --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select primary_name, year, length_minutes from titles
	natural join primary_names
	natural join title_genres
		where title_type = 'movie' and genre = 'Action'
intersect
select primary_name, year, length_minutes from titles
	natural join primary_names
	natural join title_genres
		where title_type = 'movie' and genre = 'Film-Noir';
-- Question 1e --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select name from cast_crew
	natural join titles
	natural join people
	natural join primary_names
	where title_type = 'movie' and primary_name = 'The Big Lebowski';
-- Question 1f --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select name from people
	natural join titles
	natural join primary_names
	natural join writers
	where title_type = 'movie' and primary_name = 'Die Hard'
union
select name from people
	natural join titles
	natural join primary_names
	natural join directors
	where title_type = 'movie' and primary_name = 'Die Hard';
-- Question 1g --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select primary_name, length_minutes from titles
	natural join primary_names
	natural join known_for
	natural join people
	where name = 'Tom Cruise' and title_type = 'movie';
-- Question 1h --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select primary_name, year, length_minutes from titles
	natural join primary_names
	natural join cast_crew
	natural join people
		where name = 'Meryl Streep' and title_type = 'movie'
intersect
select primary_name, year, length_minutes from titles
	natural join primary_names
	natural join cast_crew
	natural join people
		where name = 'Tom Hanks' and title_type = 'movie';
-- Question 1i --
with
	primary_names as (select title_id, name as primary_name
	 from title_names where is_primary = true)
select primary_name, year from titles
	natural join primary_names
	natural join directors
	natural join people
	natural join title_genres
	where name = 'Steven Spielberg' and genre = 'Thriller' and title_type = 'movie';