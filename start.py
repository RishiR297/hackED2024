from flask import Flask, request, send_file
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/update_graph', methods=['POST'])
def update_graph():
    # Get input data from the request
    data = request.json

    # Update the graph with the new data
    # (Assuming update_graph() and display_graph() are defined in your code)
    node1 = data['node1']
    node2 = data['node2']
    update_graph(node1, node2)

    # Save the graph as an image file and send it as a response
    plt.savefig('graph.png')
    return send_file('graph.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)