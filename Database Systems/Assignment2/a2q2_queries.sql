-- CSC 370 - Spring 2018
-- Assignment 2: Queries for Question 2 (ferries)
-- Name: James Ryan
-- Student ID: V00830984

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 2x --' header before
-- each question.


-- Question 2a --
select distinct vessel_name from fleet
	natural join sailings
		where route_number = 1;
-- Question 2b --
select distinct vessel_name, count(vessel_name) from fleet
	natural join sailings
	group by vessel_name;
-- Question 2c --
with T1 as (select distinct vessel_name, route_number from fleet
	natural join sailings)
select vessel_name, count(vessel_name) as num_routes from T1
	group by vessel_name
	having count(vessel_name) >= 2;
-- Question 2d --
select distinct route_number, vessel_name, year_built from sailings
	natural join fleet
	natural join (select route_number, min(year_built) as min_year from fleet natural join sailings
						group by route_number) as min_years
	where year_built = min_year
	order by route_number;
-- Question 2e --
with ports as (select distinct source_port as port from sailings
					where vessel_name = 'Queen of New Westminster'
				union
			   select distinct destination_port as port from sailings
			   		where vessel_name = 'Queen of New Westminster')
select distinct vessel_name from sailings 
	natural join ports
	where source_port in (port) or destination_port in (port);