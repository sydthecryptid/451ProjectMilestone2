-- adapted from canvas starter code and milestone 1
-- used ai a little to identify bugs and troubleshoot code

--to reset db, use cascade to drop dependencies
DROP TABLE IF EXISTS BusinessCategory CASCADE;
DROP TABLE IF EXISTS Review CASCADE;
DROP TABLE IF EXISTS CheckIn CASCADE;
DROP TABLE IF EXISTS Business CASCADE;
DROP TABLE IF EXISTS Category CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS Address CASCADE;
DROP TABLE IF EXISTS Zipcode CASCADE;

--create tables in order of dependencies, follows the er model 

CREATE TABLE Zipcode (
    zipcode VARCHAR(5) PRIMARY KEY,
    population INT NOT NULL,
    averageIncome NUMERIC(10,2) NOT NULL
);

create table Address(
    addressID SERIAL PRIMARY KEY, --creates a unique id to use as primary key
    street VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL, -- US state abbrev. 
    zipcode VARCHAR(5) NOT NULL,
    FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode)
);

create table Business (
    businessID VARCHAR(22) PRIMARY KEY,
    name varchar(255) NOT NULL,
    stars NUMERIC(2,1) NOT NULL,
    reviewCount INT DEFAULT 0,
    totalCheckins INT DEFAULT 0, --calculated from each checkin
    averageReviewRating NUMERIC(2,1) DEFAULT 0.0, --calculated from each review
    addressID INT NOT NULL, --derived from address

    FOREIGN KEY (addressID) REFERENCES Address(addressID)
); 

create table "user" ( --not on er diagram, but needed for reviews
    userID VARCHAR(22) PRIMARY KEY,
    reviewCount INT DEFAULT 0
);

create table Review (
    reviewID VARCHAR(22) PRIMARY KEY,
    userID VARCHAR(22) NOT NULL,
    stars NUMERIC(2,1) NOT NULL,
    businessID VARCHAR(22) NOT NULL,

    FOREIGN KEY (businessID) REFERENCES Business(businessID),
    FOREIGN KEY (userID) REFERENCES "user"(userID)
);


create table Category(
    categoryTitle VARCHAR(255) PRIMARY KEY
);

create table BusinessCategory (
    businessID VARCHAR(22) NOT NULL,
    categoryTitle VARCHAR(255) NOT NULL,
    PRIMARY KEY (businessID, categoryTitle),
    FOREIGN KEY (businessID) REFERENCES Business(businessID),
    FOREIGN KEY (categoryTitle) REFERENCES Category(categoryTitle)
);

CREATE TABLE CheckIn (
    businessID VARCHAR(22) NOT NULL,
    day VARCHAR(9) NOT NULL,  
    time VARCHAR(5) NOT NULL, 
    frequency INT NOT NULL,
    PRIMARY KEY (businessID, day, time), --weak entity so use composite for primary key
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);
