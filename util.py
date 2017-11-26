import collections
import threading
import json

# GLOBAL VARIABLE
is_connected = True
is_running = True

cur_status = ''

lock = threading.Lock()

lst_command = collections.OrderedDict()

# REGEX
JSON_REGEX = r"([^w ]+)_([\d]+)(\.json)"

res = None
with open('config.json') as json_data_file:
    res = json.load(json_data_file)

''' 
================================================================================
								END OF FILE
================================================================================
''' 