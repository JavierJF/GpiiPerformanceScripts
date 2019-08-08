import json
import random

from locust import HttpLocust, TaskSet, task

dev_rep = open("device-reporter.json")
dev_rep_json = json.load(dev_rep)

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

def login(l, username):
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
    response = l.client.post("/access_token", data=body, headers=headers, verify=False)
    return response.json()["access_token"]

def preferences(l, username, access_token):
    request = "/{}/settings/%s"
    auth_template = 'Bearer {}'
    headers = { 'Authorization': '', }

    # Create the auth header
    headers["Authorization"] = auth_template.format(access_token)
    final_req = request.format(username) % json.dumps(dev_rep_json)

    l.client.get(final_req, headers=headers, verify=False)

class UserBehavior(TaskSet):
    access_token = ""
    username = "carla"

    def on_start(self):
        # r_user_i = random.randint(0, len(users))
        # self.username = users[r_user_i - 1]
        self.access_token = login(self, self.username)

    @task
    def my_task(self):
        preferences(self, self.username, self.access_token)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000