#! /usr/bin/env python

import os
import json
import datetime
import time
import xml.etree.ElementTree as ET
import math


def process(run_id):

    # Format the command
    command = """curl 'http://www.mapmyrun.com/vxproxy/v7.0/workout/{0}/?field_set=time_series&callback=success' \
        -H 'Accept-Encoding: gzip,deflate,sdch' \
        -H 'Accept-Language: en,en-US;q=0.8' \
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36' \
        -H 'Accept: text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01' \
        -H 'Referer: http://www.mapmyrun.com/workout/{0}' \
        -H 'X-Requested-With: XMLHttpRequest' \
        -H 'Connection: keep-alive' \
        --compressed -s""".format(run_id)

    # Run the command
    f = os.popen(command)

    # Get the response
    body = f.read()

    # Check that body string starts with 'success'
    if body.find('success') == 0:

        # Load into JSON object stripping the crap 'success()' from the outside
        response = json.loads(body[8:-1])

        # Separate constituent parts needed
        start = response['start_datetime']
        series = response['time_series']['position']

        # Make a datetime object to work with - this is our start time
        start_datetime = datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(start, '%Y-%m-%dT%H:%M:%S+00:00'))
        )

        xml_skel = '<?xml version="1.0" ?><gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://w' +\
            'ww.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.' +\
            'com/xmlschemas/TrackPointExtension/v1" creator="Oregon 400t" version="1.1" ' +\
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="h' +\
            'ttp://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd ' +\
            'http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xml' +\
            'schemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExte' +\
            'nsion/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd"><metad' +\
            'ata><link href="http://www.garmin.com"><text>Garmin International</text></l' +\
            'ink><time>{0}</time></metadata><trk><na'.format(start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), run_id) +\
            'me>Run ID: {0}</name><trkseg></trkseg></trk></gpx>'.format(run_id)

        # Sort out some XML
        tree = ET.fromstring(xml_skel)
        trk = tree.find('{http://www.topografix.com/GPX/1/1}trk')
        trkseg = trk.find('{http://www.topografix.com/GPX/1/1}trkseg')

        # Process each item in the time series
        for item in series:

            # Set up track point
            trkpt = ET.Element('trkpt', lat=str(item[1]['lat']), lon=str(item[1]['lng']))

            # Set up elevation
            ele = ET.Element('ele')
            ele.text = str(item[1]['elevation'])
            trkpt.append(ele)

            # Set up datetime
            t = ET.Element('time')
            delta_date = start_datetime + datetime.timedelta(0, math.floor(item[0]))
            t.text = delta_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            trkpt.append(t)

            # Add to tree
            trkseg.append(trkpt)

        # Write out to file without any further ado
        with open('./done/{0}.gpx'.format(run_id), 'w') as f:
            
            # Off we go
            f.write(ET.tostring(tree).replace('ns0:', ''))

        # Done, so close handler
        f.close()

        # All good
        print 'Done!'

    else:

        # There's been an error
        print 'Error!'


if __name__ == '__main__':

    # Chuck 'em in here at will!
    process('633845437')
    process('633521891')
    process('630804379')
    process('627921859')

