#parsing json file 
import os 
import json
from pathlib import Path

class JsonParser :


    @staticmethod
    def parse (file_path) : 

        # get json file location 
        file_path = Path (file_path)

        #pare json file 
        with file_path.open('r',  encoding="utf-8") as file : 
            #json data frame 
            json_df = json.load(file)
            
        return json_df

    

