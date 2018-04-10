# report_enrollment.py
# James Ryan
# V00830984

#Examples and code snippets used
# create_course.py - Bill Bird
# enter_name_good.py - Bill Bird
# report_enrollment.py - Bill Bird

import sys, csv, psycopg2

psql_user = 'ryanja' #Change this to your username
psql_db = 'ryanja' #Change this to your personal DB name
psql_password = 'HardCodedPassword' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

def print_row(term, course_code, course_name, instructor_name, total_enrollment, maximum_capacity):
	print("%6s %10s %-35s %-25s %s/%s"%(str(term), str(course_code), str(course_name), str(instructor_name), str(total_enrollment), str(maximum_capacity)) )

# Open your DB connection here
conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()
cursor2 = conn.cursor()
	
try:
	cursor.execute("select * from course_offerings;")
	for record in cursor:
		c_code =  record[0]
		c_name =  record[1]
		t_code =  record[2]
		max_cap = record[3]
		i_name =  record[4]	
		cursor2.execute("select count(*) from enrollment where course_code = %s and term_code = %s", (c_code, t_code))
		enrolled = cursor2.fetchone()[0]
		print_row(t_code, c_code, c_name, i_name, enrolled, max_cap)
		
except psycopg2.ProgrammingError as err: 
	#ProgrammingError is thrown when the database error is related to the format of the query (e.g. syntax error)
	print("Caught a ProgrammingError:",file=sys.stderr)
	print(err,file=sys.stderr)
	conn.rollback()
except psycopg2.IntegrityError as err: 
	#IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
	print("Caught an IntegrityError:",file=sys.stderr)
	print(err,file=sys.stderr)
	conn.rollback()
except psycopg2.InternalError as err:  
	#InternalError generally represents a legitimate connection error, but may occur in conjunction with user defined functions.
	#In particular, InternalError occurs if you attempt to continue using a cursor object after the transaction has been aborted.
	#(To reset the connection, run conn.rollback() and conn.reset(), then make a new cursor)
	print("Caught an IntegrityError:",file=sys.stderr)
	print(err,file=sys.stderr)
	conn.rollback()
		
conn.commit()
cursor.close()
conn.close()