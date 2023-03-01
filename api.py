from flask import Flask, jsonify, request, send_file, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

@app.route("/")
def main():
    name="Welcome to the API"
    return render_template('index.html', name=name)

@app.route("/disk", methods=["POST"])
def disk():
    data = request.json
    if "fileLocation" not in data or "fileName" not in data:
        return jsonify({"error": "Missing required field in JSON payload."}), 400
    file_location = data["fileLocation"]
    file_name = data["fileName"]
    file_path = f"{file_location}/{file_name}"
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/mail", methods=["POST"])
def mailRoute():
    data=request.json
    sender_email = data["senderEmail"]
    receiver_email = data["receiverEmail"]
    subject = data["subject"]
    body = data["body"]
    print(body)
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, "")
    text = msg.as_string() # Convert the message to a string
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    return("Mail Send successfully")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')