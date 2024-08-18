from flask import Flask, render_template, request, jsonify
import restic

app = Flask(__name__)

# Initialize Restic repository (make sure to set your correct path)
try:
    restic.repository = '/tmp/backup1'
    restic.password_file = '/home/shyju/password.txt'
    #restic = Restic(repository="/path/to/repo", password="your_password")
except ResticInitError as e:
    print(f"Failed to initialize Restic repository: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/backup', methods=['POST'])
def backup():
    directory = request.form.get('directory')
    restic.repository = '/tmp/backup1'
    restic.password_file = '/home/shyju/password.txt'

    print(directory)
    if not directory:
        return jsonify({"status": "error", "message": "No directory provided."}), 400

    try:
        restic.backup(paths=[directory])
        return jsonify({"status": "success", "message": f"Backup of {directory} completed successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/snapshots')
def snapshots():
    try:
        snaps = restic.snapshots()
        #print(snaps)
        return jsonify(snaps)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


