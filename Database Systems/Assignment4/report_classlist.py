# report_classlist.py
# James Ryan
# V00830984

#Examples and code snippets used
# create_course.py - Bill Bird
# enter_name_good.py - Bill Bird
# report_classlist.py - Bill Bird

import sys, csv, psycopg2

psql_user = 'ryanja' #Change this to your username
psql_db = 'ryanja' #Change this to your personal DB name
psql_password = 'HardCodedPassword' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

def print_header(course_code, course_name, term, instructor_name):
	print("Class list for %s (%s)"%(str(course_code), str(course_name)) )
	print("  Term %s"%(str(term), ) )
	print("  Instructor: %s"%(str(instructor_name), ) )
	
def print_row(student_id, student_name, grade):
	if grade is not None:
		print("%10s %-25s   GRADE: %s"%(str(student_id), str(student_name), str(grade)) )
	else:
		print("%10s %-25s"%(str(student_id), str(student_name),) )

def print_footer(total_enrolled, max_capacity):
	print("%s/%s students enrolled"%(str(total_enrolled),str(max_capacity)))

if len(sys.argv) < 3:
	print('Usage: %s \"<course code>\" <term>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
course_code, term_code = sys.argv[1:3]

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()
cursor2 = conn.cursor()

try:
	#check if course exists	
	cursor.execute("select * from course_offerings where course_code = %s and term_code = %s;", (course_code, term_code))
	record = cursor.fetchone()
	if record is None:
		print("Course offering does not exist.")
		cursor.close()
		conn.close()
		sys.exit()
		
	#get header information
	course_name = record[1]
	max_cap = record[3]
	i_name = record[4]
	print_header(course_code, course_name, term_code, i_name)
	#get enrolled students
	cursor.execute("select * from enrollment where course_code = %s and term_code = %s;", (course_code, term_code))
	for record in cursor:
		id = record[2]
		cursor2.execute("select name from students where id = %s;", (id,))
		name = cursor2.fetchone()[0]
		#get grade
		cursor2.execute("select grade from grades where id = %s and course_code = %s and term_code = %s;", (id, course_code, term_code))		
		grade = cursor2.fetchone()
		if grade:
			grade = grade[0]			
		print_row(id, name, grade)
		
	#get footer information
	cursor.execute("select count(*) from enrollment where course_code = %s and term_code = %s;", (course_code, term_code))
	enrolled = cursor.fetchone()[0]
	print_footer(enrolled, max_cap)
		
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