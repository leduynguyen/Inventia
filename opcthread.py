from threading import *
from OpenOPC import *

import util
from util import res
# import resources as res

'''
    OPCThread Class 
'''

class OpcThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        while util.is_running:
            util.lock.acquire()
            try:
                # DEBUGGING
                # print util.lst_command
                for key in sorted(util.lst_command.keys()):
                    # DEBUGGING
                    # print util.lst_command[key]
                    opc_stt = util.lst_command[key]
                    if opc_stt == res['settings']['STT_01']:
                        opc_tag = '.'.join((opc_stt, res['settings']['ENABLE_TAG']))
                        burst_tag(opc_tag, 1, 0, 5)
                    elif opc_stt == res['settings']['STT_02']:
                        opc_tag = '.'.join((opc_stt, res['settings']['SWITCH_TAG']))
                        set_tag(opc_tag, 0)
                        opc_tag = '.'.join((opc_stt, res['settings']['ENABLE_TAG']))
                        is_err = False
                        for i in range(0, 5):
                            if not burst_tag(opc_tag, 1, 0, 5):
                                is_err = True
                                break
                            time.sleep(45)
                        if not is_err:
                            opc_tag = '.'.join((opc_stt, res['settings']['SWITCH_TAG']))
                            burst_tag(opc_tag, 1, 0, 5)
                    else:
                        # DEBUGGING
                        print ("Invalid JSON input file")
                        pass

                util.lst_command.clear()
            finally:
                util.lock.release()
            time.sleep(1)
            # DEBUGGING
            # print 'is_running : ' + str(util.is_running)


def burst_tag(opc_tag, value, return_value, burst_time):
    result = write_tag(opc_tag, value)
    util.cur_status = opc_tag + ' ' + res['naming']['LBL_LOGIC'] + ' ' + \
                      str(value) + ' : ' + result
    # DEBUGGING
    print("[" + str(time.time()) + "] Set " + str(value) + " to "
          + opc_tag + " " + result)
    if result == 'Error':
        return False
    time.sleep(burst_time)
    result = write_tag(opc_tag, return_value)
    util.cur_status = opc_tag + ' ' + res['naming']['LBL_LOGIC'] + ' ' + \
                      str(return_value) + ' : ' + result
    # DEBUGGING
    print("[" + str(time.time()) + "] Set " + str(return_value) + " to "
          + opc_tag + " " + result)
    if result == 'Error':
        return False
    time.sleep(45)

    return True

def set_tag(opc_tag, value):
    result = write_tag(opc_tag, value)
    cur_t = time.time()
    elapsed = int(time.time() - cur_t)
    # DEBUGGING
    print("[" + str(elapsed) + "] Set " + str(value) + " to "
          + opc_tag + " " + result)

          
'''
    write_tag function
'''

def write_tag(tag_name, value):
    try:
        opc = client()
        opc.connect(res['settings']['SERVER'])
    except:
        print ("Can NOT connect")
    result = opc.write((tag_name, value))
    opc.close()
    return result


''' 
================================================================================
                                END OF FILE
================================================================================
'''
