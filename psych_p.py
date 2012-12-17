# psych_study.py - Checks pennstate.sona-system.com site every 5 mins
# and texts you when a study is open
# Note: This has to be continuously on, for it to work
# This also uses mechanize, so you need to have that library
# Written by Wesley Sun

import mechanize
import datetime
import sched
import time
import smtplib

s = sched.scheduler(time.time, time.sleep)
studies_seen = []
temp_studies = []

def send_txt(text):
    user = 'EMAIL HERE'
    password = 'PASS HERE'
    emails = [PHONENUMBER HERE]
    server = smtplib.SMTP("smtp.gmail.com", 587) #this is for gmail
    server.starttls()
    server.login(user,password)
    server.sendmail(user, emails, text)

def check_site(awesomesauce):
    # Creates an instance of a browser
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False) #avoids fucken bots -_-

    # Makes you look like a computer
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # Open the site w/ login
    br.open('http://pennstate.sona-systems.com/')

    # Enters the form
    br.select_form(nr=0)
    br.form['ctl00$ContentPlaceHolder1$userid'] = 'PSU EMAIL HERE'
    br.form['ctl00$ContentPlaceHolder1$pw'] = 'PSU PASS'
    br.submit()

    # Reads the studies page
    studies_page = br.open('http://pennstate.sona-systems.com/all_exp.aspx').read()
    br.close()


    # time
    now = datetime.datetime.now()
    global temp_studies
    global studies_seen

    # loop to see if there's anything there
    if (studies_page.find('No studies are available at this time.') < 0):
        
        while studies_page.find('exp_info.aspx?experiment_id=') > 0:
            study_start = studies_page.find('exp_info.aspx?experiment_id=')
            study_end = studies_page.find('"',study_start+1)
            study = studies_page[study_start:study_end]
            
            if study not in temp_studies:
                temp_studies.append(study)
                
            studies_page=studies_page[study_end+1:]

        for s in temp_studies:
            if s in studies_seen:
                print str(now) + '//Already seen it'
            else:
                if len(studies_seen) == 0:
                    studies_seen = temp_studies
                else:
                    studies_seen.append(s)
                    
                if len(studies_seen) == 1:
                    send_txt('Sir, there is a psychological study available at this time.')
                    print str(now) + '//GOGOGOGOGOGOGOGOGOG'
                else:
                    send_txt('Sir, there are now ' + str(len(studies_seen)) + ' psychological studies available at this time.')
                    print str(now) + '//Studies up'
    else:
        print str(now) + '//Studies not up'
        temp_studies = []
        studies_seen = []

    awesomesauce.enter(60,1,check_site, (awesomesauce,))

s.enter(0,1, check_site, (s,))
s.run()
