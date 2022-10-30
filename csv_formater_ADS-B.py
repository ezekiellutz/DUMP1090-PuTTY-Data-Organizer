# -*- coding: utf-8 -*-

#import packages to be used
import pandas as pd

#declare variables
filename = input('Enter the name of the file to be converted (including the file extension): ')

#open the .csv file as defined in the variable above

with open (filename,'r') as csv_file:

    df = pd.read_csv(csv_file, header=1)
    df.columns = ['REMOVE','MESSAGE','REMOVE','REMOVE','REGISTRATION','REMOVE','DATE (YYYY/MM/DD)','TIME (HH:MM:SS)','REMOVE','REMOVE','CALLSIGN/FLIGHT NUMBER','ALTITUDE (FT)','GROUNDSPEED (MPH)','TRACK/HEADING','LATITUDE','LONGITUDE','REMOVE','REMOVE','REMOVE','REMOVE','REMOVE','REMOVE']
    
    #assign the columns of interest into a dataframe
    
    df_registration = pd.DataFrame(df.loc[:,'REGISTRATION'])
    df_date = pd.DataFrame(df.loc[:,'DATE (YYYY/MM/DD)'])
    df_time = pd.DataFrame(df.loc[:,'TIME (HH:MM:SS)'])
    df_message = pd.DataFrame(df.loc[:,'MESSAGE'])
    df_callsign = pd.DataFrame(df.loc[:,'CALLSIGN/FLIGHT NUMBER'])
    df_altitude = pd.DataFrame(df.loc[:,'ALTITUDE (FT)'])
    df_groundspeed = pd.DataFrame(df.loc[:,'GROUNDSPEED (MPH)'])
    df_trackhead = pd.DataFrame(df.loc[:,'TRACK/HEADING'])
    df_latitude = pd.DataFrame(df.loc[:,'LATITUDE'])
    df_longitude = pd.DataFrame(df.loc [:,'LONGITUDE'])
    
#create new dataframes to add additional information regarding messages (type and description)
df_message_description = pd.DataFrame(df.loc[:,'MESSAGE'])
df_message_type = pd.DataFrame(df.loc[:,'MESSAGE'])
df_message_description.rename(columns = {'MESSAGE' : 'MESSAGE DESCRIPTION'}, inplace = True)
df_message_type.rename(columns = {'MESSAGE' : 'MESSAGE TYPE'}, inplace = True)

#replaces the numerical message identifier with a description of the message
df_message_description = df_message_description.replace(1, 'This message contains the tail number, flight number, and/or call sign of the reporting aircraft.', regex=True)
df_message_description = df_message_description.replace(2, 'This message was triggered by the nose gear squat switch.', regex=True)
df_message_description = df_message_description.replace(3, 'This message contains the altitude, latitude, longitude of the reporting aircraft.', regex=True)
df_message_description = df_message_description.replace(4, 'This message contains the ground speed and heading of the reporting aircraft.', regex=True)
df_message_description = df_message_description.replace(5, 'This message was triggered by ground radar and is not CRC secured. This message will only be sent if the reporting aircraft has previously sent message 1, 2, 3, 4, or 8.', regex=True)
df_message_description = df_message_description.replace(6, 'This message will only be sent if the reporting aircraft has previously sent message 1, 2, 3, 4, or 8.', regex=True)
df_message_description = df_message_description.replace(7, 'This message was triggered by TCAS (Traffic Collision Avoidance System).', regex=True)
df_message_description = df_message_description.replace(8, 'This message is typically a general broadcast by the reporting aircraft, but can also be triggered by ground radar.', regex=True)

#replaces the numerical message identifier with a message type identifier
df_message_type = df_message_type.replace(1, 'Identification and Category', regex=True)
df_message_type = df_message_type.replace(2, 'Surface Position Message', regex=True)
df_message_type = df_message_type.replace(3, 'Airborne Position Message', regex=True)
df_message_type = df_message_type.replace(4, 'Airborne Velocity Message.', regex=True)
df_message_type = df_message_type.replace(5, 'Surveilance Alt Message', regex=True)
df_message_type = df_message_type.replace(6, 'Surveilance ID Message', regex=True)
df_message_type = df_message_type.replace(7, 'Air to Air Message', regex=True)
df_message_type = df_message_type.replace(8, 'All Call Reply', regex=True)

#joins all dataframes to a master dataframe
df_master = df_date.join(df_time, how='outer')
df_master = df_master.join(df_altitude, how='outer')
df_master = df_master.join(df_groundspeed, how='outer')
df_master = df_master.join(df_trackhead, how='outer')
df_master = df_master.join(df_latitude, how='outer')
df_master = df_master.join(df_longitude, how='outer')
df_master = df_master.join(df_registration, how='outer')
df_master = df_master.join(df_callsign, how='outer')
df_master = df_master.join(df_message, how='outer')
df_master = df_master.join(df_message_type, how='outer')
df_master = df_master.join(df_message_description, how='outer')

#outputs the master dataframe to an excel spreadsheet that can be reviewed
df_master.to_excel('decoded_file.xlsx', index = False)