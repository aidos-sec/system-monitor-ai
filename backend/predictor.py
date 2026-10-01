"""Прогноз нагрузки: сглаживание (moving average) + линейная регрессия.

v1.2: исправлена ошибка сериализации — numpy-типы явно приводятся
к обычным Python-типам перед отправкой в JSON.
"""
import numpy as np
from collections import deque

WINDOW = 120        # сколько секунд истории храним
SMOOTH = 30         # окно сглаживания: среднее за 30 секунд
HORIZON = 300       # горизонт прогноза: 5 минут
THRESHOLD = 90.0    # порог тревоги по CPU, %

class Predictor:
    def __init__(self):
        self.history = deque(maxlen=WINDOW)

    def add(self, timestamp: float, value: float):
        self.history.append((timestamp, value))

    def _smooth(self, y):
        """Скользящее среднее: каждую точку заменяем средним вокруг неё."""
        kernel = np.ones(SMOOTH) / SMOOTH
        pad = SMOOTH - 1
        ypad = np.concatenate([np.full(pad, y[0]), y])
        return np.convolve(ypad, kernel, mode="valid")

    def predict(self) -> dict:
        if len(self.history) < SMOOTH + 5:
            return {"ready": False}

        data = np.array(self.history)
        t = data[:, 0] - data[0, 0]
        y = self._smooth(data[:, 1])

        k, b = np.polyfit(t, y, 1)
        # важно: приводим numpy-числа к обычным float
        k, b = float(k), float(b)

        future_t = float(t[-1]) + HORIZON
        predicted = max(0.0, min(100.0, k * future_t + b))

        rising = k > 0.05
        alert = bool(rising and predicted >= THRESHOLD)

        time_to_threshold = None
        if rising:
            t_cross = (THRESHOLD - b) / k
            if t_cross > t[-1]:
                time_to_threshold = int(round(t_cross - t[-1]))

        return {
            "ready": True,
            "horizon_sec": HORIZON,
            "predicted_cpu": round(float(predicted), 2),
            "trend": "up" if k > 0.05 else ("down" if k < -0.05 else "stable"),
            "time_to_threshold_sec": time_to_threshold,
            "alert": alert,
        }

predictor = Predictor()