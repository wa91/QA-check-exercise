
import pandas,sqlalchemy,re,datetime,sys

#Get credentials from arguments
try:
	user=sys.argv[1]
	password=sys.argv[2]
	server=sys.argv[3]
	database=sys.argv[4]
except Exception as e: 
	print(e)
	print('Please pass Postrges credentials as arguments to the script e.g. code.py USERNAME PASSWORD SERVER DATABASE')
	quit()

#get runtime parameters
while True:
	env_in = input("Enter the parameter 'env': ")
	if len(env_in)==0:
		print("Please enter a valid environment parameter")
		continue
	else:
		break

while True:
	date_in = input("Enter the parameter 'date' in the format 'YYYY-MM-DD': ") 
	if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',date_in):
		print("Please enter a valid date parameter")
		continue
	else:
		break

# connect to Postgres
engine = sqlalchemy.create_engine('postgresql://'+user+':'+password+'@'+server+':5432/'+database+'',echo=False)

# read qa_tests table only where tests are enabled
rows = pandas.read_sql("select * from qa_tests where enabled='Y'", con=engine)

# replace sql with input parameters
rows['test_sql']=rows['test_sql'].str.replace('#env',env_in).str.replace('#date',"'"+date_in+"'::date")

#run the tests
print(" ")
for index, row in rows.iterrows():
	print(" ")
	print(row['code'])
	print(" ")
	print(row['test_sql'])
	print(" ")
	result = pandas.read_sql(row['test_sql'], con=engine)
	print(result.iloc[:,0][0])