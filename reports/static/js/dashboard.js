    const map = L.map('heatmap').setView([-17.824858, 31.053028], 6);

    // OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    const incidentData = [
        {lat: -17.824858, lon: 31.053028, severity: 3},
        {lat: -18.01274, lon: 31.07555, severity: 5},
        // So now I want to get these from db
    ];

    //incidents as circles with color-coded severity
    incidentData.forEach((incident) => {
        const color = incident.severity > 3 ? 'red' : 'green';
        L.circle([incident.lat, incident.lon], {
            color: color,
            radius: incident.severity * 500
        }).addTo(map);
    });

    const labels = ["Week 1", "Week 2", "Week 3", "Week 4"];
    const data = {
        labels: labels,
        datasets: [{
            label: 'Reported Incidents',
            data: [50, 70, 45, 80],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    const trendChart = new Chart(
        document.getElementById('trendChart'),
        config
    );