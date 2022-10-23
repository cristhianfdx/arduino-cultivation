window.onload = () => {
  let urlImage;

  const getAlerts = () => {
    let template = '';
    const data = document.querySelector('#data');

    fetch("/api/alerts")
      .then((response) => response.body)
      .then((rb) => {
        const reader = rb.getReader();

        return new ReadableStream({
          start(controller) {

            function push() {
              reader.read().then(({ done, value }) => {
                if (done) {
                  controller.close();
                  return;
                }

                controller.enqueue(value);
                push();
              });
            }
            push();
          },
        });
      })
      .then((stream) =>
        new Response(stream, { headers: { 'Content-Type': 'text/html' } }).text()
      )
      .then((result) => {
        const response = JSON.parse(result);
        response.forEach(alert => {
          const date = new Date(alert["created_at"]);
          template += `
                <tr>
                    <td>${alert["description"]}</td>
                    <td>${alert["type"]}</td>
                    <td>${alert["value"]}</td>
                    <td>${alert["status"]}</td>
                    <td>${date.toISOString().slice(0, 10)} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}</td>
                </tr>
            `;
        });
        data.innerHTML = template;
      })
      .catch((err) => console.error(err));
  };

  const setInputs = () => {
    fetch("/api/sensors")
      .then((response) => response.body)
      .then((rb) => {
        const reader = rb.getReader();

        return new ReadableStream({
          start(controller) {

            function push() {
              reader.read().then(({ done, value }) => {
                if (done) {
                  controller.close();
                  return;
                }

                controller.enqueue(value);
                push();
              });
            }
            push();
          },
        });
      })
      .then((stream) =>
        new Response(stream, { headers: { 'Content-Type': 'text/html' } }).text()
      )
      .then((result) => {
        const response = JSON.parse(result);
        response.forEach(sensor => {
          switch (sensor.type) {
            case 'hl_sensor':
              document.querySelector('#hl_sensor').value = sensor.value;
              break;
            case 'relative_humidity':
              document.querySelector('#relative_humidity').value = `${sensor.value}%`;
              break;
            case 'temperature':
              document.querySelector('#temperature').value = `${sensor.value}°C`;
              break;
            case 'heat_index':
              document.querySelector('#heat_index').value = `${sensor.value}°C`;
              break;
            default:
              urlImage = sensor.value !== 1 ? `./static/img/fresas-template.png` : `./static/img/fresas-agua.png`;
              document.querySelector('#img img').src = urlImage;
              break;
          }
        });
      })
      .catch((err) => console.error(err));
  };

  setInputs();
  getAlerts();

  setInterval(() => {
    setInputs();
    getAlerts();
  }, 500);
};
