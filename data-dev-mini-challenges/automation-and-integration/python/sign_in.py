# ----------------------------------------------------------------------------
from credentials import tableau as creds

import requests
import json

# ----------------------------------------------------------------------------
def sign_in():
    url = f"{creds.server}/api/3.7/auth/signin"

    body = json.dumps({'credentials': {
                            'personalAccessTokenName': creds.token_name,
                            'personalAccessTokenSecret': creds.token_secret,
                            'site': {
                                'contentUrl': creds.site }}})

    headers = {'content-type': 'application/json',
               'accept': 'application/json'}

    response = requests.post(url, data=body, headers=headers)

    auth = json.loads(response.text)

    print(f'Sign in to site {creds.site} successful.\n')

    # print(f'Authentication details:\n\n{json.dumps(auth, indent=2)}')

    return auth


if __name__ == "__main__":
    sign_in()

