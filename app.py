from flask import Flask, render_template, request, session
import os
import json
from werkzeug.utils import secure_filename
from resume_parser import extract_text_from_file
from scoring import calculate_similarity

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'  # Needed to use session

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    job_description = ''
    total_applicants = shortlisted_count = rejected_count = 0

    if request.method == 'POST':
        job_description = request.form['job_description']
        resumes = request.files.getlist('resumes')

        for file in resumes:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            resume_text = extract_text_from_file(filepath)
            ats_score = calculate_similarity(job_description, resume_text)
            status = "Shortlisted" if ats_score >= 75  else "Rejected"

            results.append({
                'filename': filename,
                'score': ats_score,
                'status': status
            })

        # Sort results by ATS score (descending)
        results.sort(key=lambda x: x['score'], reverse=True)

        # Store results in session for filtering later
        session['results'] = json.dumps(results)

        total_applicants = len(results)
        shortlisted_count = len([r for r in results if r['status'] == 'Shortlisted'])
        rejected_count = total_applicants - shortlisted_count

    return render_template("index.html",
                           results=results,
                           job_description=job_description,
                           total_applicants=total_applicants,
                           shortlisted_count=shortlisted_count,
                           rejected_count=rejected_count)


@app.route('/filter', methods=['GET', 'POST'])
def filter_results():
    filtered_results = []
    min_score = max_score = ""

    if 'results' not in session:
        return "No results available. Please upload resumes first."

    results = json.loads(session['results'])

    if request.method == 'POST':
        try:
            min_score = float(request.form['min_score'])
            max_score = float(request.form['max_score'])

            filtered_results = [
                r for r in results if min_score <= r['score'] <= max_score
            ]

            # Sort filtered results
            filtered_results.sort(key=lambda x: x['score'], reverse=True)

        except ValueError:
            return "Invalid score values. Please enter valid numbers."

    return render_template("filter.html",
                           filtered_results=filtered_results,
                           min_score=min_score,
                           max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True)
