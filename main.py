from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/subdomains', methods=['POST'])
def get_subdomains():
    domain = request.json.get('domain')

    if not domain:
        return jsonify({'error': 'Domain not provided'}), 400

    try:
        process = subprocess.Popen(['subfinder', '-d', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        if process.returncode != 0:
            return jsonify({'error': f'Subfinder error: {error}'}), 500

        subdomains = output.strip().split('\n')

        # Save subdomains to a text file
        filename = os.path.join('users', f'{domain}.txt')
        with open(filename, 'w') as file:
            for subdomain in subdomains:
                file.write(subdomain + '\n')

        return jsonify({'subdomains': subdomains}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
