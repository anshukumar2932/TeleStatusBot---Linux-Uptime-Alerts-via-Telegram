 
# **Setting Up a Telegram Bot for Linux System Status Updates (Online/Offline Alerts)**  

---

#### HOW to make telegram bot

## **Step 1: Create a Telegram Bot and Get API Token**  
Telegram provides a **Bot API** that allows automated messages.  

### **1.1 Create a New Telegram Bot**  
1. Open Telegram and search for **"BotFather"** (official Telegram bot for managing bots).  
2. Start a chat and type:  
   ```
   /newbot
   ```
3. **Choose a name** for your bot (e.g., "MyServerBot").  
4. **Choose a unique username** (must end in `bot`, e.g., `myserver_status_bot`).  
5. **BotFather will give you a token** like this:  
   ```
   1234567890:ABCdefGhIjklMNOpQrSTUVwxyz1234567890
   ```
   **Save this token** (It is your `BOT_TOKEN` for the script).  

### **1.2 Get Your Telegram Chat ID**  
1. Open Telegram and search for **"IDBot"** or use this bot: [@userinfobot](https://t.me/useridinfobot).  
2. Start the bot and type:  
   ```
   /start
   ```
3. It will reply with your **Chat ID**:  
   ```
   Your Chat ID: 98*****1
   ```
   **Save this number** (It is your `CHAT_ID` for the script).  

---

## **Step 2: Create a Python Script for Telegram Alerts**  

### **2.1 Install Required Packages**  
1. Ensure Python is installed:  
   ```bash
   python3 --version
   ```
   If Python is missing, install it:  
   ```bash
   sudo apt install python3 -y
   ```
2. Install the **requests** library:  
   ```bash
   pip install requests
   ```

### **2.2 Create the Script**  
1. Open a terminal and create a new Python script:  
   ```bash
   nano /home/your-user/status_bot.py
   ```
2. **Copy and paste the following code:**  
   ```python
   import requests
   import time
   import os
   
   BOT_TOKEN = "1234567890:ABCdefGhIjklMNOpQrSTUVwxyz1234567890"
   CHAT_ID = "98*****1"
   MESSAGE = f"🔔 Linux system is online! {time.ctime()}"
   
   # Wait for network connectivity before sending a message (max 50 seconds)
   for _ in range(10):  # Try for 50 seconds (10 tries x 5 sec)
       try:
           requests.get("https://api.telegram.org", timeout=5)
           break  # Exit loop if network is available
       except requests.exceptions.RequestException:
           time.sleep(5)  # Wait 5 seconds before retrying
   
   # ✅ Send message to Telegram **once**
   url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
   params = {"chat_id": CHAT_ID, "text": MESSAGE}
   response = requests.get(url, params=params)
   
   # ✅ Log response (optional)
   with open("/home/anshu/telegram_log.txt", "a") as log:
       log.write(f"{time.ctime()}: {response.status_code} - {response.text}\n")       
   ```
3. **Save and exit:**  
   - Press `CTRL+X`, then `Y`, then `Enter`.

4. **Make the script executable:**  
   ```bash
   chmod +x /home/your-user/status_bot.py
   ```

---

## **Step 3: Automatically Send Alerts When System Boots**  

### **Method 1: Use systemd (Recommended for 24/7 Reliability)**  
1. Create a systemd service:  
   ```bash
   sudo nano /etc/systemd/system/telegram-status.service
   ```
2. **Add the following content:**
   ```
   [Unit]
   Description=Send Telegram alert when system boots
   After=network.target

   [Service]
   User=your-user
   ExecStart=/usr/bin/python3 /home/your-user/status_bot.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```
   - Replace `your-user` with your actual Linux username.  
3. **Save and exit:** (`CTRL+X`, then `Y`, then `Enter`).  
4. **Enable the service to run at boot:**  
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable telegram-status
   ```
5. **Test by running manually:**  
   ```bash
   sudo systemctl start telegram-status
   ```
   If successful, you will receive a Telegram message:  
   ```
   🔔 Linux system is online!
   ```
6. **Reboot the system to test automatic startup:**  
   ```bash
   sudo reboot
   ```
   After the reboot, check your Telegram for a message.

---

### **Method 2: Use cron (Alternative for Simplicity)**  
Cron can execute the script at startup.  

1. Edit the cron jobs:  
   ```bash
   crontab -e
   ```
2. Add the following line at the bottom:  
   ```
   @reboot /usr/bin/python3 /home/your-user/status_bot.py
   ```
3. **Save and exit** (`CTRL+X`, then `Y`, then `Enter`).  
4. **Reboot to test:**  
   ```bash
   sudo reboot
   ```

---

## **Step 4: Send an Alert When the System is Shutting Down**  
To send a Telegram alert **before shutdown**, create another script.  

1. **Create a new shutdown script:**  
   ```bash
   nano /home/your-user/status_bot_shutdown.py
   ```
2. **Paste the following code:**  
   ```python
   import requests

   BOT_TOKEN = "your_bot_token"
   CHAT_ID = "your_chat_id"
   MESSAGE = "⚠️ Linux system is shutting down!"

   url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}"
   requests.get(url)
   ```
3. **Save and exit** (`CTRL+X`, `Y`, `Enter`).  
4. **Make it executable:**  
   ```bash
   chmod +x /home/your-user/status_bot_shutdown.py
   ```

### **Automatically Send Shutdown Alerts**
1. Open the system shutdown script:  
   ```bash
   sudo nano /etc/systemd/system/telegram-shutdown.service
   ```
2. **Paste the following:**
   ```
   [Unit]
   Description=Send Telegram alert before shutdown
   DefaultDependencies=no
   Before=shutdown.target reboot.target halt.target

   [Service]
   Type=oneshot
   ExecStart=/usr/bin/python3 /home/your-user/status_bot_shutdown.py

   [Install]
   WantedBy=halt.target reboot.target shutdown.target
   ```
3. **Save and exit** (`CTRL+X`, `Y`, `Enter`).  
4. **Enable the service:**  
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable telegram-shutdown
   ```
5. **Test it by shutting down the system:**  
   ```bash
   sudo shutdown -h now
   ```
   You should receive a message:  
   ```
   ⚠️ Linux system is shutting down!
   ```

---

## **Final Test: Ensure It Works 24/7**
- **Reboot your system** and check for the `"System is Online"` message.  
- **Manually shut down** and check for the `"System is Shutting Down"` message.  

---
