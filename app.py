from flask import Flask
from scraping import get_relevant_jobs

app = Flask(__name__)

@app.route('/getUserRelevantJobs', methods=['GET'])
def getUserReleventJobs():
    return  get_relevant_jobs()

if __name__ == '__main__':
    app.run(debug=True)