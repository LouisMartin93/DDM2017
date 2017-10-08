#!/usr/bin/env python

"""
Create the stars and observations tables using Python.
"""

import sqlite3 as lite
from astropy.table import Table


# First read in the datafiles. I use astropy Table because
# this can be easily modified if we were to change the format
# in the future.
stars = Table().read('YAEPS.stars-table.dat',  format='csv')
observations = Table().read('YAEPS.observations-table.dat',  format='csv')


# Next, we create a connection to the database.
con = lite.connect("DDM17-python.db")

with con:


    # Create the command to create the table. I use a 
    # multiline string to ease readability here.
    table = 'Stars'
    command = """CREATE TABLE IF NOT EXISTS {0} (StarID INT,
			 FieldID INT, Star varchar(10), ra DOUBLE,
			 decl DOUBLE, g FLOAT, r FLOAT,
			 UNIQUE(StarID), PRIMARY KEY(StarID),
			 FOREIGN KEY(FieldID) REFERENCES Observations(ID))""".format(table)

    # Next, actually execute this command.
    con.execute(command)

    # Now that this is working, let us loop over the table entries
    # and insert these into the table.
    for row in stars:
        command = "INSERT INTO Stars VALUES({0},{1},'{2}',{3},{4},{5},{6})".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        print command
        con.execute(command)




    #
    # Create the observations table.
    #
    table = 'Observations'
    command = """
CREATE TABLE IF NOT EXISTS Observations (ID INT,
     	    Field varchar(10),
  		    date DOUBLE, 
		    exptime FLOAT,
		    quality FLOAT, 
  		    WhereStored varchar(256),
		    UNIQUE (ID),
		    PRIMARY KEY (ID)
			);
""".format(table)

    # Next, actually execute this command.
    con.execute(command)

    # Now that this is working, let us loop over the table entries
    # and insert these into the table.
    #
    # Note the '' around the string values - try to remove them, it won't go well!
    for row in observations:
        command = "INSERT INTO Observations VALUES({0},'{1}',{2},{3},{4},'{5}')".format(row[0], row[1], row[2], row[3], row[4], row[5])
        print command
        con.execute(command)
