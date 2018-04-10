-- CSC 370 - Spring 2018
-- Assignment 3: Queries for Question 3 (vwsn_1year)
-- Name: James Ryan
-- Student ID: V00830984

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 3x --' header before
-- each question.


-- Question 3a --
with
	max_temp as (select max(temperature) from observations)
select station_id, name, temperature, observation_time from observations
		natural join max_temp
		natural join stations
		where temperature = max and station_id = id;
-- Question 3b --
with
	max_temps as (select station_id, max(temperature) as max_temperature from observations
					group by station_id
					having station_id >=1 and station_id <= 10) 
select station_id, name, max_temperature, observation_time from observations
	natural join max_temps
	natural join (select id as station_id, name from stations) as station_info
	where temperature = max_temperature;
-- Question 3c --
with
	obs_in_june as (select station_id from observations
					where date_part('month', observation_time) = 6),
	temp1 as (select station_id from observations
				except
		  	  select station_id from obs_in_june)
select station_id, name from temp1
	natural join (select id as station_id, name from stations) as station_info;
-- Question 3d --

-- Question 3e --
