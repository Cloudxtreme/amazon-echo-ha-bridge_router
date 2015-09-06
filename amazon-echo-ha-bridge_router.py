import subprocess
from flask import Flask
app = Flask(__name__)

# To control Harmony Hub, you can use HarmonyHubControl. The version at
# https://github.com/adamtart/harmony is configured to run on Mac OS X.
# (Kudos to cdegroot for getting it to work on OS X.)
# Activity IDs can be determined by calling HarmonyHubControl with the
# 'list_activities' command, e.g.:
#     HarmonyHubControl <username> <password> <hub_ip> list_activities
HARMONY_ACTIVITIES = {
    'OFF': '-1',
    'TV': "15440915",
    'CHROMECAST': '15440938',
    'PS3': '15440971',
    'NETFLIX': '15453134',
    'MAC_MINI': '15504106',
}

HARMONY_HUB_CONTROL = '/Users/adamtart/bin/harmonyhubcontrol/HarmonyHubControl'
HARMONY_HUB_IP_ADDRESS = '10.0.1.33'

HARMONY_CREDENTIALS_FILENAME = './harmony_credentials.txt'
harmony_username = None
harmony_password = None


def GetHarmonyCredentials(filename):
  """Retrieves Harmony username and password from file.

  File should be two lines, first line containing the Harmony username, and
  second line containing the Harmony password, e.g.:

      username
      hunter2

  Args:
    filename: string, filename containing Harmony username and password.

  Returns:
    Tuple (string, string): (<username>, <password>).
  """
  global harmony_username, harmony_password
  
  if (harmony_username is not None and harmony_password is not None):
    return (harmony_username, harmony_password)
  
  with open(filename, 'r') as f:
    lines = [line.strip() for line in f.readlines()]
  if len(lines) != 2:
    raise ValueError('File must have two lines!')
  harmony_username, harmony_password = (lines[0], lines[1])
  return harmony_username, harmony_password


def GetHarmonyCmd(activity):
  username, password = GetHarmonyCredentials(HARMONY_CREDENTIALS_FILENAME)
  print username, password
  return [
      "%s" % HARMONY_HUB_CONTROL,
      "%s" % username,
      "%s" % password,
      "%s" % HARMONY_HUB_IP_ADDRESS,
      "start_activity",
      "%s" % HARMONY_ACTIVITIES[activity]
  ]


def CallHarmonyCmd(activity):
  cmd = GetHarmonyCmd(activity)
  subprocess.call(cmd)
  msg = "%s turned ON" % activity
  print msg
  return msg


@app.route("/<activity>")
def harmony_activity(activity):
  if activity.upper() not in HARMONY_ACTIVITIES:
    return "Invalid activity %s" % activity
  return CallHarmonyCmd(activity.upper())


if __name__ == "__main__":
  app.run(host='0.0.0.0')