import pandas as pd

# Load the Excel sheets
ctf_df = pd.read_excel("../CTF.xlsx")
discord_df = pd.read_excel("output.xlsx")

# Create a mapping from discord ID to display name
id_to_name = discord_df.set_index("id")["display_name"].to_dict()

# Replace user IDs in the CTF DataFrame with corresponding display names
ctf_df["User"] = ctf_df["User"].map(id_to_name).fillna(ctf_df["User"])

# Save the updated CTF sheet
ctf_df.to_excel("CTF_updated.xlsx", index=False)

print("CTF.xlsx has been updated with display names and saved as CTF_updated.xlsx.")
