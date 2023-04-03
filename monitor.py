import os
import platform
import subprocess
import shutil
import json

class Monitor:
    def get_statistics(self):
        ## Dictionary for the values
        statistics = {}

        os_name = platform.platform()
        statistics['OS'] = os_name

        uptime = os.popen("uptime -s").read().split('\n').pop(0)

        statistics['uptime'] = uptime

        cpu = os.popen("grep -m 1 'model name' /proc/cpuinfo").read().split(': ').pop(-1).split('\n').pop(0)
        ## Get the amount of cpu's
        physical_and_logical_cpu_count = os.cpu_count()

        ## Current cpu load %
        cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]

        statistics['CPU'] = dict(
            {
                'cpu_name': cpu,
                'physical_and_logical_cpu_count': physical_and_logical_cpu_count,
                'cpu_load': round(cpu_load)
            }
        )

        ## Linux command free -t -m to get the ram info
        total_ram, used_ram, free_ram = map(
            int, os.popen('free -t -m').readlines()[-1].split()[1:])

        ## Dump ram info to the dictionary
        statistics['ram'] = dict({
            'total_ram': round((total_ram / 1024), 2),
            'used_ram': round((used_ram / 1024), 2),
            'free_ram': round((free_ram / 1024), 2)
        })

        ## Get the disk usage info
        total, used, free = shutil.disk_usage("/")

        ## Dump disk info to dictionary
        statistics['disk'] = dict(
            {
                'total_disk_space': round(total / 1024 ** 3, 1),
                'used_disk_space': round(used / 1024 ** 3, 1),
                'free_disk_space': round(free / 1024 ** 3, 1)
            }
        )
        
        ping_result = subprocess.run(['ping', '-i 1', '-c 3', 'google.com'], stdout=subprocess.PIPE).stdout.decode(
        'utf-8').split('\n')

        ## Get the right variables
        min, avg, max = ping_result[-2].split('=')[-1].split('/')[:3]

        ## Dump the latency to dictionary
        statistics['network_latency'] = dict(
            {
                'min': float(min.strip()),
                'avg': float(avg.strip()),
                'max': float(max.strip())
            }
        )
        with open('result.json', 'w') as f:
            json.dump(statistics, f)