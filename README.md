# Voltage–Current Measurement & Regression Web App

A lightweight Flask application that lets you:

- **Enter** measurement pairs (Voltage in volts, Current in amperes) via a web form  
- **Store** each reading in both **JSON** (`data.json`) and **XML** (`data.xml`) text files  
- **Display** all readings in a styled HTML table  
- **Plot** an interactive scatter‐plus‐best‐fit‐line chart in the browser (using Chart.js)  
- **Compute** a linear regression (σ₍V₎≪σ₍I₎) and show slope/intercept ± standard errors  

---

## 📁 Project Structure

```

measurement\_app/
├── app.py                # Flask server: form handling, JSON/XML I/O, regression logic
├── requirements.txt      # Python dependencies (Flask, NumPy)
├── data.json             # JSON array of measurement objects
├── data.xml              # XML document of <measurements>
└── templates/
├── index.html        # Data‐entry form (Voltage & Current)
└── results.html      # Table + regression stats + Chart.js plot

````

---

## 🚀 Installation & Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
   cd REPO_NAME
````

2. **Create & activate a Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize storage files**
   The first run of the app will create `data.json` and `data.xml` if they don’t exist.

5. **Start the server**

   ```bash
   python app.py
   ```

6. **Browse**

   * **Data entry** → [http://localhost:5000/](http://localhost:5000/)
   * **View results** → [http://localhost:5000/results](http://localhost:5000/results)

---

## 📝 How It Works

1. **Data Entry** (`/`)

   * HTML form asks for **Voltage (V)** and **Current (A)**.
   * On submit, POSTs to `/submit`.

2. **Storage** (`/submit`)

   * **JSON**: appends an object `{ "voltage": V, "current": I }` to `data.json` using Python’s `json` module.
   * **XML**: adds a `<measurement>` node with `<voltage>` and `<current>` children to `data.xml` using `xml.etree.ElementTree`.

3. **Reading & Regression** (`/results`)

   * Reads back JSON into NumPy arrays `Vs` and `Is`.
   * Computes a best‐fit line via `numpy.polyfit(Vs, Is, 1)` → slope (m) & intercept (b).
   * If >2 points, also computes covariance to extract standard errors σₘ, σ\_b (assumes negligible voltage error).

4. **Display**

   * Renders an HTML table of all (V,I) pairs.
   * Displays numeric regression results `m ± σₘ` and `b ± σ_b`.
   * Embeds a `<canvas>` and uses **Chart.js** to draw the scatter plot + fit line interactively.

---

## 📊 Data Format Overview

### JSON (JavaScript Object Notation)

* **Definition**: Lightweight, human‐readable text format using arrays (`[]`) and objects (`{}`).
* **Storage**:

  ```json
  [
    { "voltage": 1.23, "current": 0.45 },
    { "voltage": 2.34, "current": 0.78 }
    // …
  ]
  ```
* **I/O**: Python’s `json.load` / `json.dump` with `indent=2`.
* **Pros**: Concise; native JavaScript support; easy to parse.
* **Cons**: No comments; schema agreement required.

### XML (eXtensible Markup Language)

* **Definition**: Tag‐based hierarchical markup; self‐describing with custom tags.
* **Storage**:

  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <measurements>
    <measurement>
      <voltage>1.23</voltage>
      <current>0.45</current>
    </measurement>
    <measurement>
      <voltage>2.34</voltage>
      <current>0.78</current>
    </measurement>
    <!-- … -->
  </measurements>
  ```
* **I/O**: Python’s `xml.etree.ElementTree` for parsing & serialization.
* **Pros**: Supports schemas (XSD), namespaces; widely used in enterprise.
* **Cons**: Verbose; heavier parsing.

---

## 💡 Optional Database Alternative

For more advanced needs (concurrent access, complex queries):

* **SQLite** (embedded relational DB)

  * Python: built‐in `sqlite3` or SQLAlchemy ORM
  * Pros: Zero configuration; ACID‐compliant; powerful SQL querying.

* **MongoDB** (NoSQL document store)

  * Python: `pymongo`
  * Pros: Schemaless JSON documents; horizontal scalability.

Switching to a DB simplifies concurrency and indexing, but flat files suffice for lightweight lab use.

---

## 🛠 Customization & Extensions

* **Additional fields**: Extend form, JSON/XML structures, and regression logic.
* **Styling**: Update CSS in templates or link an external stylesheet.
* **Export**: Add CSV/Excel download endpoints.
* **Authentication**: Integrate Flask‐Login or OAuth for user‐specific data.

---

## 👤 Author

Rachit Jain

