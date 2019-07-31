import requests
import pprint
import json
import random

from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from urllib.parse import urlencode, quote_plus
from timeit import default_timer as timer

# Variables
users = [
    "alice",
    "alsa",
    "andrei",
    "audio",
    "ben",
    "brenda",
    "bryan",
    "carla",
    "catalina",
    "chris",
    "chromeDefault",
    "condTest",
    "condTest2",
    "daniel-raw",
    "daniel",
    "davey",
    "david",
    "debbie",
    "easit1",
    "easit2",
    "elaine",
    "elmer",
    "elmerv",
    "elod",
    "empty",
    "franklin",
    "gert",
    "jaws",
    "jme_app",
    "jme_common",
    "li",
    "liam",
    "liam.md",
    "livia",
    "lorie",
    "lorie.md",
    "maggie",
    "magic",
    "maguro",
    "manuel",
    "mary",
    "mickey",
    "MikelVargas",
    "multi_context",
    "naomi",
    "nisha",
    "nvda",
    "nyx.json",
    "nyx.md",
    "olb_Alicia_app",
    "olga",
    "oliver",
    "omar",
    "omnitor1",
    "omnitor2",
    "os_android",
    "os_android_common",
    "otis",
    "phil",
    "rachel",
    "randy",
    "roger",
    "rose",
    "ryan",
    "salem",
    "sammy",
    "simon",
    "slater",
    "snapset_5",
    "talkback1",
    "talkback2",
    "testUser1",
    "timothy",
    "tom",
    "tvm_jasmin",
    "tvm_sammy",
    "tvm_vladimir",
    "uioPlusCommon",
    "uioPlus_captions",
    "uioPlus_character_space",
    "uioPlus_defaults",
    "uioPlus_font_size",
    "uioPlus_highlight_colour",
    "uioPlus_high_contrast",
    "uioPlus_inputs_larger",
    "uioPlus_line_space",
    "uioPlus_multiple_settings",
    "uioPlus_self_voicing",
    "uioPlus_simplified",
    "uioPlus_syllabification",
    "uioPlus_toc",
    "uioPlus_word_space",
    "vicky",
    "victoria",
    "vladimir",
    "wayne"
]

def filter_errors(response):
    if response is None:
        return True
    elif response.status_code != 200:
        return True
    else:
        return False

def get_oauth(username):
    auth_url = "https://flowmanager.jj.dev.gcp.gpii.net/access_token"
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
    }
    body = {
        "grant_type": "password",
        "username": username,
        "password": "test",
        "client_id": "pilot-computer",
        "client_secret": "pilot-computer-secret"
    }

    response = requests.post(auth_url, data=body, headers=headers, verify=False)

    if response.status_code == 200:
        r_data = response.json()
        if "access_token" in r_data:
            return r_data["access_token"]
    else:
        print("Error SCode: ", response.status_code)

    return None

def send_request(session, request, dev_rep_json, headers, auth_template, auth_users):
    # r_user_i = random.randint(0, len(users))
    r_user_i = 8
    r_user = users[r_user_i - 1]
    user_auth = None

    # Get user authentication if necessary
    if r_user not in auth_users:
        print("Get auths: ", auth_users)
        print("Get new auth: ", r_user)
        user_auth = get_oauth(r_user)

        if user_auth is not None:
            auth_users[r_user] = user_auth
        else:
            return None
    else:
        user_auth = auth_users[r_user]

    # Request the user data - Complete the payloads with the proper data
    final_req = request.format(r_user) % dev_rep_json
    headers["Authorization"] = auth_template.format(user_auth)

    # Send the request
    result = session.get(final_req, headers=headers, verify=False)
    return result


def send_requests(base_url, n):
    request = base_url + '/{}/settings/%s'
    auth_template = 'Bearer {}'
    headers = { 'Authorization': '', }
    results = []

    with open("device-reporter.json") as rep_file:
        dev_reporter = json.load(rep_file)
        dev_rep_json = json.dumps(dev_reporter)
        auth_users = {}
        session = FuturesSession(executor=ThreadPoolExecutor(max_workers=30))

        for i in range(0, n):
            print("Iteration: ", i)
            results.append(send_request(session, request, dev_rep_json, headers, auth_template, auth_users))

    return results

if __name__ == "__main__":
    base_url = "https://flowmanager.jj.dev.gcp.gpii.net"
    results_async = send_requests(base_url, 300)
    results = []

    for r in results_async:
        if r is not None:
            results.append(r.result())

    errors = list(filter(filter_errors, results))
    err_num = len(errors)

    print("Error num: ", err_num)
    print("Errors: ", errors)
    if err_num is not 0:
        print(errors[0].reason)
        print("Error headers: ", errors[0].headers)
        print("Error body: ", errors[0].text)


