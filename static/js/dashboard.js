fetch('/result')
    .then(res => res.json())
    .then(measdata => {
    document.getElementById("opsys").innerHTML = "<p>OS: " + measdata.OS + "</p>"
    document.getElementById("uptime").innerHTML = "<p>Running since: " + measdata.uptime + "</p>"
    document.getElementById("cpuname").innerHTML = measdata.CPU.cpu_name
    document.getElementById("cores").innerHTML = measdata.CPU.physical_and_logical_cpu_count
    document.getElementById("cpuload").innerHTML = measdata.CPU.cpu_load
    document.getElementById("totram").innerHTML = measdata.ram.total_ram
    document.getElementById("useram").innerHTML = measdata.ram.used_ram
    document.getElementById("freeram").innerHTML = measdata.ram.free_ram
    document.getElementById("totdisk").innerHTML = measdata.disk.total_disk_space
    document.getElementById("usedisk").innerHTML = measdata.disk.used_disk_space
    document.getElementById("freedisk").innerHTML = measdata.disk.free_disk_space
    document.getElementById("minlat").innerHTML = measdata.network_latency.min
    document.getElementById("maxlat").innerHTML = measdata.network_latency.max
    document.getElementById("avglat").innerHTML = measdata.network_latency.avg
    })

