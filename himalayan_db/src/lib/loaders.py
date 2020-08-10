import pandas as pd
import numpy as np
from collections import namedtuple

def phost_decode(code:int) -> str:
    """Decode peaks.phost.
    """
    try:
        switch = {0: "Unclassified",
                  1: "Nepal",
                  2: "China",
                  3: "India",
                  4: "Nepal, China",
                  5: "Nepal, India",
                  6: "Nepal, China, India"}
        return switch[code]
    except Exception:
        return ""

def pstatus_decode(code:int) -> str:
    """Decode peaks.pstatus.
    """
    try:
        switch = {0: "Unknown",
                  1: "Unclimbed",
                  2: "Climbed"}
        return switch[code]
    except Exception:
        return ""

def load_peaks(path:str="./../../data/csv/", eight_thousanders:bool=True) -> pd.DataFrame:
    """Load peaks above 8,000 meters from peaks.csv. 
    """
    peaks_df = pd.read_csv(path + "peaks.csv")
    
    # load data and perform basic cleanup
    if eight_thousanders:
        peaks_df = peaks_df[peaks_df.heightm >= 8000]
    else:
        peaks_df = peaks_df[peaks_df.heightm < 8000]
    peaks_df.reset_index(inplace=True, drop=True)
    peaks_df.phost = peaks_df.phost.apply(phost_decode)
    peaks_df.pstatus = peaks_df.pstatus.apply(pstatus_decode)
    
    # clean up selected NaN
    peaks_df.restrict.fillna("", inplace=True)

    # combine year and psmtdate
    pyear = peaks_df.pyear.copy()
    psmtdate = peaks_df.psmtdate.copy()

    # create first_ascend_date
    pyear[peaks_df.pyear.isnull()] = 0
    pyear = pyear.astype({'pyear':np.int32}).apply(str)
    first_ascend_date = pyear.str.cat(psmtdate, sep=" ")

    # combine year and psmtdate using proper time format
    # https://tinyurl.com/qno7ror
    first_ascend_date = pd.to_datetime(first_ascend_date, format="%Y %b %d", errors='ignore')
    peaks_df["first_ascend_date"] = first_ascend_date
    peaks_df = peaks_df.drop(["pyear", "psmtdate"], axis=1)
    
    return peaks_df

def load_expeditions(path:str="./../../data/csv/", eight_thousanders:bool=True) -> pd.DataFrame:
    """Load expeditions on peaks above 8,000 meters from expeditions.csv. 
    """
    # load external data
    exp_df = pd.read_csv(path + "expeditions.csv")
    peak_ids = load_peaks(path, eight_thousanders)["peakid"]
    
    # keep only expeditions for peaks above 8,000+ meters
    exp_df = exp_df[exp_df["peakid"].isin(peak_ids)].reset_index()   
    # remove all the shitty weird str
    exp_df.replace("  -   -", np.nan, inplace=True)
    
    return exp_df

def load_members(path:str="./../../data/csv/", eight_thousanders:bool=True) -> pd.DataFrame:
    """Load memebrs from expeditions on peaks above 8,000 meters from members.csv. 
    """
    # load external data
    mem_df = pd.read_csv(path + "members.csv")
    if not eight_thousanders:
        return mem_df
    
    # keep only members from expeditions for peaks above 8,000+ meters
    peakids = load_peaks(path, eight_thousanders)["peakid"]
    mem_df = mem_df[mem_df["peakid"].isin(peakids)].reset_index()   
    
    return mem_df

def load_unique_members(path:str = "./../../data/csv/", 
                        mem_df:pd.DataFrame = None,
                        duplicate_identifiers:list = ["fname", "lname", "sex"], 
                        drop_empty_names:bool = False, 
                        eight_thousanders:bool = True) -> pd.DataFrame:
    """Same as load_members. The only difference is that load_unique_members keeps only 
    unique climbers. For example, if Tom Jones appears on more than two expeditions, only 
    the first occurance in the dataset will be kept. 
    
    Args:
        path (str): Path to the csv file.
        mem_df (pd.DataFrame): If None, load_members will be invoked to load the csv.
        duplicate_identifiers (list): Column names used to identify the duplicate members. 
        drop_empty_names (bool): Set True to drop clilmbers with the first or last name not entered. 
    Return:
        (pd.DataFrame): Data frame with only unique memebers from expeditions to the peaks above 8,000 memters.
    """
    if mem_df is None:
        mem_df = load_members(path, eight_thousanders)
    
    # columns used for determine if the person is the same
    mem_df = mem_df.drop_duplicates(subset=duplicate_identifiers)
    if drop_empty_names:
        mem_df = mem_df[not (mem_df.fname.isnull() | mem_df.lname.isnull())]
    
    return mem_df.reset_index()
    