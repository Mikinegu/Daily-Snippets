# 🎶 Offline Music Scheduler for Factory PA Systems

### 🗓️ Day 1 — Core Automation System (Offline / No GUI / No Bluetooth Yet)

---

## 📌 Overview

This is an **offline, automated music scheduling system** designed for factory Bluetooth PA systems. It plays music automatically based on time and day, pauses during breaks, and skips playback on Sundays or holidays — all without internet access.

This is part of a **365-day GitHub coding challenge**. Each day adds a practical feature to a real-world project.

---

## ✅ Features Implemented

- ⏰ **Automated Start/Stop** at clock-in and clock-out times
- 🍽️ **Lunch break pause and resume**
- 📅 **Day-specific playlists** from folders
- 🔕 **Skips Sundays and holiday dates**
- 💾 Easy config with a single `config.json`
- 🎵 Uses `pygame` for offline `.mp3` playback
- 📂 Easy song management — just drag & drop `.mp3` files into folders
- 📦 Fully offline, no GUI, no internet dependency

---

## 🗂️ Folder Structure

project/
├── main.py
├── config.json
└── playlists/
├── monday/
├── tuesday/
├── wednesday/
├── thursday/
├── friday/
└── sunday/


> Add your `.mp3` files to each day’s folder.

---

## 🧠 Configuration

All schedule and control logic is managed through `config.json`.

### Example `config.json`:

```json
{
  "blackout_days": ["sunday"],
  "holidays": {
    "2025-09-11": "Enkutatash (New Year)",
    "2025-12-25": "Christmas"
  },
  "bluetooth_device_name": "Factory PA",
  "monday": {
    "clock_in": "08:30",
    "lunch_break": "12:00",
    "lunch_resume": "13:00",
    "clock_out": "17:00"
  }
}
