import http.client
import json
import urllib

import config


class API(object):
    """Retrieve data from person api as needed.  Will eventually replace Mozillians API"""
    def __init__(self):
        """
        :param session: the flask session to update with userinfo
        """
        self.config = config.OIDCConfig()
        self.person_api_url = 'uhbz4h3wa8.execute-api.us-west-2.amazonaws.com'

    def get_bearer(self):
        conn = http.client.HTTPSConnection(self.config.OIDC_DOMAIN)
        payload = json.dumps(
            {
                'client_id': self.config.OIDC_CLIENT_ID,
                'client_secret': self.config.OIDC_CLIENT_SECRET,
                'audience': 'https://person-api.sso.mozilla.com',
                'grant_type': 'client_credentials'
            }
        )

        headers = {'content-type': "application/json"}

        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode('utf-8'))

    def get_userinfo(self, auth_zero_id):
        user_id = urllib.quote(auth_zero_id)
        conn = http.client.HTTPSConnection("{}".format(self.person_api_url))
        token = "Bearer {}".format(self.get_bearer().get('access_token'))

        headers = { 'authorization': token }

        conn.request("GET", "/prod/profile/{}".format(user_id), headers=headers)

        res = conn.getresponse()
        data = res.read()
        return json.loads(json.loads(data.decode('utf-8')).get('body'))
