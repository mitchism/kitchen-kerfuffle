import pandas as pd

''' 
with pickle, 	data writes in 288 ms, reads in 190 ms, filesize 91MB
with feather, 	data writes in 205 ms, reads in 245 ms, filesize 40MB
with parquet, 	data writes in 377 ms, reads in 363 ms, filesize 37MB
with json, 		data writes in 455 ms, reads in 580 ms, file size 98MB
with json gzip,	data writes in 1.03 s, reads in 958 ms, file size 23 MB  
'''

def picklewrite(df,name):
    df.to_pickle(f"{name}.pkl")

def pickleread(name):
    outputcontent = pd.read_pickle(f"{name}.pkl")
    return outputcontent

def parquetwrite(df,name):
    df.to_parquet(f"{name}.parquet") 
    
def parquetread(name):
    outputcontent = pd.read_parquet(f"{name}.parquet")
    return outputcontent

def featherwrite(df,name):
    df.to_feather(f"{name}.feather")
    
def featherread(name):
    outputcontent = pd.read_feather(f"{name}.feather")
    return outputcontent

def jsonwrite(df,name,pref):
    df.to_json(f"{name}(orient-{pref}).json",orient=pref,index=False)
    
def jsonread(name,pref):
    outputcontent = pd.read_json(f"{name}(orient-{pref}).json",orient=pref)
    return outputcontent

def jsonwrite_compressed(df,name,pref):
    comp_pref={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}
    df.to_json(f"{name}(orient-{pref})_gzip.json",orient=pref,index=False,compression=comp_pref)
    
def jsonread_compressed(name,pref):
    outputcontent = pd.read_json(f"{name}(orient-{pref})_gzip.json",orient=pref,compression='gzip')
    return outputcontent
