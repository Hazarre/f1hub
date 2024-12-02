## Value
- provide ground truth data about employers who sponsor. 
- a place for international students to share information about employment, immigration and life after graduation. 
- 


## Todo    
- Load data into SQL from exel spreadsheet for 2023 perm data
- Build a query agent that do QA against the db 
- Make model / db session read only 
- Build apis for common views



## MVP 
- use data from last 3-5 years, starting from 2018
- a few example questions and answers 
- views of aggregate common search queries  
	* by company, school, major, employer.
- agent to write generic SQL query against the full database, return the results back. 
- townhall 
- forum 



## Next
- User login, save searches/queries, personal info (school, major, year of graduation). 

## Tech 
- fastapi 
- 1Gb perm data => sqlite? simple deploy. cheap to run. 
- FE: 
 * React ShadCN or MaterialUI
 * Flutter https://pub.dev/packages/syncfusion_flutter_datagrid

## Additional 
- SQL query agent 
- sign on 

## Tools 
- [LangChang QA over SQL](https://python.langchain.com/docs/tutorials/sql_qa/)
- []

## Domains 
f-1central.com
f-1hub
f1stud.com
f-1grad.com
f1network.org

## Later