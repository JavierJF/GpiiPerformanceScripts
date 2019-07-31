import subprocess
import os

for n in range(10, 500, 50):
    for i in range(10, 50, 10):
        if n < 200 and i < 20:
            break
        base_url = "--host=https://flowmanager.jj.dev.gcp.gpii.net "
        args_locust = base_url + "-f " + os.getcwd() + "\\request-locus.py --no-web -c " + str(n) + " -r " + str(i) + " -t 60 --only-summary"
        print("Args: ", args_locust)
        args = ["locust " + args_locust]

        p = subprocess.Popen("locust " + args_locust, stdout=subprocess.PIPE)
        (out, err) = p.communicate()
        status = p.wait()

        if i >= n:
            break