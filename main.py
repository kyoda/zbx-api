# -*- coding: utf-8 -*-

import os
import urllib
import urllib2
import json

class ZabbixApi(object):

    def __init__(self, host, user, password):

        self.request_id = 1
        self.host = host
        self.auth_token = self.request('user.login', {'user': user, 'password': password})['result']

    def request(self, method, params, auth_token=None):

        if hasattr(self, 'auth_token'):
            auth_token = self.auth_token

        headers = {"Content-Type": "application/json-rpc"}
        uri = "https://{0}/zabbix/api_jsonrpc.php".format(self.host)
        data = json.dumps({'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'auth': auth_token,
            'id': self.request_id})
        request = urllib2.Request(uri, data, headers)
        self.request_id += 1
        return json.loads(urllib2.urlopen(request).read())

    def getUserid(self, name):
        key = 'userid'
        params = {
            'output': key,
            'filter': {
                'alias': [name]
            }
        }
        r = self.request('user.get', params)
        return r['result'][0][key]

    def getUsrgrpid(self, name):
        key = 'usrgrpid'
        params = {
            'output': key,
            'filter': {
                'name': [name]
            }
        }
        r = self.request('usergroup.get', params)
        return r['result'][0][key]

    def getMediatypeid(self, name):
        key = 'mediatypeid'
        params = {
            'output': key,
            'filter': {
                'description': [name]
            }
        }
        r = self.request('mediatype.get', params)
        return r['result'][0][key]

    def getGroupid(self, name):
        key = 'groupids'
        params = {
            'output': key,
            'filter': {
                'name': [name]
            }
        }
        r = self.request('hostgroup.get', params)
        return r['result'][0]['groupid']

    def getTemplateid(self, name):
        key = 'templateids'
        params = {
            'output': key,
            'filter': {
                'name': [name]
            }
        }
        r = self.request('template.get', params)
        return r['result'][0]['templateid']

    def getActionFromId(self, actionid):
        params = {
            'output': "extend",
            "selectOperations": "extend",
            "selectConditions": "extend",
            'filter': {
                'actionids': actionid
            }
        }
        r = self.request('action.get', params)
        return r


if __name__ == '__main__':

    api = ZabbixApi('localhost', 'user', 'password')
    filepath = os.path.dirname(os.path.abspath(__file__))

    ### user ###
    with open(filepath + '/user.json', 'r') as f:
        user = json.loads(f.read())
    admin_id = api.getUsrgrpid(u'Zabbix administrators')
    user['usrgrps'][0]['usrgrpid'] = admin_id
    r = api.request('user.create', user)
    print r

    ### mediatype ###
    with open(filepath + '/mediatype.json', 'r') as f:
        mediatype = json.loads(f.read())
    mediatype_id = api.getMediatypeid(u'Email')
    mediatype['mediatypeid'] = mediatype_id
    r = api.request('mediatype.update', mediatype)
    print r

    ### template ###
    with open(filepath + '/template.json', 'r') as f:
        template = json.loads(f.read())
    with open(filepath + '/template.xml', 'r') as f:
        source = f.read()
    template['source'] = source
    r = api.request('configuration.import', template)
    print r

    ### host ###
    # require 'groupid' 'templateid'
    #with open(filepath + '/host.json', 'r') as f:
    #    host = json.loads(f.read())
    #r = api.request('host.create', host)
    #print r

    ### action trigger ###
    #with open(filepath + '/action_trigger.json', 'r') as f:
    #    action_trigger = json.loads(f.read())
    ## require mediatypeid, userid, def_longdata, r_longdata
    #r = api.request('action.create', action_trigger)
    #print r

    ### action auto-registration ###
    # require templateid 
    #with open(filepath + '/action_auto.json', 'r') as f:
    #    action_auto = json.loads(f.read())
    #r = api.request('action.create', action_auto)
    #print r

