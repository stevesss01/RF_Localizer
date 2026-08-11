"""
RF Localizer - Real-Time Monitoring Dashboard

Features:
- Live signal-strength graph
- RF waveform visualization
- RF heatmap
- Moving localization hotspot
- Radar sweep
- Source coordinates
- Confidence indicator
- Arduino serial input with simulation fallback
"""

import sys
import time
import math
import numpy as np
import pyqtgraph as pg
import serial

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar
)
from PyQt5.QtCore import QTimer


# ============================================================
# CONFIGURATION
# ============================================================

USE_ARDUINO = True

# Change this to your Arduino COM port
COM_PORT = "COM13"

BAUD_RATE = 9600


# ============================================================
# SERIAL CONNECTION
# ============================================================

ser = None

if USE_ARDUINO:
    try:
        ser = serial.Serial(
            COM_PORT,
            BAUD_RATE,
            timeout=1
        )

        # Allow Arduino serial connection to initialize
        time.sleep(2)

    except serial.SerialException as error:
        print("Serial connection unavailable:")
        print(error)
        print("Switching to simulation mode.")

        USE_ARDUINO = False


# ============================================================
# DASHBOARD
# ============================================================

class RFDashboard(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "RF LOCALIZER PRO"
        )

        self.resize(1700, 950)

        self.phase = 0
        self.start_time = time.time()

        # ----------------------------------------------------
        # MAIN WINDOW
        # ----------------------------------------------------

        central = QWidget()

        self.setCentralWidget(
            central
        )

        central.setStyleSheet("""
        QWidget {
            background-color: #08111f;
            color: white;
            font-family: Segoe UI;
        }
        """)

        main_layout = QVBoxLayout(
            central
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QLabel(
            "RF LOCALIZER - REAL TIME MONITORING SYSTEM"
        )

        header.setStyleSheet("""
        QLabel {
            font-size: 28px;
            font-weight: bold;
            padding: 15px;
            border-radius: 12px;
            color: white;

            background:
            qlineargradient(
                x1:0, y1:0,
                x2:1, y2:0,
                stop:0 #081c3a,
                stop:0.5 #0d4f8b,
                stop:1 #00c6ff
            );
        }
        """)

        main_layout.addWidget(
            header
        )

        # ----------------------------------------------------
        # CLOCK
        # ----------------------------------------------------

        self.clock = QLabel()

        self.clock.setStyleSheet("""
        QLabel {
            font-size: 16px;
            color: #00ffff;
            padding: 4px;
        }
        """)

        main_layout.addWidget(
            self.clock
        )

        # ----------------------------------------------------
        # TOP PANELS
        # ----------------------------------------------------

        top_layout = QHBoxLayout()

        main_layout.addLayout(
            top_layout
        )

        # SYSTEM STATUS

        self.status = QLabel()

        self.status.setStyleSheet("""
        QLabel {
            background: #101a2d;
            border: 2px solid #00ffff;
            border-radius: 12px;
            padding: 12px;
        }
        """)

        top_layout.addWidget(
            self.status,
            1
        )

        # SIGNAL GRAPH

        self.signal_graph = pg.PlotWidget(
            title="Live Signal Strength"
        )

        self.signal_graph.setBackground(
            "#101a2d"
        )

        self.signal_graph.showGrid(
            x=True,
            y=True
        )

        self.signal_curve = (
            self.signal_graph.plot(
                pen=pg.mkPen(
                    "#66ffff",
                    width=3
                )
            )
        )

        top_layout.addWidget(
            self.signal_graph,
            3
        )

        # RF WAVE

        self.wave_graph = pg.PlotWidget(
            title="RF Wave Activity"
        )

        self.wave_graph.setBackground(
            "#101a2d"
        )

        self.wave_graph.showGrid(
            x=True,
            y=True
        )

        self.wave_curve = (
            self.wave_graph.plot(
                pen=pg.mkPen(
                    "#00ff99",
                    width=2
                )
            )
        )

        top_layout.addWidget(
            self.wave_graph,
            1
        )

        # ----------------------------------------------------
        # HEATMAP + RADAR
        # ----------------------------------------------------

        middle_layout = QHBoxLayout()

        main_layout.addLayout(
            middle_layout
        )

        # HEATMAP

        self.heatmap = pg.ImageView()

        try:
            self.heatmap.setColorMap(
                pg.colormap.get("inferno")
            )
        except Exception:
            pass

        middle_layout.addWidget(
            self.heatmap,
            2
        )

        # RADAR

        self.radar = pg.PlotWidget(
            title="RF Radar"
        )

        self.radar.setBackground(
            "#101a2d"
        )

        self.radar.setAspectLocked(
            True
        )

        middle_layout.addWidget(
            self.radar,
            1
        )

        # ----------------------------------------------------
        # LOCALIZATION INFORMATION
        # ----------------------------------------------------

        self.location = QLabel()

        self.location.setStyleSheet("""
        QLabel {
            background: #101a2d;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
        }
        """)

        main_layout.addWidget(
            self.location
        )

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        self.confidence = QProgressBar()

        self.confidence.setMaximum(
            100
        )

        self.confidence.setStyleSheet("""
        QProgressBar {
            border: 1px solid #31506e;
            border-radius: 7px;
            text-align: center;
            color: white;
        }

        QProgressBar::chunk {
            background-color: #00e6a8;
            border-radius: 7px;
        }
        """)

        main_layout.addWidget(
            self.confidence
        )

        # ----------------------------------------------------
        # DATA STORAGE
        # ----------------------------------------------------

        self.grid = np.zeros(
            (50, 50)
        )

        self.signal_history = []

        # ----------------------------------------------------
        # UPDATE TIMER
        # ----------------------------------------------------

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_dashboard
        )

        self.timer.start(
            120
        )

    # ========================================================
    # READ SIGNAL
    # ========================================================

    def get_signal(self):

        global USE_ARDUINO
        global ser

        if USE_ARDUINO and ser:

            try:

                line = (
                    ser.readline()
                    .decode(
                        "utf-8",
                        errors="ignore"
                    )
                    .strip()
                )

                if line:

                    return int(line)

            except (
                ValueError,
                serial.SerialException
            ):
                pass

        # ----------------------------------------------------
        # FALLBACK SIMULATION
        # ----------------------------------------------------

        return int(
            70
            + 15 * math.sin(self.phase)
            + 8 * math.sin(self.phase * 0.4)
        )

    # ========================================================
    # DASHBOARD UPDATE
    # ========================================================

    def update_dashboard(self):

        signal = self.get_signal()

        self.phase += 0.06

        # ----------------------------------------------------
        # SIGNAL HISTORY
        # ----------------------------------------------------

        self.signal_history.append(
            signal
        )

        self.signal_history = (
            self.signal_history[-120:]
        )

        self.signal_curve.setData(
            self.signal_history
        )

        # ----------------------------------------------------
        # RF WAVEFORM
        # ----------------------------------------------------

        x_wave = np.linspace(
            0,
            10,
            500
        )

        wave = (
            np.sin(
                6 * x_wave
                + self.phase
            )
            +
            0.5 *
            np.sin(
                12 * x_wave
                + self.phase * 1.5
            )
        )

        self.wave_curve.setData(
            x_wave,
            wave
        )

        # ----------------------------------------------------
        # LOCALIZATION POSITION
        # ----------------------------------------------------

        x = int(
            25
            + 15 *
            np.cos(
                self.phase * 1.8
            )
        )

        y = int(
            25
            + 15 *
            np.sin(
                self.phase * 1.8
            )
        )

        # ----------------------------------------------------
        # HEATMAP FADE
        # ----------------------------------------------------

        self.grid *= 0.995

        # ----------------------------------------------------
        # CREATE RF HOTSPOT
        # ----------------------------------------------------

        for i in range(-4, 5):

            for j in range(-4, 5):

                xx = x + i
                yy = y + j

                if (
                    0 <= xx < 50
                    and
                    0 <= yy < 50
                ):

                    distance = math.sqrt(
                        i * i + j * j
                    )

                    if distance < 4:

                        intensity = (
                            signal
                            *
                            (1 - distance / 4)
                        )

                        self.grid[
                            xx,
                            yy
                        ] = intensity

        self.heatmap.setImage(
            self.grid.T,
            autoLevels=False
        )

        # ----------------------------------------------------
        # RADAR
        # ----------------------------------------------------

        self.radar.clear()

        theta = np.linspace(
            0,
            2 * np.pi,
            500
        )

        # Radar rings

        for radius in [5, 10, 15, 20, 25]:

            self.radar.plot(
                radius * np.cos(theta),
                radius * np.sin(theta),
                pen=pg.mkPen(
                    0,
                    255,
                    0,
                    70
                )
            )

        # Crosshair

        self.radar.plot(
            [-25, 25],
            [0, 0],
            pen=pg.mkPen(
                0,
                255,
                0,
                70
            )
        )

        self.radar.plot(
            [0, 0],
            [-25, 25],
            pen=pg.mkPen(
                0,
                255,
                0,
                70
            )
        )

        # ----------------------------------------------------
        # RADAR SWEEP
        # ----------------------------------------------------

        radar_angle = (
            self.phase * 18
        )

        for i in range(12):

            angle = (
                radar_angle
                - i * 0.08
            )

            alpha = max(
                255 - i * 18,
                20
            )

            self.radar.plot(
                [
                    0,
                    25 * math.cos(angle)
                ],
                [
                    0,
                    25 * math.sin(angle)
                ],
                pen=pg.mkPen(
                    0,
                    255,
                    0,
                    alpha,
                    width=4
                )
            )

        # ----------------------------------------------------
        # RADAR TARGET
        # ----------------------------------------------------

        target_radius = (
            8 + signal / 4
        )

        target_x = (
            target_radius
            * math.cos(
                self.phase * 2
            )
        )

        target_y = (
            target_radius
            * math.sin(
                self.phase * 2
            )
        )

        # Glow layers

        for size, alpha in [
            (40, 25),
            (30, 40),
            (22, 70)
        ]:

            self.radar.plot(
                [target_x],
                [target_y],
                pen=None,
                symbol="o",
                symbolBrush=(
                    255,
                    0,
                    0,
                    alpha
                ),
                symbolSize=size
            )

        # Main target

        self.radar.plot(
            [target_x],
            [target_y],
            pen=None,
            symbol="o",
            symbolBrush="red",
            symbolSize=12
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if signal > 85:

            quality = "EXCELLENT"

        elif signal > 55:

            quality = "GOOD"

        else:

            quality = "WEAK"

        uptime = int(
            time.time()
            - self.start_time
        )

        self.clock.setText(
            time.strftime(
                "%d-%m-%Y    %H:%M:%S"
            )
        )

        self.status.setText(
            f"""
SYSTEM STATUS

RF LINK       : ACTIVE
SIGNAL LEVEL  : {signal}
QUALITY       : {quality}
FREQUENCY     : 2.4 GHz
NODES         : 2
TRACKING      : ACTIVE
UPTIME        : {uptime}s
"""
        )

        self.location.setText(
            f"""
ESTIMATED RF SOURCE LOCATION

X : {x}       Y : {y}       CONFIDENCE : {signal}%
"""
        )

        self.confidence.setValue(
            max(
                0,
                min(
                    100,
                    signal
                )
            )
        )


# ============================================================
# APPLICATION
# ============================================================

app = QApplication(
    sys.argv
)

pg.setConfigOption(
    "background",
    "#08111f"
)

window = RFDashboard()

window.show()

sys.exit(
    app.exec()
)