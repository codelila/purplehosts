from subprocess import check_output

def generate():
  return check_output("cat /dev/urandom | tr -d -c '[:alnum:]' | head -c 10", shell=True)
