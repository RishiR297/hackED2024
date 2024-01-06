from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/providers')
def providers():
    return render_template('providers.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')


# code for graph
y_values = []

@app.route('/update_graph', methods=['POST'])
def update_graph():
    # Get input data from the request
    data = request.get_json()
    node1 = data.get('node1')
    node2 = data.get('node2')

    # Convert the input values to numbers and add them to the y-values list
    y_values.extend([float(node1), float(node2)])

    # Generate x-values at fixed intervals
    x_values = list(range(len(y_values)))

    # Return the new graph data
    return jsonify({
        'labels': x_values,
        'datasets': [{
            'label': 'My Graph',
            'data': y_values,
            'fill': False,
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.1
        }]
    })

if __name__ == '__main__':
    app.run(debug=True)
