# GPII Performance Testing Scripts

These scripts are used to test performance of local and cloud instances of the GPII.  To use these scripts, you will
need:

1. Python 3
2. Locust, which you can install using a command like `pip3 install locust`

# Running Locust

The file `request-locust.py` defines a configuration that will log in and then retrieve preference data for a user.

## Running against a local instance of the GPII

1. Start your instance from the `universal` repo using a command like: `node ./gpii.js`.
2. Start Locust from this directory using a command like `locust --host http://localhost:8081 -f request-locust.py`
