# 🖥️ Real-time System Monitoring with AI Predictions

Real-time system monitoring dashboard that predicts CPU overload **before it happens**.
Collects system metrics every second, streams them via WebSocket, and uses time-series
forecasting to alert when CPU is expected to cross a critical threshold within 5 minutes.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📊 **Live dashboard** — CPU, RAM and disk usage streamed every second via WebSocket
- 🤖 **AI prediction** — linear regression on a smoothed time series forecasts CPU load 5 minutes ahead
- 🔔 **Smart alerts** — fires only under sustained real load (moving-average smoothing eliminates false positives)
- 📈 **Trend detection** — up / down / stable with estimated time-to-threshold
- ⚡ **Zero config** — runs locally with one command, no external services needed

## 🎬 Demo

*(gif will be here)*

| Idle (no false alerts) | Under load (alert triggered) |
|---|---|
| *(screenshot)* | *(screenshot)* |

## 🚀 Quick Start

```bash
pip install -r requirements.txt
cd backend
python main.py          # on Windows use: py main.py
