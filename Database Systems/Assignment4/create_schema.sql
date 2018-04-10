-- James Ryan --
-- V00830984 --

-- drop tables --
drop table if exists grades;
drop table if exists enrollment;
drop table if exists prerequisites;
drop table if exists course_offerings;
drop table if exists students;
drop table if exists courses;

-- drop functions --
drop function if exists course_size_trigger();
drop function if exists prereq_trigger();
drop function if exists valid_prereq_trigger();

-- Create students table --
CREATE TABLE students(
	id varchar(9),
	name varchar(255),
	primary key(id),
	check(length(id) > 0),
	check(length(name) > 0) 
	);
	
-- Create courses table --
CREATE TABLE courses(
	code varchar(10),
	primary key(code),
	check(length(code) > 0)
	);

-- Create course offerings table --
CREATE TABLE course_offerings(
	course_code varchar(10),
	name varchar(128),
	term_code varchar(6),
	maximum_capacity int,
	professor_name varchar(255),
	primary key(course_code, term_code),
	foreign key (course_code) references courses (code)
		on delete restrict
		on update restrict,
	check(length(name) > 0),
	check(maximum_capacity >= 0)
	);

-- Create enrollment table --
CREATE TABLE enrollment(
	course_code varchar(10),
	term_code varchar(6),
	id varchar(9),
	primary key (course_code, term_code, id),
	foreign key (course_code, term_code) references course_offerings (course_code, term_code)
		on delete restrict
		on update restrict,
	foreign key (id) references students (id)
		on delete restrict
		on update restrict
	);

-- Create grades table --
CREATE TABLE grades (
	id varchar(9),
	course_code varchar(10),
	term_code varchar(6),
	grade int,
	primary key (course_code, term_code, id),
	foreign key (id) references students (id),
	foreign key (course_code, term_code) references course_offerings (course_code, term_code)
		on delete restrict
		on update restrict,
	check(grade >= 0 and grade <= 100)
	);

-- Create prerequisites table --
CREATE TABLE prerequisites (
	course_code varchar(10),
	term_code varchar(6),
	prereq_course_code varchar(10),
	primary key (course_code, term_code, prereq_course_code),
	foreign key (course_code, term_code) references course_offerings (course_code, term_code)
		on delete restrict
		on update restrict,
	foreign key (prereq_course_code) references courses (code)
		on delete restrict
		on update restrict
	);
	
-- Functions --

-- Course size restriction --		
create function course_size_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from enrollment 
		where course_code = new.course_code and term_code = new.term_code) >
						(select maximum_capacity from course_offerings
							where course_code = new.course_code and term_code = new.term_code)
then raise exception 'Class at capacity';
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger prereq_constraint
	after insert or update on enrollment
	for each row
		execute procedure course_size_trigger();

-- Student Enrollment Prerequisite Restriction --
create function prereq_trigger()
returns trigger as
$BODY$
DECLARE
	prereq RECORD;
begin
for prereq in (select prereq_course_code from prerequisites where
								course_code = new.course_code and term_code = new.term_code)
	loop
		if (prereq.prereq_course_code = (select distinct course_code from enrollment where 
									course_code = prereq.prereq_course_code
									and id = new.id
									and term_code < new.term_code)) --if student enrolled in prereq course
		then
			if (prereq.prereq_course_code = (select distinct course_code from grades where
										course_code = prereq.prereq_course_code and
										id = new.id and
										term_code < new.term_code)) --if student has a grade
			then
				if (prereq.prereq_course_code = (select distinct course_code from grades where
										course_code = prereq.prereq_course_code and
										id = new.id and
										term_code < new.term_code and
										grade >= 50)) --if student has grade over 50
				then --do nothing
				else --student doesn't have a grade over 50
					raise exception 'Missing Prerequisite(s)';
				end if;
			else --student doesn't have a grade, do nothing
			end if;
		else --student not enrolled in prereq course
			raise exception 'Missing Prerequisite(s)';
		end if;
	end loop;
return new;
end
$BODY$
language plpgsql;

create trigger course_size_constraint		--Wanted to combine into one constraint with the course_offerings
	after insert or update on enrollment	--but PostgreSQL wouldn't allow it
	for each row
		execute procedure prereq_trigger();
		
-- Valid Prerequisite Trigger --
create function valid_prereq_trigger()
returns trigger as
$BODY$
begin
if (new.prereq_course_code = (select distinct course_code from course_offerings where
								course_code = new.prereq_course_code))
then
	return new;
end if;
raise exception 'No previous course offering for prerequisite';
return null;
end
$BODY$
language plpgsql;

create trigger prerequisite_constraint
	after insert or update on prerequisites
	for each row
		execute procedure valid_prereq_trigger();