file=open("time_table.txt")
l=[]
for i in file:
    l.append(i.split())
import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES=["https://www.googleapis.com/auth/calendar"]
def main_gg(summary,location,start_time,end_time):
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  try:
    service = build("calendar", "v3", credentials=creds)
    event={
      "summary":summary,
      "location":location,
      "colorId":6,
      "start":{
        "dateTime":start_time,
        "timeZone":"GMT+05:30"
      },
      "end":{
        "dateTime":end_time,
        "timeZone":"GMT+05:30"
      },
      "recurrence":[
        "RRULE:FREQ=WEEKLY;COUNT=20"
      ]
    }
    event=service.events().insert(calendarId="primary",body=event).execute()
    print(f"event created {event.get('htmlLink')}")
  except HttpError as error:
    print("an error occurred",error)
if __name__== '__main__':
  main_gg(summary,location,start_time,end_time)

theory_start=l[0][2:]
theory_end=l[1][1:]
lab_start=l[2][2:]
lab_end=l[3][1:]
def time_24_hour(l1):
    for i in range(0,len(l1)):
        if l1[i]=="Lunch":
            for j in range(i+1,len(l1)):
                integer=int(l1[j][0:2])
                l1[j]=str(integer+12)+l1[j][2:]
    return l1
theory_start=time_24_hour(theory_start)
theory_end=time_24_hour(theory_end)
lab_start=time_24_hour(lab_start)
lab_end=time_24_hour(lab_end)

import re
from datetime import datetime, timedelta
current_date = datetime.now()
days_until_next_monday = (0 - current_date.weekday()) % 7
next_monday = current_date + timedelta(days=days_until_next_monday)
pattern="[-]([a-zA-Z0-9]+)[-]([a-zA-Z0-9]{2})[-]([a-zA-Z0-9]{3})[-]([a-zA-Z0-9]{3,4})[-]([a-zA-Z0-9]{3})"
for i in range(4,16):
    for j in range(0,len(l[i])):
        h=['MON','TUE','WED','THU','FRI','SAT','SUN']
        if l[i][j] in h:
            days_until_next_monday = (h.index(l[i][j]) - current_date.weekday()) % 7
            next_day = current_date + timedelta(days=days_until_next_monday)
        elif l[i][j] in ['THEORY','LAB']:
            count=-1
            type_class=l[i][j]
        elif l[i][j] == "Lunch" or l[i][j]=='-':
            count+=1
        elif re.findall(pattern,l[i][j]):
            count+=1
            x=re.findall(pattern,l[i][j])
            summary=x[0][0]
            location=x[0][2]+" "+x[0][3]
            if type_class=="THEORY":
                start=theory_start[count]
                end=theory_end[count]
            elif type_class=="LAB":
                start=lab_start[count]
                end=lab_end[count]
            start_time=str(next_day.date())+"T"+start+":00"
            end_time=str(next_day.date())+"T"+end+":00"
            main_gg(summary,location,start_time,end_time)
        elif l[i][j][-1].isdigit():
            count+=1
