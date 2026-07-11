## Project Milestone 2 - (NOT DONE) Sydnee Boothby CPTS 451 06/03

Homework documentation in separate file, 
JSON files are not included in github (too large to be committed), but are in canvas

### Terminal Commands to Run:

psql -U sydnee -d postgres : get psql running
psql -U sydnee -d postgres -c "CREATE DATABASE yelpdb;" : create db
sudo -u postgres psql -c "CREATE DATABASE yelpdb OWNER sydnee;" : if ownership issues 

psql -U sydnee -d yelpdb -f boothby_relations_v2.sql : run sql file to create tables
python parseAndInsert_Sample.py : run python file to import data from JSONS

### To Be Completed:
- debug python file (bugs with user and review data ip)
- written explanation of business popularity  
