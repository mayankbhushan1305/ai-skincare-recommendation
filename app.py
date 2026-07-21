from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for using sessions


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
    routine["treatment"] = "Basic hydrating serum"

  routine["sunscreen"] = "SPF 50 sunscreen Gel or Water-based"

  return routine


# Function to determine skin type from quiz answers
def determine_skin_type(oiliness, dryness, sensitivity):
  score = {"oily": 0, "dry": 0, "sensitive": 0, "combination": 0}

  if oiliness == "yes":
    score["oily"] += 2
  else:
    score["dry"] += 1

  if dryness == "yes":
    score["dry"] += 2
  else:
    score["oily"] += 1

  if sensitivity == "yes":
    score["sensitive"] += 2
  else:
    score["combination"] += 1

  return max(score, key=score.get)


# Home route
@app.route("/", methods=["GET", "POST"])
def index():
  recommendation = None
  predicted_skin = session.pop("predicted_skin", None)

  if request.method == "POST":
    skin_type = request.form.get("skin_type")
    concern = request.form.get("concern")

    routine = get_recommendation(skin_type, concern)

    recommendation = f"""
        <b>Cleanser:</b> {routine['cleanser']} <br>
        <b>Moisturizer:</b> {routine['moisturizer']} <br>
        <b>Treatment:</b> {routine['treatment']} <br>
        <b>Sunscreen:</b> {routine['sunscreen']}
        """

  return render_template(
      "index.html", recommendation=recommendation, predicted_skin=predicted_skin
  )


# Quiz route
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
  result = None
  predicted_skin = None

  if request.method == "POST":
    oiliness = request.form.get("oiliness")
    dryness = request.form.get("dryness")
    sensitivity = request.form.get("sensitivity")

    predicted_skin = determine_skin_type(oiliness, dryness, sensitivity)

    # Store predicted skin type in session to carry over to the home page
    session["predicted_skin"] = predicted_skin

    result = f"Your skin type is likely: {predicted_skin.title()}"

  return render_template(
      "quiz.html", result=result, predicted_skin=predicted_skin
  )


# Run the app
if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000)
