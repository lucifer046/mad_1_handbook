from flask import Flask, render_template, request

# f_app: flask_application_instance
f_app = Flask(__name__)

# Main route handling both GET and POST
@f_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Show form to collect details
        return render_template("get_details.html")
    
    if request.method == "POST":
        # Process form data and display results
        u_name = request.form['name'] # u_name: user_name
        return render_template("display_details.html", display_name=u_name)

if __name__ == '__main__':
    f_app.run(debug=True)