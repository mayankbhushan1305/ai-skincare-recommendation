from flask import Flask, render_template, request

app = Flask(__name__)

# Function to generate skincare recommendation
def get_recommendation(skin_type, concern):
    routine = {}

    # Skin type based
    if skin_type == "oily":
        routine["cleanser"] = "Salicylic acid foaming cleanser"
        routine["moisturizer"] = "Oil-free gel moisturizer"
    elif skin_type == "dry":
        routine["cleanser"] = "Hydrating gentle cleanser"
        routine["moisturizer"] = "Ceramide-rich cream"
    elif skin_type == "sensitive":
        routine["cleanser"] = "Fragrance-free gentle cleanser"
        routine["moisturizer"] = "Soothing aloe-based moisturizer"
    else:  # Combination or normal
        routine["cleanser"] = "Balanced mild cleanser"
        routine["moisturizer"] = "Lightweight moisturizer"

    # Concern based
    if concern == "acne":
        routine["treatment"] = "Niacinamide or salicylic acid serum"
    elif concern == "pigmentation":
        routine["treatment"] = "Vitamin C serum"
    elif concern == "aging":
        routine["treatment"] = "Retinol serum"
    else:
        routine["treatment"] = "Basic hydration serum"

    routine["sunscreen"] = "SPF 50 sunscreen"

    return routine


# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None

    if request.method == "POST":
        skin_type = request.form.get("skin_type")
        concern = request.form.get("concern")

        routine = get_recommendation(skin_type, concern)

        # Human-readable output
        recommendation = f"""
        <b>Cleanser:</b> {routine['cleanser']} <br>
        <b>Moisturizer:</b> {routine['moisturizer']} <br>
        <b>Treatment:</b> {routine['treatment']} <br>
        <b>Sunscreen:</b> {routine['sunscreen']}
        """

    return render_template("index.html", recommendation=recommendation)


# Run the app
if __name__ == "__main__":
    # Listen on all interfaces, port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)