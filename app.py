from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import logging
import sys
import os

app = Flask(__name__)

# =========================
# إعداد Logging ل Console فقط
# =========================
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler (يظهر على Render logs)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# مفتاح أمان Webhook
SECRET_KEY = "8ca9as98d7as9d7as89d7a9sd7asd98"

# =========================
# دالة إرسال رسالة WhatsApp عبر Selenium
# =========================
def send_whatsapp_message(number, message):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://web.whatsapp.com")
        logger.info("Scan the QR Code on WhatsApp Web...")
        time.sleep(15)  # وقت لمسح QR Code
        
        # البحث عن الرقم
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.send_keys(number)
        time.sleep(3)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # كتابة الرسالة وإرسالها
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.send_keys(message)
        time.sleep(1)
        message_box.send_keys(Keys.ENTER)

        logger.info(f"Message sent to {number}: {message}")
        driver.quit()
    except Exception as e:
        logger.error(f"Error sending message to {number}: {e}")
        try:
            driver.quit()
        except:
            pass

# =========================
# Webhook endpoint
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    provided_key = request.headers.get("go-api-key")
    if provided_key != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    try:
        lead = data.get("lead", {})
        assigned_user = data.get("assigned_user", {})

        lead_name = lead.get("name")
        lead_phone = lead.get("phone")
        assigned_phone = assigned_user.get("phone-numb-assigned")

        # رسالة شكر للـ Lead (بدون رقم الهاتف)
        lead_message = f"شكراً لك {lead_name} على التواصل مع شركة Creators Media. فريقنا سيتواصل معك قريباً."

        # إشعار للمندوب
        agent_message = f"لديك Lead جديد: {lead_name} – {lead_phone}"

        # إرسال الرسائل في Threads منفصلة
        threading.Thread(target=send_whatsapp_message, args=(lead_phone, lead_message)).start()
        threading.Thread(target=send_whatsapp_message, args=(assigned_phone, agent_message)).start()

        logger.info(f"Webhook processed successfully for lead: {lead_name}")
        return jsonify({"status": "ok", "lead_message": lead_message, "agent_message": agent_message}), 200
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return jsonify({"error": str(e)}), 500

# =========================
# تشغيل السيرفر
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
