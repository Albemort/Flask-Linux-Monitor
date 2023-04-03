fetch('/result')
    .then(res => res.json())
    .then(measdata => {
    document.getElementById("opsys").innerHTML = "<p>OS: " + measdata.OS + "</p>"
    document.getElementById("uptime").innerHTML = "<p>Running since: " + measdata.uptime + "</p>"
    document.getElementById("cpuname").innerHTML = measdata.CPU.cpu_name
    document.getElementById("cores").innerHTML = measdata.CPU.physical_and_logical_cpu_count
    document.getElementById("totram").innerHTML = measdata.ram.total_ram
    document.getElementById("useram").innerHTML = measdata.ram.used_ram
    document.getElementById("freeram").innerHTML = measdata.ram.free_ram
    document.getElementById("totdisk").innerHTML = measdata.disk.total_disk_space
    document.getElementById("usedisk").innerHTML = measdata.disk.used_disk_space
    document.getElementById("freedisk").innerHTML = measdata.disk.free_disk_space

    })

google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    var data = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['CPU', 55],
    ]);

    var options = {
    width: 400, height: 120,
    redFrom: 90, redTo: 100,
    yellowFrom:75, yellowTo: 90,
    minorTicks: 5
    };

    var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

    chart.draw(data, options);

    setInterval(function() {
    data.setValue(0, 1, 40 + Math.round(60 * Math.random()));
    chart.draw(data, options);
    }, 13000);
    setInterval(function() {
    data.setValue(1, 1, 40 + Math.round(60 * Math.random()));
    chart.draw(data, options);
    }, 5000);
    setInterval(function() {
    data.setValue(2, 1, 60 + Math.round(20 * Math.random()));
    chart.draw(data, options);
    }, 26000);
}