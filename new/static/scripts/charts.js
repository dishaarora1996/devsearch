  ///Service Booking Chart 
  const labels = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June', 
  ];

  const data = {
    labels: labels,
    datasets: [{
      label: 'Service Booking',
      backgroundColor: 'rgb(221, 74, 65)',
      borderColor: 'rgb(221, 74, 65)',
      data: [0, 10, 5, 2, 20, 30, 45],
    }]
  };

  const config = {
    type: 'bar',
    data: data,
    options: {}
  };

  const myChart = new Chart(
    document.getElementById('booking-chart'),
    config
  );
 ///Service Booking Chart 
 