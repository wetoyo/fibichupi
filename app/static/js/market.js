fetch('/market/{{ market.id }}/history.json')
  .then(r => r.json())
  .then(data => {
    const ctx = document.getElementById('priceChart');

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.map(d => d.timestamp.slice(11, 19)),
        datasets: [{
          label: 'YES price',
          data: data.map(d => d.price * 100),
          borderColor: '#34d399',
          backgroundColor: 'rgba(52, 211, 153, 0.15)',
          tension: 0.2,
          fill: true,
        }]
      },
      options: {
        scales: {
          y: {
            min: 0,
            max: 100
          },
          x: {}
        }
      }
    });
  });
