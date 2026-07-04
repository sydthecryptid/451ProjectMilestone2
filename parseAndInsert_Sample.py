import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value): 
    if value == 0:
        return 'False'
    else:
        return 'True'
    
def disable_fk_constraints(conn): #prevent errors during inserts 
    """Temporarily disable foreign key constraints"""
    cur = conn.cursor()
    cur.execute("SET CONSTRAINTS ALL DEFERRED;")
    cur.close()

def enable_fk_constraints(conn):
    """Re-enable foreign key constraints"""
    cur = conn.cursor()
    cur.execute("SET CONSTRAINTS ALL IMMEDIATE;")
    cur.close()
    
# set database connection parameters
DB_PARAMS = dict(
    dbname="yelpdb",
    user="sydnee", #change to your username
    host="localhost",
    password="password"
)

def get_conn():
    return psycopg2.connect(**DB_PARAMS) 
    

COMMIT_BATCH_SIZE = 1000 #commit to db by batches

# populate address table, return unique id for key
def insertAddress(cur, street, city, state, zipcode):
    cur.execute(

        "INSERT INTO Address (street, city, state, zipcode) "
        "VALUES (%s, %s, %s, %s) RETURNING addressID",
        (street, city, state, zipcode),
    )
    return cur.fetchone()[0]  #generate id

# populate business table, each table follows similar pattern
def insertBusinessAndCategories(cur, data):
    address_id = insertAddress(
        cur,
        data["address"],
        data["city"],
        data["state"],
        data["postal_code"],
    )
 
    cur.execute(
        """INSERT INTO Business
               (businessID, name, stars, reviewCount, totalCheckins, averageReviewRating, addressID)
           VALUES (%s, %s, %s, %s, 0, 0.0, %s) ON CONFLICT (businessID) DO NOTHING""",
        (
            data["business_id"],
            data["name"],
            data["stars"],
            data.get("review_count", 0),
            address_id,
        ),
    )
 
    categories = data.get("categories") or []
    if categories: 
        for cat in categories:
            cat = cat.strip()
            if not cat:
                continue
            cur.execute(
                "INSERT INTO Category (categoryTitle) VALUES (%s) ON CONFLICT (categoryTitle) DO NOTHING",
                (cat,),
            )
            cur.execute(
                "INSERT INTO BusinessCategory (businessID, categoryTitle) "
                "VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (data["business_id"], cat),
            )
 

def insert2BusinessTable(path): 
    with open(path,'r') as f:   
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = get_conn()
        except Exception as e:
            print(f'Unable to connect to the database! with exception: {e}')
            return
        cur = conn.cursor()

        with open(path, 'r') as f:
            for line in f:
                data = json.loads(line)

                line = line.strip()
                if not line:
                    continue
                try:
                    insertBusinessAndCategories(cur, data)
                    count+=1
                    if count % COMMIT_BATCH_SIZE == 0:
                        conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"Error inserting line {count}:with open(path, 'r') as f: {e}")

        cur.close()
        conn.close()

    print(count, "businesses inserted" ) 
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()


def parseUser(path):
    conn = get_conn()
    cur = conn.cursor()
    count = 0
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            try:
                cur.execute(
                    'INSERT INTO "user" (userID, reviewCount) VALUES (%s, %s) ON CONFLICT (userID) DO NOTHING',
                    (data["user_id"], data.get("review_count", 0)),
                )
                count += 1
                if count % COMMIT_BATCH_SIZE == 0:
                    conn.commit()
                    print(f"...{count} users inserted")
            except Exception as e:
                conn.rollback()
                print(f"User insert failed for {data.get('user_id')}: {e}")
    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted: {count} users")

def parseReview(path):
    conn = get_conn()
    cur = conn.cursor()
    count = 0
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            try:
                cur.execute(
                    "INSERT INTO Review (reviewID, userID, stars, businessID) "
                    "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (data["review_id"], data["user_id"], data["stars"], data["business_id"]),
                )
                count += 1
                if count % COMMIT_BATCH_SIZE == 0:
                    conn.commit()
                    print(f"{count} reviews inserted")
            except Exception as e:
                conn.rollback()
                print(f"Review insert failed")
                print(f"Review insert failed for {data.get('review_id')}: {e}") #help debug
                
    conn.commit()
    cur.close()
    conn.close()
    print(f"Finished: inserted {count} reviews")

def parseCheckIn(path):
    conn = get_conn()
    cur = conn.cursor()
    count = 0
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            business_id = data.get("business_id")
            time_dict = data.get("time", {})
            for day, times in time_dict.items():
                for t, frequency in times.items():
                    try:
                        cur.execute(
                            'INSERT INTO CheckIn (businessID, day, time, frequency) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
                            (business_id, day, t, frequency),
                        )
                        count += 1
                        if count % COMMIT_BATCH_SIZE == 0:
                            conn.commit()
                            print(f"{count} check-ins inserted")
                    except Exception as e:
                        conn.rollback()
                        print(f"Check-in insert failed for {business_id} on {day} at {t}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted: {count} check-ins")

def parseZipcodes(path):
    conn = get_conn()
    cur = conn.cursor()
    zipcodes_seen = set()
    count = 0
    
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            zipcode = data.get("postal_code")
            
            if zipcode and zipcode not in zipcodes_seen:
                zipcodes_seen.add(zipcode)
                try:
                    cur.execute(
                        "INSERT INTO Zipcode (zipcode, population, averageIncome) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                        (zipcode, 0, 0.0),  # Default values since JSON doesn't have this data
                    )
                    count += 1
                    if count % COMMIT_BATCH_SIZE == 0:
                        conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"Zipcode insert failed for {zipcode}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted: {count} zipcodes") 


conn = get_conn()
disable_fk_constraints(conn) #prevent foreign key constraint violations
conn.close()

#insertion into tables in order of dependencies
parseZipcodes("./yelp_business.JSON")
insert2BusinessTable("./yelp_business.JSON")
parseUser("./yelp_user.JSON")
parseReview("./yelp_review.JSON")
parseCheckIn("./yelp_checkin.JSON")

conn = get_conn()
enable_fk_constraints(conn) #reenable foreign key constraints after inserts
conn.close()