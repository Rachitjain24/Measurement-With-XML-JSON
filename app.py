from flask import Flask, render_template, request, redirect, url_for
import os, json, numpy as np, xml.etree.ElementTree as ET

app = Flask(__name__)
JSON_FILE = "data.json"
XML_FILE  = "data.xml"

def init_storage():
    # ensure JSON exists
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as f:
            json.dump([], f, indent=2)
    # ensure XML exists
    if not os.path.exists(XML_FILE):
        root = ET.Element("measurements")
        ET.ElementTree(root).write(XML_FILE,
                                  encoding="utf-8",
                                  xml_declaration=True)

def read_measurements():
    # load JSON array of {"voltage":V,"current":I}
    with open(JSON_FILE) as f:
        arr = json.load(f)
    Vs = [item["voltage"] for item in arr]
    Is = [item["current"] for item in arr]
    return np.array(Vs), np.array(Is)

@app.route('/')
def index():
    init_storage()
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    V = float(request.form["voltage"])
    I = float(request.form["current"])

    # --- JSON append ---
    with open(JSON_FILE) as f:
        data = json.load(f)
    data.append({"voltage": V, "current": I})
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)

    # --- XML append ---
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    meas = ET.SubElement(root, "measurement")
    ET.SubElement(meas, "voltage").text = str(V)
    ET.SubElement(meas, "current").text = str(I)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

    return redirect(url_for('results'))

@app.route('/results')
def results():
    Vs, Is = read_measurements()
    # pack for Chart.js
    points = [{"x": float(v), "y": float(i)} for v, i in zip(Vs, Is)]

    slope = intercept = err_slope = err_intercept = None
    if Vs.size >= 2:
        # fit line
        m, b = np.polyfit(Vs, Is, 1)
        slope, intercept = float(m), float(b)
        # error estimates only if >2 points
        if Vs.size > 2:
            _, cov = np.polyfit(Vs, Is, 1, cov=True)
            err_slope, err_intercept = map(float, np.sqrt(np.diag(cov)))

    return render_template(
        'results.html',
        points=points,
        slope=slope,
        intercept=intercept,
        err_slope=err_slope,
        err_intercept=err_intercept
    )

if __name__ == '__main__':
    init_storage()
    app.run(host='0.0.0.0', port=5000, debug=True)
