document.getElementById('imageInput').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/detect', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    document.getElementById('shipCount').textContent = data.ship_count;
    document.getElementById('shipTypes').textContent = data.ship_types.join(', ');

    // Update chart
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [...new Set(data.ship_types)],
            datasets: [{
                label: 'Ship Types',
                data: data.ship_types.reduce((acc, type) => {
                    acc[type] = (acc[type] || 0) + 1;
                    return acc;
                }, {}),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        }
    });
});
