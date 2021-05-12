import glob
import os
import ujson
import pandas as pd

def extract_city(row):
    """Extract city from address column and return as a new column."""
    if row["address"] is None:
        return None

    piece = row["address"][:row["address"].rfind(",")]  # find last comma
    city_name = piece.split(" ")[-1]

    return city_name.lower()

def add_county(row):
    """Add county information based on counties dict."""
    county = None
    for key in counties.keys():
        if row["address_city"] in counties[key]:
            county = key

    return county

# Set path
path = "/Users/MyMac/Desktop/mids/241/w241_final_project/"
# Set empty list to collect shop data
combined_list = []
# Dictionary to fix multiple word and misspelled cities
replace_values = {"way": "federal way",
                  "stevens": "lake stevens",
                  "terrace": "mountlake terrace",
                  "island": "camano island",
                  "city": "fall city",
                  "park": "lake forest park",
                  "heights": "airway heights",
                  "harbor": "gig harbor",
                  "gap": "union gap",
                  "vancover": "vancouver",
                  "valley": "spokane valley",
                  "place": "university place"}
# Dictionary to assign counties
# Aurburn and bothell span two counties (picked primary one by geography)
counties = {"king": ["seattle", "bellevue", "kent", "renton", "federal way", "kirkland", "auburn", "redmond",
                        "sammamish", "shoreline", "burien", "newcastle", "seatac", "bothell", "kenmore",
                        "woodinville", "issaquah", "maple valley", "fall city", "lake forest park"],
               "spokane": ["spokane", "spokane valley", "mead", "airway heights"],
               "pierce": ["tacoma", "lakewood", "puyallup", "fife", "spanaway", "gig harbor", "university place"],
               "clark": ["vancouver", "battleground", "camas"],
               "snohomish": ["everett", "marysville", "lynnwood", "arlington", "stanwood", "edmonds", "lake stevens",
                             "mountlake terrace", "snohomish"],
               "yakima": ["yakima", "union gap", "selah"],
               "whatcom": ["bellingham", "ferndale"],
               "benton": ["kennewick", "richland"],
               "franklin": ["pasco"],
               "thurston": ["olympia", "lacey", "tumwater"],
               "island": ["clinton", "camano island"]}

# Shops with more than one location (identified through look-up vs. name count)
more_chains = ["Coopers Auto Repair Specialists", "Cottman Transmission and Total Auto Care",
               "Dan Fast Muffler & Brake", "Erker’s Auto & Truck Repair", "Friendly Automotive West",
               "Gary’s Point S", "Gaynor’s Automotive",
               "Golden Rule Brake - Spokane Valley", "Good Neighbor Tire & Auto Service", "Goodyear Auto Service",
               "Honest-1 Auto Care", "Chuck’s Auto Repair - Shoreline", "Chuck’s Midtown Motors Automotive Repair",
               "Bonnie & Clyde’s Automotive Center", "Bonnie & Clyde’s Muffler Center",
               "Bonnie and Clyde’s Auto Center", "Bonnie and Clyde’s Muffler Center",
               "Ace Auto Repair & Tire Pros", "Ace Auto Repair & Tire Pros Shoreline", "All Auto Repair",
               "All Auto Repair Xpress", "Northwest Automotive", "Sculley’s Automotive", "Sears Auto Center",
               "Seattle Automotive", "Smart Service Independent Toyota Honda Subaru",
               "Terry’s Transmission and Auto Repair", "Tire Center", "Tire-Rama", "Tri-Cities Battery & Auto Repair",
               "Tri-Cities Battery And Auto Repair", "Tru-Line Bellevue", "Tru-Line Seattle", "Tune Tech",
               "Unlimited Service-Downtown", "Wilde Automotive"]

# Shops that do radiators or toyotas, mobile services, out of business, and duplicates
# (1 duplicate "Jimmy's Auto Service")
remove = ["Les Schwab Tire Center", "Jiffy Lube", "Grease Monkey", "Caliber Collision",
          "Gerber Collision & Glass", "Gerber Collision & Glass - Pasco", "All About Auto Collision",
          "Auburn Collision Center", "Bellevue Collision Center", "D & D Brakes",
          "Express Auto Body And Paint", "Fat Boys Fleet Services", "Gary Estes Mobile Repairs",
          "German Car Specialists", "Gorilla Auto Center", "H & I Automotive", "Hopkins Automotive",
          "Independent Subaru Repair & Service", "Jerry’s Little Car Shop Mazda’s Only", "Keith Cox Autobahn",
          "Lacey Collision Center", "Michael’s Collision Center", "Mouse Meat Inc.",
          "Northwest European Autoworks", "Northwest Rally Sports", "Northwest Subie Specialists",
          "James Mobile Auto Repair", "Kevin Osgood Mobile Mechanic", "Mechanic On The Move",
          "Paul’s Mobile Brake Service", "Pennzoil 10 Minute Oil Change", "Proformance Complete Auto Care",
          "Pros Tires", "R & N Repair", "Richard’s Mobile Mechanic Service", "Roadrunner Towing and Recovery",
          "Service King Collision Bellevue", "Service King Collision Burien", "Snohomish European Auto Service",
          "South Lake European", "Spalding Auto Parts", "Steve’s Mobile Automotive Services",
          "Stew’s Self Service Garage", "Stones German Garage", "Strictly BMW Independent Service", "TDC Auto Repair",
          "The Car Guy 253 - Mobile Mechanic", "Tork Motorsports", "Universal Tire & Wheel", "Valley Auto Glass",
          "Z Sport Euro"]

# COMBINE SHOP DATA
# Change working directory
os.chdir(path + "/02_source_data")

# Loop over shop json files, combine, and write to df
for file in glob.glob("*.json"):
    with open(file, "r") as f:
        contents = ujson.loads(f.read())

    combined_list += contents

df = pd.DataFrame(combined_list)

# Check df shape
print("\nThe combined dataframe has {} rows and {} columns.\n".format(df.shape[0], df.shape[1]))

# Check column counts by city
print("Column counts by city:")
print(df.groupby("city").count())

# DROP DUPLICATE RECORDS
# Drop duplicates
df = df.sort_values(by=["city", "page"])
df_deduped = df.drop_duplicates(subset=["url"], keep='first')
# Check de-duplicated df shape
print("\nThe de-duplicated dataframe has {} rows and {} columns.\n".format(df_deduped.shape[0], df_deduped.shape[1]))
# Check column counts by city after removing duplicates
print("Column counts by city after initial duplicate removal:")
print(df_deduped.groupby("city").count())

# SAVE PILOT RANDOM SAMPLE & COMBINED
# Randomly sample data for pilot shops
pilot_sample = df_deduped.sample(20, random_state=1)
# Save de-duplicated data as csv
df_deduped.to_csv(path + "02_source_data/combined_data.csv", encoding='utf-8-sig')
# Save pilot sample as csv
pilot_sample.to_csv(path + "02_source_data/pilot_sample.csv", encoding='utf-8-sig')

# DROP PILOT RECORDS
df_deduped = pd.merge(df_deduped, pilot_sample, how="outer", indicator=True)
df_deduped = df_deduped[df_deduped["_merge"] != "both"]
print("\nClean data:")
print("\tRemove {} pilot shops".format(pilot_sample.shape[0]))

# REMOVE INVALID SHOPS
# Remove shops that do not do radiators or toyotas, mobile, out of business, and duplicates (x1)
print("\tRemove {} invalid shops (no radiators/toyotas, mobile, out of business, one duplicate)".format(df_deduped[df_deduped["name"].isin(remove)].shape[0]))
df_deduped = df_deduped[~df_deduped["name"].isin(remove)]

# REMOVE SHOPS WITH MISSING ADDRESS OR PHONE
# Check for missing address and phone
print("\tRemove {} shops missing address".format(df_deduped["address"].isnull().sum()))
print("\tRemove {} shops missing phone number".format(df_deduped["phone_number"].isnull().sum()))

# Drop records with missing address or phone
# (13 records missing address - 9 are mobile; 1 record missing phone)
df_deduped = df_deduped.dropna(subset=["address", "phone_number"])

# ADD COUNTY INDICATOR & DROP OREGON RECORDS
# Extract city from address
df_deduped["address_city"] = df_deduped.apply(extract_city, axis=1)

# Drop 6 cities in Oregon (portland = 5, hillsboro = 1)
df_deduped_wa = df_deduped[(df_deduped["address_city"] != "portland") & (df_deduped["address_city"] != "hillsboro")]
print("\tRemove {} shops in Oregon".format(sum(df_deduped["address_city"] == "portland") + sum(df_deduped["address_city"] == "hillsboro")))

# Fix one city name to enable dictionary-based replace below
df_deduped_wa.loc[df_deduped_wa["name"] == "Maple Valley Auto Repair and Muffler", "address_city"] = "maple valley"

# Replace multiple word city names and typos (could only grab last word when parsing)
df_deduped_wa = df_deduped_wa.replace({"address_city": replace_values})

# Add county column
df_deduped_wa["county"] = df_deduped_wa.apply(add_county, axis=1)

# Check for missing counties
missing_counties = df_deduped_wa[df_deduped_wa["county"].isnull()]

print("\nAdd county indicator:")
print(df_deduped_wa["county"].value_counts())

# ADD CHAIN SHOP INDICATOR
# Get list of shops with more than one location
multiple_shops = df_deduped_wa["name"].value_counts().loc[lambda x: x > 1]
chains = multiple_shops.keys().tolist()

# Combine list of chains by count with chains identified by lookup
chains = chains + more_chains

# Add indicator for chain shops
df_deduped_wa["chain"] = df_deduped_wa["name"].apply(lambda x: 1 if x in chains else 0)

# Get count for chain shops vs. small shops
print("\nAdd chain shop indicator:")
print("\tThere are {} small shops".format(df_deduped_wa["chain"].value_counts()[0]))
print("\tThere are {} chain shops".format(df_deduped_wa["chain"].value_counts()[1]))

# GET COUNTY/CHAIN BLOCK SIZES
blocks = pd.crosstab(df_deduped_wa["county"], df_deduped_wa["chain"])
blocks.to_csv(path + "02_source_data/blocks.csv")
df_deduped.to_csv(path + "02_source_data/combined_data.csv", encoding='utf-8-sig')
print("\nCounty/chain block sizes:")
print(blocks)

# REMOVE UNNEEDED COLUMNS & RE-ORDER COLUMNS
df_deduped_wa = df_deduped_wa.drop(columns=["page", "city", "url", "_merge"])
df_deduped_wa = df_deduped_wa[["name", "address_city", "address", "phone_number", "county", "chain"]]

# CHECK FINAL DF SHAPE
print("\nThe cleaned, de-duplicated dataframe has {} rows and {} columns.\n".format(df_deduped_wa.shape[0], df_deduped_wa.shape[1]))

# SAVE DF FOR RANDOMIZATION
df_deduped_wa.to_csv(path + "02_source_data/combined_cleaned.csv", encoding="utf-8-sig", index=False)
