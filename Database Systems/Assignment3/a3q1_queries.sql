-- CSC 370 - Spring 2018
-- Assignment 3: Queries for Question 1 (imdb)
-- Name: James Ryan
-- Student ID: V00830984

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 1x --' header before
-- each question.


-- Question 1a --
with
	primary_names as (select title_id, name as primary_name from title_names 
		where is_primary = true),
	ratings_years as (select rating, year, title_id from ratings
		natural join titles
		where votes >= 10000 and title_type = 'movie'),
	max_rating_year as (select * from (select max(rating) over(partition by year), year, title_id from ratings_years
		order by year) as temp
		where year >= 2000 and year <= 2017)
select distinct primary_name, year, rating, votes from (select distinct * from titles
					natural join max_rating_year
					natural join ratings
					natural join primary_names
					where rating = max) as temp2
						order by year;
-- Question 1b --
with
	primary_names as (select title_id as series_id, name as primary_name from title_names 
		where is_primary = true),
	episodes as (select primary_name, episode_number, season_number, series_id from tv_series
		natural join series_episodes
		natural join primary_names),
	episode_count as (select primary_name, count(primary_name) as episode_count from episodes
		group by primary_name
		order by episode_count desc)
select * from episode_count
	where episode_count >= 6000;
