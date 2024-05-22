import os
import stat


def prepare_exp(SSHHost, SSHPort, REMOTEROOT, optpt):
    f = open("config", 'w')
    f.write("Host benchmark\n")
    f.write("   Hostname %s\n" % SSHHost)
    f.write("   Port %d\n" % SSHPort)
    f.close()

    f = open("run-experiment.sh", 'w')
    f.write("#!/bin/bash\n")
    f.write("set -x\n\n")

    # adjust this line to properly start memcached
    f.write("ssh -F config ubuntu@benchmark -o StrictHostKeyChecking=no -i /home/ubuntu/.ssh/test_key \" memcached -u ubuntu -p 11211 > memcached.out 2> memcached.err &\"\n")

    f.write("RESULT=`ssh -F config ubuntu@benchmark -o StrictHostKeyChecking=no -i /home/ubuntu/.ssh/test_key \"pidof memcached\"`\n")

    f.write("sleep 5\n")

    f.write(
        "if [[ -z \"${RESULT// }\" ]]; then echo \"memcached process not running\"; CODE=1; else CODE=0; fi\n")

    f.write("mcperf -l 0 -t 60 -n %d -N %d -s %s --port=11211 > stats.normal 2> stats.log\n\n" %
            (optpt["noRequests"], optpt["concurrency"], SSHHost))  # adjust this line to properly start the client

    # add a few lines to extract the "Response rate" and "Response time \[ms\]: av and store them in $REQPERSEC and $LATENCY"
    f.write(
        "REQPERSEC=`grep \"Response rate\" stats.log | awk '{print $3}'`\n")

    f.write(
        "LATENCY=`grep \"Response time \[ms\]: av\" stats.log | awk '{print $5}'`\n\n")

    f.write("ssh -F config ubuntu@benchmark -o StrictHostKeyChecking=no -i /home/ubuntu/.ssh/test_key \"sudo kill -9 $(cat memcached.pid)\"\n")

    f.write("echo \"requests latency\" > stats.csv\n")
    f.write("echo \"$REQPERSEC $LATENCY\" >> stats.csv\n")

    f.write("scp -F config ubuntu@benchmark -o StrictHostKeyChecking=no -i /home/ubuntu/.ssh/test_key:~/memcached.* .\n")

    f.write("if [[ $(wc -l <stats.csv) -le 1 ]]; then CODE=1; fi\n\n")

    f.write("exit $CODE\n")

    f.close()

    os.chmod("run-experiment.sh", stat.S_IRWXU)
