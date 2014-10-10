mapmyrun2gpx
============

Converts [mapmyrun](http://www.mapmyrun.com) workout data to a 
[GPX](http://www.topografix.com/gpx.asp) formatted file - Linux only, tested 
on Debian

This is a VERY SIMPLISTIC implementation of getting your precious workout data
from mapmyrun with all the timings.

Motivation
----------

I'm moving from mapmyrun to [Strava](http://www.strava.com/) and want to take 
my data with me and import it - after all, it's mine (I did all the running!). 
Unfortunately mapmyrun only gives you access to the route data, not how you ran 
it.

What does it do?
----------------

It makes a request to a workout page, as identified by its ID, and scrapes a 
JSON request for building the maps. It then takes the start time of the 
workout and uses that as a baseline for populating the rest of the GPX data.

Once done it drops the GPX data into a file named 'workout_ID'.gpx in the 
output directory _done_.

How to run it
-------------

NOTE: In order for this script to access your workout data you must make sure 
that each workout is set to be accessible publically. That's done by selecting 
the 'world' button on the top right hand toolbar of the workout view.

Just find the workout IDs of the workouts you want GPX data for. That ID is 
present in the URL, for example: http://www.mapmyrun.com/workout/123456789.
Add one or more at the end of the _getmmr2gpx.py_ file thus: 

    if __name__ == '__main__':

        # Chuck 'em in here at will!
        process('123456788')
        process('123456789')

Add as many as you like in the code above - it will chew though them all, 
leaving you a load of *.gpx files in the output directory. When you're ready
just run it:

    $ python getmmr2gpx.py

It either prints 'Error!' or 'Done!' once per call to _process()_ - that's
either a pass or a fail, respectively.

Requirements
------------

Just run:

    $ pip install -r requirements.txt

Please note that (on Debian/Ubuntu) _lxml_ has certain requirements best 
addressed by running the following beforehand:

    $ apt-get install libxml2-dev libxslt-dev python-dev

Regarding other Linuxes, please [google](http://www.google.com) or whatever.
