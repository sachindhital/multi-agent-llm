# llm/app/flask_app.py

from flask import Flask, render_template, request
import requests
import markdown

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():
    blog = None
    image_urls = []

    if request.method == "POST":
        topic = request.form["topic"]
        breakdown = request.form.get("breakdown", "")

        payload = {"topic": topic, "breakdown": breakdown}
        response = requests.post("http://localhost:8000/generate_blog", json=payload)

        if response.status_code == 200:
            data = response.json()
            blog = markdown.markdown(data["blog"])
            image_urls = data.get("image_urls", [])
        else:
            blog = f"<p style='color:red'>{response.text}</p>"

    return render_template("index.html", blog=blog, image_urls=image_urls)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
