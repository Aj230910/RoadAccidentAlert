# 🚨 Road Accident Alert System – Real-Time Detection & Email Notification

An AI-powered full-stack application that captures live camera input, detects road accidents, and instantly sends an alert email with snapshot evidence and exact location for faster emergency response.

---

## 📌 Problem Statement

Road accidents often go unnoticed or are reported late, especially on highways and during night hours.  
The delay in informing emergency services results in loss of critical time, increasing the risk of fatalities.

---

## 💡 Solution

This system automates accident reporting by:
- Capturing live camera input from the frontend
- Allowing snapshot capture during an accident
- Sending the snapshot to the backend
- Automatically triggering an emergency email with:
  - Accident snapshot
  - Location details
  - Google Maps link
  - Timestamp

This reduces response time and improves chances of saving lives.

---

## 🧠 System Architecture

Frontend (React + Material UI):
- Live webcam streaming
- Snapshot capture
- Accident detected UI alert
- Sends snapshot to backend API

Backend (Flask + Python):
- Receives snapshot from frontend
- Stores snapshot securely
- Sends automated alert email
- Attaches image and location details

---

## 🛠️ Tech Stack

### Frontend
- React.js (Vite)
- Material UI (MUI)
- react-webcam
- Axios

### Backend
- Python
- Flask
- SMTP (Gmail)
- dotenv

### AI / Vision (Optional / Extendable)
- OpenCV
- YOLO (for future accident detection)

---

## ✨ Key Features

- 🎥 Live webcam feed in browser
- 📸 Snapshot capture on accident
- 🚨 Real-time accident alert UI
- 📩 Automatic email notification
- 📍 Location + Google Maps link
- 📎 Snapshot attached in email
- 💻 Clean & modern Material UI dashboard

---

