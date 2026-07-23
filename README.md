## Project Milestone 2 - Sydnee Boothby CPTS 451 06/12

### Homework Guide:
1. Revised database schema: boothby_relations_v2.sql
2. Revised ER diagram: Boothby_ER_v2.pdf
3. Database population: run parseAndInsert_Sample.py 
4. Database retrieval stats: results pasted in boothby_TableSizes.txt
5. Update and trigger statements: boothby_TRIGGERS.sql and boothby_UPDATE.sql
6. Written proposal for business classification metrics: classificationMetrics.pdf
7. App prototype: business_search.ui (layout designs/settings) run prototype file: business_Search_App.py

### Prerequistes
python installed, venv setup
PyQt6 installed
yelp_business, yelp_checkin, yelp_review, yelp_user jsons (may not be in github repo)


### Terminal Commands to Run:

psql -U sydnee -d postgres : get psql running\

psql -U sydnee -d yelpdb -f boothby_relations_v2.sql : run sql file to create tables\ 
python parseAndInsert_Sample.py : run python file to import data from JSONS\
 
psql -U sydnee -d yelpdb -f boothby_UPDATE.sql : run update + triggers\
psql -U sydnee -d yelpdb -f boothby_TRIGGERS.sql\

python business_search_App.py: run app demo\ 


### In Progress:
-Add queries for business popularity + success (add ui buttons)
-Add zipcode stats in ui (num businesses, total population, average income)
-category refinement button


-more test cases + find bugs
-fix naming conventions of functions/files (current ver works, but is messy)


