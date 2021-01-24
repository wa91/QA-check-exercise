# QA check exercise

#### This Python script is designed to run predifined QA scripts on a Postgres database.

Postgres connection details are passed to the script as follows:

`python run_qa.py <Username> <Password> <Server> <Database>`

The script will then prompt for the required runtime parameters 'env' and 'date'.

The Postgres database table 'qa_tests' will then be read  - only where `enabled = 'Y'`

The test_sql parameters will be replaced by the runtime parameters, the tests will be run and output displayed.

Example qa_tests table:   (Parameters in test_sql are defined with a hashtag, in order to assist value replacement)
<table cellspacing=0 border=1>
					<tr>
						<td style=min-width:50px>code</td>
						<td style=min-width:50px>description</td>
						<td style=min-width:50px>enabled</td>
						<td style=min-width:50px>parameter</td>
						<td style=min-width:50px>test_sql</td>
						<td style=min-width:50px>exp_result</td>
					</tr>
					<tr>
						<td style=min-width:50px>qa_ch_01</td>
						<td style=min-width:50px>Runs the SQL against the
Channel table to count
duplicates. Duplicates
count must be 0</td>
						<td style=min-width:50px>Y</td>
						<td style=min-width:50px>env</td>
						<td style=min-width:50px>Select count(*) from (select
channel_code, count(*)
from channel_table_#env
group by channel_code
having count(*) > 1)t</td>
						<td style=min-width:50px>0</td>
					</tr>
					<tr>
						<td style=min-width:50px>qa_ch_02</td>
						<td style=min-width:50px>Check the FK between
channel_code and its
child table
channel_transaction to
identify orphans at a
given date</td>
						<td style=min-width:50px>Y</td>
						<td style=min-width:50px>env,date</td>
						<td style=min-width:50px>select count(*)
from
channel_transaction_#env A left join
channel_table_#env B on (A.channel_code
= B.channel_code)
where B.channel_code is null
and B.transaction_date = #date</td>
						<td style=min-width:50px>0</td>
					</tr>
					<tr>
						<td style=min-width:50px>qa_ch_03</td>
						<td style=min-width:50px>Counts the records in
channel_transaction
table at a given date that
have amount null</td>
						<td style=min-width:50px>N</td>
						<td style=min-width:50px>date</td>
						<td style=min-width:50px>select count(*) from
channel_transaction_#env
where transaction_date =
#date and transaction_amount
is null</td>
						<td style=min-width:50px>0</td>
					</tr>
				</table>
        
        
  Example display output:
  
  <img alt="output" src="https://imgur.com/oxEfAY6.png">
