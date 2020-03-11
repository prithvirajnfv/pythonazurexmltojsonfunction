import logging

import azure.functions as func
import os
import xmltodict
import json

namespaces = {
  'SDML': None, # skip this namespace
  'FPML': None, # skip this namespace
}

def sd_xmltojson_function(msgIn: func.ServiceBusMessage, msgOut: func.Out[str]):
    try:
        strxml= msgIn.get_body().decode('utf-8')
        logging.info('Received xml from sdxmlqueue: %s', strxml)
        outMsgDict = xmltodict.parse(strxml, namespaces=namespaces, cdata_key='_value')
        logging.debug('Converted xml to json message: %s', outMsgDict)
        msgOut.set(json.dumps(outMsgDict))
    except Exception as e:
        logging.error('Failed to parse xml: {}'.format(str(e)))
        raise e 
    