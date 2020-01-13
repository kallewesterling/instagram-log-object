import pandas as pd
from pathlib import Path
import os

class Log():
    
    def __init__(self, filename=None):
        if filename == None: raise RuntimeError("A valid filename must be provided") from None
        self.filename = Path(filename)
        self.file_exists = self.filename.exists()
        self._current_df = None
        
        self._current_df = self._update_current_contents()
    
    def log(self, action, context, from_user, to_user):
        data = pd.DataFrame.from_dict([
            {
                "from_user": from_user,
                "to_user": to_user,
                "action": action,
                "context": context,
                "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "timestamp": pd.Timestamp.now()
            },
        ])
        if self.file_exists: 
            self._update_current_contents()
            self._current_df = self._current_df.append(data, ignore_index=True)
        else:
            self._current_df = data
        self._current_df.to_pickle(self.filename, compression='gzip')
        
    def reset(self):
        try:
            os.remove(self.filename)
            self.file_exists = False
            self._current_df = None
            return("Log removed.")
        except:
            raise RuntimeError("An error occurred and log was not removed.") from None
    
    def _update_current_contents(self):
        if self.file_exists: self._current_df = pd.read_pickle(self.filename, compression='gzip')
        else: self._current_df = None
        return(self._current_df)
    
    @property
    def current(self):
        self._current_df = self._update_current_contents()
        return(self._current_df)
    
    def search_user(self, username=None, _to=True, _from=False, provide="dataframe"):
        _ = self.current
        if self._current_df is not None:
            if _to: locs = self._current_df.loc[self._current_df['to_user'] == username]
            elif _from: locs = self._current_df.loc[self._current_df['from_user'] == username]
            if provide == "dataframe":
                return(locs)
            elif provide == "count":
                return(len(locs))
            else:
                raise RuntimeError("Could not interpret request for data provision.") from None
        else:
            if provide == "dataframe": return(pd.DataFrame())
            elif provide == "count": return(0)
            else: raise RuntimeError("Could not interpret request for data provision.") from None
    
    def search_target(self, username=None, provide="dataframe"):
        return(self.search_user(username=username, _to=True, _from=False, provide=provide))
    
    def search_source(self, username=None, provide="dataframe"):
        return(self.search_user(username=username, _to=False, _from=True, provide=provide))
    
    def search_date(self, date=None, provide="dataframe"):
        _ = self.current
        if self._current_df is not None:
            locs = self._current_df.loc[self._current_df['date'] == date]
            if provide == "dataframe":
                return(locs)
            elif provide == "count":
                return(len(locs))
            else:
                raise RuntimeError("Could not interpret request for data provision.") from None
        else:
            if provide == "dataframe": return(pd.DataFrame())
            elif provide == "count": return(0)
            else: raise RuntimeError("Could not interpret request for data provision.") from None
                
    def _latest_as_dict(self):
        _ = self.current
        if self._current_df is not None:
            index = self._current_df.last_valid_index()
            items = self._current_df.iloc[index]
            return({
                "from_user": items['from_user'],
                "to_user": items['to_user'],
                "action": items['action'],
                "context": items['context'],
                "date": items['date'],
                "timestamp": items['timestamp']
            })
        else:
            return({})
    
    @property
    def latest_as_dict(self):
        return(self._latest_as_dict())