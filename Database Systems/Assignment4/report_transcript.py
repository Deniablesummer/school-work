# report_transcript.py
# James Ryan
# V00830984

#Examples and code snippets used
# create_course.py - Bill Bird
# enter_name_good.py - Bill Bird
# report_transcript.py - Bill Bird

import sys, csv, psycopg2

psql_user = 'ryanja' #Change this to your username
psql_db = 'ryanja' #Change this to your personal DB name
psql_password = 'HardCodedPassword' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

def print_header(student_id, student_name):
	print("Transcript for %s (%s)"%(str(student_id), str(student_name)) )
	
def print_row(course_term, course_code, course_name, grade):
	if grade is not None:
		print("%6s %10s %-35s   GRADE: %s"%(str(course_term), str(course_code), str(course_name), str(grade)) )
	else:
		print("%6s %10s %-35s   (NO GRADE ASSIGNED)"%(str(course_term), str(course_code), str(course_name)) )

if len(sys.argv) < 2:
	print('Usage: %s <student id>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
student_id = sys.argv[1]
	
conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()
cursor2 = conn.cursor()

try:
	#check if student exists
	cursor.execute("select * from students where id = %s;", (student_id,))
	record = cursor.fetchone()
	if record is None:
		print("Error: Student does not exist.")
		cursor.close()
		conn.close()
		sys.exit()
	#get name
	name = record[1]
	print_header(student_id, name)
	#get classes for student
	cursor.execute("select * from enrollment where id = %s;", (student_id,))
	for record in cursor:
		course_code = record[0]
		term_code = record[1]
		#get grade
		cursor2.execute("select grade from grades where id = %s and course_code = %s and term_code = %s;", (student_id, course_code, term_code))
		grade = cursor2.fetchone()
		if grade:
			grade = grade[0]
		#get course name
		cursor2.execute("select name from course_offerings where course_code = %s and term_code = %s;", (course_code, term_code))
		course_name = cursor2.fetchone()
		course_name = course_name[0]		
		#print row
		print_row(term_code, course_code, course_name, grade)
		
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