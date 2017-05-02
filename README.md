Udacity Full Stack Web Developer Nanodegree

Project 4: Tournament Results

Tournament Results is a python application that shows the makings of a Swiss Pairings
Tournament. Using PostgreSQL and Python DB-API to create and query data from the database.

What you will need to run the application:
1. Oracle VM Virtual Box
2. Vagrant
3. Python 2.7

How to run the application:
1. Fork and Download the github repository.
2. Navigate to the fullstack/vagrant folder.
3. Run vagrant up from Git Bash or Terminal.
4. Run vagrant ssh from Git Bash or Terminal.
5. Navigate to the ../../vagrant/tournament folder.
6. Run psql vagrant and create the tournament database then exit by typing \q.
7. Connect to the tournament database by running psql tournament.
8. Run the command \i tournament.sql to create the appropriate tables and views then exit by typing \q.
9. Finally run the command python tournament_test.py
