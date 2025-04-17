#!/bin/bash

SERVICE_NAME=smartassistant
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
PYTHON_PATH="/home/iotserver/face_rec/bin/python3"
SCRIPT_PATH="/home/iotserver/Desktop/face_recognition/main3.py"
WORK_DIR="/home/iotserver/Desktop/face_recognition"
USER_NAME="iotserver"

echo "Creating $SERVICE_NAME systemd service..."

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Smart Assistant (face_rec venv)
After=network.target

[Service]
ExecStart=$PYTHON_PATH $SCRIPT_PATH
WorkingDirectory=$WORK_DIR
User=$USER_NAME
Restart=always
StandardOutput=inherit
StandardError=inherit
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

echo "Reloading systemd and enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service
sudo systemctl start $SERVICE_NAME.service

echo "✅ $SERVICE_NAME service is now set to run on boot."
echo "Use 'journalctl -u $SERVICE_NAME -f' to monitor logs."
