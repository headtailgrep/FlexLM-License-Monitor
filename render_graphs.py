#!/usr/bin/python

## render_graphs.py, r03 - license monitor cgi/template
## last revised: 2021-05-13
## author: John Reiser <reiser@rowan.edu>
## updated by Stephen C. Host P. Eng., steve@hostovsky.com
## updates rrdgraphs
## r04: added hline to denote a red line for the maximum number of licenses 
## owned, update the hrule variable for each database to reflect your license count
## and improve readability for your users. 
## Thanks John for writing this great tool!
##
## Also added a 3 month  tframes option (requires editing index.html to match calls)
##
##
## WARNING: update the paths below (imgdir, rrdir) to suit your install (Host)
##

import os, sys, cgi, time, rrdtool
#import cgitb
#cgitb.enable()
q = cgi.FieldStorage()



url = "" # with trailing slash
imgdir = "/var/www/htdocs/"
rrddir = "/var/www/htdocs/monitor/rrd/"


licenses = ['AutoCAD', 'ACADE', 'ACAD2004', 'MINITAB', 'LDLFLM', 'SOLIDWORKS', 'MATLAB', 'VISMOCK', 'ABAQUS', 'NX', 'SIEMENSTCA', 'SIEMENSTCC', 'SWPRO', 'SWPUB', 'SWOFFICEPRO', 'GLYPH', 'SPINFIRE', 'ideas', 'CREO', 'CREOPRO', 'MATHCAD', 'PDMVIEW', 'PDMEDIT', 'PDMPROCESSOR']
tframes = {'24hours':300, '7days':2100, '1month':9000,'3months':18000, '1year':109500} #key: text of timeframe, value: refresh rate
period = '24hours' 



if q.getfirst('period') in tframes.keys():
	period = q.getfirst('period')
if "license" in q:
	if q["license"].value in licenses:
		l = q["license"].value
		if (l == "AutoCAD"):
			hrule=35
		elif (l == "ACADE"):
			hrule=1
		elif (l == "ACAD2004"):
			hrule=4
		elif (l == "MINITAB"):
			hrule=20
		elif (l == "LDLFLM"):
			hrule=7
		elif (l == "SOLIDWORKS"):
			hrule=82
		elif (l == "MATLAB"):
			hrule=1
		elif (l == "VISMOCK"):
			hrule=5
                elif (l == "ABAQUS"):
			hrule=46
		elif (l == "SIEMENSTCA"):
			hrule=75
		elif (l == "SIEMENSTCC"):
			hrule=81
		elif (l == "SWPRO"):
			hrule=9
		elif (l == "SWPUB"):
			hrule=6
		elif (l == "SWOFFICEPRO"):
			hrule=7
		elif (l == "NX"):
                        hrule=2
                elif (l == "GLYPH"):
                        hrule=5
                elif (l == "SPINFIRE"):
                        hrule=2
                elif (l == "ideas"):
                        hrule=2
                elif (l == "CREO"):
                        hrule=3
		elif (l == "CREOPRO"):
			hrule=4
		elif (l == "MATHCAD"):
			hrule=3
		elif (l == "PDMVIEW"):
                        hrule=5
		elif (l == "PDMEDIT"):
                        hrule=20
                elif (l == "PDMPROCESSOR"):
                        hrule=50




		if "height" in q:
               		h = q["height"].value
		else:
			h=250

		if "width" in q:
			w = q["width"].value
		else:
	        	w=850


		hstr=str(hrule)
		hstring="LINE:"
                hstring+=hstr
                hstring+="#cc0000:max_licenses"

		wstr=str(w)
		htstr=str(h)
		sstring=wstr
		sstring+=htstr

		fn = imgdir+l+"-"+period+".png"
		if(not os.path.exists(fn)):
			tempfile = open(fn, "w")
			tempfile.write("")
			tempfile.close()
		if ((time.time()-os.stat(fn).st_mtime)>tframes[period]):
	        #if (1==1):
			try:
				rrdtool.graph(fn,
						  '--imgformat', 'PNG',
						  '--width', '600',
						  '--height', '200',
						  '-s', "-"+period,
						  '-l', '0', # no negative values, ever
						  '-u', '3', # max 3 y-axis by default 
						  '-Y', 
						  '--title', l+' Licenses used over '+period+' :'+ time.ctime(),
						  '--font', 'DEFAULT:0:Utopia',
						  hstring,
						  'DEF:value='+rrddir+l+'.rrd:value:MAX',
						  'AREA:value#3F1A0A:license_users')
			except:
				pass
		image = open(fn, 'rb').read()
		print "Content-Type: image/png\nContent-Length: %d\n" % len(image)
		print image
	else:
		print "Content-Type: text/plain\n"
		print "Invalid graph requested."
else:
	print "Content-Type: text/plain\n"
	print "Invalid request."
