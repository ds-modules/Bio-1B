import pandas as pd
# Get Original Data of Sections with IDs

def collect_data(room):
    roomsSheetIDs = '1rlbYu9TdkNiZ9tnG6ndn_R5CTaASSlpnHEZREgf8Sdg'
    roomsSheetName = 'room_ids'
    rooms_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(roomsSheetIDs, roomsSheetName)
    rooms_df = pd.read_csv(rooms_URL)
    
    # Get Selected Room Data
    room_number = room.split(' ')[2]
    csv_id = rooms_df[rooms_df['Room Number'] == int(room_number)]['CSV ID'].values[0]
    SheetName = 'Room' + room_number
    rooms_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(csv_id, SheetName)
    
    return pd.read_csv(rooms_URL)