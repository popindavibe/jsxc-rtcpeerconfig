from getturn.getturncredentials import *

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    json_file = 'turnConf.inc'
    json_data = open(json_file)
    result = turn_request_handler(json_data)
    json_data.close()

    return result
