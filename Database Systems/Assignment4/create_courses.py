# create_courses.py
# James Ryan
# V00830984

#Examples and code snippets used
# create_course.py - Bill Bird
# enter_name_good.py - Bill Bird
import sys, csv, psycopg2

psql_user = 'ryanja' #Change this to your username
psql_db = 'ryanja' #Change this to your personal DB name
psql_password = 'HardCodedPassword' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

if len(sys.argv) < 2:
	print("Usage: %s <input file>",file=sys.stderr)
	sys.exit(0)
input_filename = sys.argv[1]

# Open your DB connection here
conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

with open(input_filename) as f:
	for row in csv.reader(f):
		if len(row) == 0:
			continue #Ignore blank rows
		if len(row) < 4:
			print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			break
		code, name, term, instructor, capacity = row[0:5]
		prerequisites = row[5:] #List of zero or more items
		
		try:
			cursor.execute("insert into courses values(%s) on conflict do nothing;", (code,))
			cursor.execute("insert into course_offerings values(%s, %s, %s, %s, %s) on conflict do nothing;", (code, name, term, capacity, instructor))
			for prereq in prerequisites:
				cursor.execute("insert into prerequisites values (%s, %s, %s)on conflict do nothing;", (code, term, prereq))
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

		