-- CSC 370 - Spring 2018
-- Assignment 3: Queries for Question 2 (ferries)
-- Name: James Ryan
-- Student ID: V00830984

-- Place your query for each sub-question in the appropriate position
-- below. Do not modify or remove the '-- Question 2x --' header before
-- each question.


-- Question 2a --
with
	pairings as (select sailings1.vessel_name as vessel1, sailings2.vessel_name as vessel2 from sailings as sailings1
		cross join
			sailings as sailings2
		where sailings1.route_number = sailings2.route_number
			and sailings1.scheduled_departure = sailings2.scheduled_departure
			and sailings1.vessel_name <> sailings2.vessel_name
			and sailings1.vessel_name < sailings2.vessel_name)
select vessel1, vessel2, count(vessel1) as num_pairings from pairings
	group by (vessel1, vessel2)
	order by num_pairings desc;
-- Question 2b --
with
	nom_dur_route as (select route_number, nominal_duration from routes),
	act_dur_route as (select 
				route_number,extract(epoch from (arrival - scheduled_departure)::interval / 60) as duration
				from sailings),
	avg_dur_route as (select route_number, avg(duration) as avg_duration from act_dur_route
			group by route_number)
select route_number, nominal_duration, avg_duration from avg_dur_route
	natural join nom_dur_route;
-- Question 2c --
with
	nom_dur_route1 as (select route_number, nominal_duration from routes
						where route_number = 1),
	late_sailings as (select * from sailings
		natural join nom_dur_route1
		where extract(epoch from ((arrival - scheduled_departure)::interval / 60)) >= nominal_duration + 5)
select date_part('month', departure_date)::integer as month, count(departure_date)
	from 
		(select scheduled_departure::date as departure_date from sailings
			where route_number = 1
		 except
		 select scheduled_departure::date as departure_date from late_sailings) as days_wout_late_sailings
	group by month;
-- Question 2d --
with
	total_sailings_vessel as (select vessel_name, count(scheduled_departure) as total_sailings from sailings
								group by vessel_name),
	nom_dur_route as (select route_number, nominal_duration from routes),
	late_sailing as (select * from sailings
		natural join nom_dur_route
		where extract(epoch from ((arrival - scheduled_departure)::interval / 60)) >= nominal_duration + 5),
	total_late_sailings_vessel as (select vessel_name, count(scheduled_departure) as late_sailings from late_sailing
								group by vessel_name)
select vessel_name, total_sailings, late_sailings, 
		(late_sailings::double precision/total_sailings::double precision) as late_fraction 
		from total_sailings_vessel 
				natural join total_late_sailings_vessel
			  union
			  select vessel_name, total_sailings, 0 as late_sailings, 0 as late_fraction from 
				(select vessel_name from total_sailings_vessel 
				except
				select vessel_name from late_sailing) as temp1
					natural join total_sailings_vessel
	order by vessel_name;
		
-- Question 2e --

-- Question 2f --

-- Question 2g --
with
	nom_dur_route as (select route_number, nominal_duration from routes),
	late_sailing as (select vessel_name, arrival from sailings
					     natural join nom_dur_route
					     where 
					     	extract	(epoch from ((arrival - scheduled_departure)::interval / 60)) > nominal_duration + 5),
	sailings_left_late as (select vessel_name, arrival from sailings
						       where
						       extract(epoch from ((actual_departure - scheduled_departure)::interval / 60)) >= 15),
	made_up_sailings as (select vessel_name, arrival  from sailings_left_late
							except
						 select vessel_name, arrival from late_sailing)
select vessel_name, count(vessel_name) from made_up_sailings
	group by vessel_name;