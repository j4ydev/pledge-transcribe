import pandas as pd
from config import APPROVAL_DATAFRAME_PATH, INSPECT_DATAFRAME_PATH

df = pd.read_csv("")
headings = df.columns.tolist(INSPECT_DATAFRAME_PATH)

# Drop unnecessary columns.
df.drop(columns=headings[1], inplace=True)
df.drop(columns=headings[2], inplace=True)
df.drop(columns=headings[3], inplace=True)
df.drop(columns=headings[4], inplace=True)
df.drop(columns=headings[5], inplace=True)
df.drop(columns=headings[6], inplace=True)
df.drop(columns=headings[7], inplace=True)
df.drop(columns=headings[8], inplace=True)
df.drop(columns=headings[9], inplace=True)
df.drop(columns=headings[10], inplace=True)
df.drop(columns=headings[11], inplace=True)
df.drop(columns=headings[12], inplace=True)
df.drop(columns=headings[13], inplace=True)
df.drop(columns=headings[15], inplace=True)
df.drop(columns=headings[16], inplace=True)
df.drop(columns=headings[17], inplace=True)

headings = ['video_id', 'approval']  
df.columns = headings

df['approval'].replace('Doubt', 'Reject', inplace=True)
df['approval'].replace('InvigilationState', 'Reject', inplace=True)
df['approval'].fillna('Reject', inplace=True)

df.to_csv(APPROVAL_DATAFRAME_PATH, index=False)
