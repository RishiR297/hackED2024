// const express = require('express');
// const path = require('path');
// const app = express();

// app.use(express.json());

// // Serve static files from the "public" directory
// app.use(express.static(path.join(__dirname, 'public')));


// let yValues = [];

// function updateGraph(node1, node2) {
//     // Convert the input values to numbers and add them to the y-values array
//     yValues.push(Number(node1), Number(node2));

//     // Generate x-values at fixed intervals
//     let xValues = Array.from({length: yValues.length}, (_, i) => i);

//     // Return the new graph data
//     return {
//         labels: xValues,
//         datasets: [{
//             label: 'My Graph',
//             data: yValues,
//             fill: false,
//             borderColor: 'rgb(75, 192, 192)',
//             tension: 0.1
//         }]
//     };
// }

// app.post('/update_graph', (req, res) => {
//     // Get input data from the request
//     const data = req.body;

//     // Update the graph with the new data
//     // (Assuming updateGraph() is defined in your code)
//     const node1 = data.node1;
//     const node2 = data.node2;
//     const graphData = updateGraph(node1, node2);

//     // Send the new graph data as a response
//     res.json(graphData);
// });

// app.listen(3000, () => console.log('Server running on port 3000'));


// Assume you have an HTML input element with id 'input1' and 'input2'
let input1 = document.getElementById('input1');
let input2 = document.getElementById('input2');

// Add an event listener that sends a POST request whenever the input value changes
[input1, input2].forEach(input => {
    input.addEventListener('change', () => {
        fetch('/update_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ node1: input1.value, node2: input2.value }),
        })
        .then(response => response.json())
        .then(data => {
            // Update the graph with the new data
            Plotly.newPlot('myDiv', [data.datasets[0]], {
                xaxis: {
                    title: 'X Axis',
                },
                yaxis: {
                    title: 'Y Axis',
                }
            });
        });
    });
});