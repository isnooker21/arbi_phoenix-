"""
🔥 ARBI PHOENIX - GUI Dashboard
Modern PyQt6-based trading dashboard with Start Trade functionality

"The Phoenix interface that never sleeps"
"""

import sys
import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QTextEdit, QTableWidget,
    QTableWidgetItem, QProgressBar, QGroupBox, QFrame, QSplitter,
    QTabWidget, QScrollArea, QMessageBox, QDialog, QFormLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QRect, QSize
)
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QPixmap, QIcon, QPainter,
    QLinearGradient, QBrush
)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PhoenixStyle:
    """Phoenix UI styling constants"""
    
    # Colors
    BACKGROUND = "#1E1E1E"
    SURFACE = "#2D2D2D"
    PRIMARY = "#FF6B35"  # Phoenix orange
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    ERROR = "#F44336"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B0B0B0"
    ACCENT = "#00BCD4"
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_LARGE = 14
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_SMALL = 10
    
    @staticmethod
    def get_stylesheet():
        """Get main application stylesheet"""
        return f"""
        QMainWindow {{
            background-color: {PhoenixStyle.BACKGROUND};
            color: {PhoenixStyle.TEXT_PRIMARY};
            font-family: {PhoenixStyle.FONT_FAMILY};
        }}
        
        QWidget {{
            background-color: {PhoenixStyle.BACKGROUND};
            color: {PhoenixStyle.TEXT_PRIMARY};
            font-size: {PhoenixStyle.FONT_SIZE_MEDIUM}px;
        }}
        
        QGroupBox {{
            background-color: {PhoenixStyle.SURFACE};
            border: 2px solid {PhoenixStyle.PRIMARY};
            border-radius: 8px;
            margin: 5px;
            padding-top: 15px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: {PhoenixStyle.PRIMARY};
        }}
        
        QPushButton {{
            background-color: {PhoenixStyle.PRIMARY};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
            font-size: {PhoenixStyle.FONT_SIZE_MEDIUM}px;
        }}
        
        QPushButton:hover {{
            background-color: #FF8A65;
        }}
        
        QPushButton:pressed {{
            background-color: #E64A19;
        }}
        
        QPushButton:disabled {{
            background-color: #555555;
            color: #888888;
        }}
        
        QPushButton.success {{
            background-color: {PhoenixStyle.SUCCESS};
        }}
        
        QPushButton.success:hover {{
            background-color: #66BB6A;
        }}
        
        QPushButton.warning {{
            background-color: {PhoenixStyle.WARNING};
            color: black;
        }}
        
        QPushButton.error {{
            background-color: {PhoenixStyle.ERROR};
        }}
        
        QLabel {{
            color: {PhoenixStyle.TEXT_PRIMARY};
        }}
        
        QLabel.title {{
            font-size: {PhoenixStyle.FONT_SIZE_LARGE}px;
            font-weight: bold;
            color: {PhoenixStyle.PRIMARY};
        }}
        
        QLabel.subtitle {{
            color: {PhoenixStyle.TEXT_SECONDARY};
        }}
        
        QLabel.success {{
            color: {PhoenixStyle.SUCCESS};
            font-weight: bold;
        }}
        
        QLabel.error {{
            color: {PhoenixStyle.ERROR};
            font-weight: bold;
        }}
        
        QTextEdit {{
            background-color: {PhoenixStyle.SURFACE};
            border: 1px solid {PhoenixStyle.PRIMARY};
            border-radius: 4px;
            padding: 5px;
            font-family: 'Consolas', monospace;
            font-size: {PhoenixStyle.FONT_SIZE_SMALL}px;
        }}
        
        QTableWidget {{
            background-color: {PhoenixStyle.SURFACE};
            alternate-background-color: #3A3A3A;
            border: 1px solid {PhoenixStyle.PRIMARY};
            border-radius: 4px;
            gridline-color: #555555;
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid #555555;
        }}
        
        QTableWidget::item:selected {{
            background-color: {PhoenixStyle.PRIMARY};
        }}
        
        QHeaderView::section {{
            background-color: {PhoenixStyle.PRIMARY};
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }}
        
        QProgressBar {{
            border: 2px solid {PhoenixStyle.PRIMARY};
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }}
        
        QProgressBar::chunk {{
            background-color: {PhoenixStyle.SUCCESS};
            border-radius: 3px;
        }}
        
        QTabWidget::pane {{
            border: 1px solid {PhoenixStyle.PRIMARY};
            background-color: {PhoenixStyle.SURFACE};
        }}
        
        QTabBar::tab {{
            background-color: {PhoenixStyle.BACKGROUND};
            color: {PhoenixStyle.TEXT_SECONDARY};
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {PhoenixStyle.PRIMARY};
            color: white;
        }}
        
        QTabBar::tab:hover {{
            background-color: #FF8A65;
            color: white;
        }}
        """

class StatusIndicator(QLabel):
    """Animated status indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.status = "disconnected"
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
    def set_status(self, status: str):
        """Set status: connected, disconnected, error, warning"""
        self.status = status
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        colors = {
            "connected": PhoenixStyle.SUCCESS,
            "disconnected": "#666666",
            "error": PhoenixStyle.ERROR,
            "warning": PhoenixStyle.WARNING
        }
        
        color = colors.get(self.status, "#666666")
        painter.setBrush(QBrush(QColor(color)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, 16, 16)

class MetricCard(QGroupBox):
    """Metric display card"""
    
    def __init__(self, title: str, value: str = "0", unit: str = "", parent=None):
        super().__init__(title, parent)
        self.setFixedHeight(120)
        
        layout = QVBoxLayout()
        
        # Value label
        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {PhoenixStyle.PRIMARY};
            margin: 10px;
        """)
        
        # Unit label
        self.unit_label = QLabel(unit)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.unit_label.setStyleSheet(f"""
            font-size: 12px;
            color: {PhoenixStyle.TEXT_SECONDARY};
        """)
        
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)
        self.setLayout(layout)
    
    def update_value(self, value: str, color: str = None):
        """Update the displayed value"""
        self.value_label.setText(value)
        if color:
            self.value_label.setStyleSheet(f"""
                font-size: 24px;
                font-weight: bold;
                color: {color};
                margin: 10px;
            """)

class TradingControlPanel(QGroupBox):
    """Main trading control panel with Start Trade button"""
    
    start_trading = pyqtSignal()
    stop_trading = pyqtSignal()
    pause_trading = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("🔥 Trading Control", parent)
        self.is_trading = False
        self.is_paused = False
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Status display
        status_layout = QHBoxLayout()
        
        self.status_indicator = StatusIndicator()
        self.status_label = QLabel("System Ready")
        self.status_label.setProperty("class", "title")
        
        status_layout.addWidget(self.status_indicator)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        # Main control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("🚀 START TRADE")
        self.start_button.setFixedHeight(50)
        self.start_button.setProperty("class", "success")
        self.start_button.clicked.connect(self.on_start_clicked)
        
        self.pause_button = QPushButton("⏸️ PAUSE")
        self.pause_button.setFixedHeight(50)
        self.pause_button.setProperty("class", "warning")
        self.pause_button.clicked.connect(self.on_pause_clicked)
        self.pause_button.setEnabled(False)
        
        self.stop_button = QPushButton("🛑 STOP")
        self.stop_button.setFixedHeight(50)
        self.stop_button.setProperty("class", "error")
        self.stop_button.clicked.connect(self.on_stop_clicked)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        
        # Trading mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Trading Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Conservative", "Balanced", "Aggressive"])
        self.mode_combo.setCurrentText("Balanced")
        
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        
        layout.addLayout(status_layout)
        layout.addLayout(button_layout)
        layout.addLayout(mode_layout)
        self.setLayout(layout)
    
    def on_start_clicked(self):
        """Handle start button click"""
        if not self.is_trading:
            self.start_trading.emit()
            self.set_trading_state(True)
        
    def on_pause_clicked(self):
        """Handle pause button click"""
        if self.is_trading and not self.is_paused:
            self.pause_trading.emit()
            self.is_paused = True
            self.pause_button.setText("▶️ RESUME")
            self.status_label.setText("Trading Paused")
            self.status_indicator.set_status("warning")
        else:
            self.start_trading.emit()
            self.is_paused = False
            self.pause_button.setText("⏸️ PAUSE")
            self.status_label.setText("Trading Active")
            self.status_indicator.set_status("connected")
    
    def on_stop_clicked(self):
        """Handle stop button click"""
        if self.is_trading:
            self.stop_trading.emit()
            self.set_trading_state(False)
    
    def set_trading_state(self, is_trading: bool):
        """Update UI based on trading state"""
        self.is_trading = is_trading
        self.is_paused = False
        
        if is_trading:
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.pause_button.setText("⏸️ PAUSE")
            self.status_label.setText("Trading Active")
            self.status_indicator.set_status("connected")
        else:
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Trading Stopped")
            self.status_indicator.set_status("disconnected")
    
    def set_connection_status(self, connected: bool):
        """Update connection status"""
        if connected:
            self.start_button.setEnabled(True)
            if not self.is_trading:
                self.status_label.setText("System Ready")
                self.status_indicator.set_status("connected")
        else:
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Broker Disconnected")
            self.status_indicator.set_status("error")

class OpportunityTable(QTableWidget):
    """Table for displaying arbitrage opportunities"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table()
        
    def setup_table(self):
        """Setup table structure"""
        headers = ["Triangle", "Direction", "Profit (Pips)", "Spread Cost", "Net Profit", "Confidence", "Status"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 100)
        self.setColumnWidth(5, 80)
        self.setColumnWidth(6, 80)
        
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
    def update_opportunities(self, opportunities: List):
        """Update table with new opportunities"""
        self.setRowCount(len(opportunities))
        
        for row, opp in enumerate(opportunities):
            # Triangle
            triangle_text = f"{opp.pair1[:3]}-{opp.pair2[:3]}-{opp.pair3[:3]}"
            self.setItem(row, 0, QTableWidgetItem(triangle_text))
            
            # Direction
            direction_item = QTableWidgetItem(opp.direction.upper())
            if opp.direction == "forward":
                direction_item.setForeground(QColor(PhoenixStyle.SUCCESS))
            else:
                direction_item.setForeground(QColor(PhoenixStyle.WARNING))
            self.setItem(row, 1, direction_item)
            
            # Profit (Pips)
            profit_item = QTableWidgetItem(f"{opp.profit_pips:.1f}")
            if opp.profit_pips > 0:
                profit_item.setForeground(QColor(PhoenixStyle.SUCCESS))
            else:
                profit_item.setForeground(QColor(PhoenixStyle.ERROR))
            self.setItem(row, 2, profit_item)
            
            # Spread Cost
            self.setItem(row, 3, QTableWidgetItem(f"{opp.spread_cost:.1f}"))
            
            # Net Profit
            net_item = QTableWidgetItem(f"{opp.net_profit:.1f}")
            if opp.net_profit > 0:
                net_item.setForeground(QColor(PhoenixStyle.SUCCESS))
            else:
                net_item.setForeground(QColor(PhoenixStyle.ERROR))
            self.setItem(row, 4, net_item)
            
            # Confidence
            confidence_item = QTableWidgetItem(f"{opp.confidence:.0%}")
            self.setItem(row, 5, confidence_item)
            
            # Status
            status_item = QTableWidgetItem("READY" if opp.is_executable else "WAIT")
            if opp.is_executable:
                status_item.setForeground(QColor(PhoenixStyle.SUCCESS))
            else:
                status_item.setForeground(QColor(PhoenixStyle.TEXT_SECONDARY))
            self.setItem(row, 6, status_item)

class PositionTable(QTableWidget):
    """Table for displaying active positions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table()
        
    def setup_table(self):
        """Setup table structure"""
        headers = ["Ticket", "Symbol", "Type", "Volume", "Open Price", "Current Price", "Profit", "Pips", "Time"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        for i, width in enumerate([80, 80, 60, 80, 100, 100, 100, 80, 120]):
            self.setColumnWidth(i, width)
        
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
    def update_positions(self, positions: List):
        """Update table with current positions"""
        self.setRowCount(len(positions))
        
        for row, pos in enumerate(positions):
            # Ticket
            self.setItem(row, 0, QTableWidgetItem(str(pos.ticket)))
            
            # Symbol
            self.setItem(row, 1, QTableWidgetItem(pos.symbol))
            
            # Type
            type_item = QTableWidgetItem(pos.type.upper())
            if pos.type == "buy":
                type_item.setForeground(QColor(PhoenixStyle.SUCCESS))
            else:
                type_item.setForeground(QColor(PhoenixStyle.ERROR))
            self.setItem(row, 2, type_item)
            
            # Volume
            self.setItem(row, 3, QTableWidgetItem(f"{pos.volume:.2f}"))
            
            # Open Price
            self.setItem(row, 4, QTableWidgetItem(f"{pos.open_price:.5f}"))
            
            # Current Price
            self.setItem(row, 5, QTableWidgetItem(f"{pos.current_price:.5f}"))
            
            # Profit
            profit_item = QTableWidgetItem(f"${pos.profit:.2f}")
            if pos.profit > 0:
                profit_item.setForeground(QColor(PhoenixStyle.SUCCESS))
            else:
                profit_item.setForeground(QColor(PhoenixStyle.ERROR))
            self.setItem(row, 6, profit_item)
            
            # Pips (simplified calculation)
            pips = (pos.current_price - pos.open_price) * 10000
            if pos.type == "sell":
                pips = -pips
            pips_item = QTableWidgetItem(f"{pips:.1f}")
            if pips > 0:
                pips_item.setForeground(QColor(PhoenixStyle.SUCCESS))
            else:
                pips_item.setForeground(QColor(PhoenixStyle.ERROR))
            self.setItem(row, 7, pips_item)
            
            # Time
            time_str = pos.open_time.strftime("%H:%M:%S")
            self.setItem(row, 8, QTableWidgetItem(time_str))

class ActivityLog(QTextEdit):
    """Activity log widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumBlockCount(1000)  # Limit to 1000 lines
        
    def add_log(self, message: str, level: str = "INFO"):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "INFO": PhoenixStyle.TEXT_PRIMARY,
            "SUCCESS": PhoenixStyle.SUCCESS,
            "WARNING": PhoenixStyle.WARNING,
            "ERROR": PhoenixStyle.ERROR
        }
        
        color = colors.get(level, PhoenixStyle.TEXT_PRIMARY)
        
        formatted_message = f'<span style="color: {color}">[{timestamp}] {message}</span>'
        self.append(formatted_message)
        
        # Auto-scroll to bottom
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class PhoenixDashboard(QMainWindow):
    """
    🔥 Main Phoenix Dashboard
    
    Modern trading interface with real-time monitoring and control
    """
    
    def __init__(self, arbitrage_engine=None, recovery_system=None, profit_harvester=None):
        super().__init__()
        
        self.logger = logging.getLogger("PhoenixDashboard")
        
        # Core components
        self.arbitrage_engine = arbitrage_engine
        self.recovery_system = recovery_system
        self.profit_harvester = profit_harvester
        
        # UI state
        self.is_trading = False
        
        # Setup UI
        self.setup_ui()
        self.setup_timers()
        
        # Apply styling
        self.setStyleSheet(PhoenixStyle.get_stylesheet())
        
        self.logger.info("🖥️ Phoenix Dashboard initialized")
    
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("🔥 Arbi Phoenix Dashboard")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel (Control + Metrics)
        left_panel = self.create_left_panel()
        content_splitter.addWidget(left_panel)
        
        # Right panel (Tables + Charts)
        right_panel = self.create_right_panel()
        content_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        content_splitter.setSizes([400, 1000])
        
        main_layout.addWidget(content_splitter)
        
        # Status bar
        self.statusBar().showMessage("Phoenix Dashboard Ready")
    
    def create_header(self):
        """Create header layout"""
        layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("🔥 ARBI PHOENIX")
        title_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {PhoenixStyle.PRIMARY};
            margin: 10px;
        """)
        
        # Subtitle
        subtitle_label = QLabel("The Ultimate Immortal Trading System")
        subtitle_label.setStyleSheet(f"""
            font-size: 14px;
            color: {PhoenixStyle.TEXT_SECONDARY};
            margin-left: 10px;
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addStretch()
        
        # Connection status
        self.connection_status = QLabel("🔌 Connecting...")
        layout.addWidget(self.connection_status)
        
        return layout
    
    def create_left_panel(self):
        """Create left control panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Trading Control Panel
        self.control_panel = TradingControlPanel()
        self.control_panel.start_trading.connect(self.start_trading)
        self.control_panel.stop_trading.connect(self.stop_trading)
        self.control_panel.pause_trading.connect(self.pause_trading)
        layout.addWidget(self.control_panel)
        
        # Metrics Grid
        metrics_group = QGroupBox("📊 Performance Metrics")
        metrics_layout = QGridLayout(metrics_group)
        
        # Create metric cards
        self.profit_card = MetricCard("Total Profit", "$0.00")
        self.opportunities_card = MetricCard("Opportunities", "0")
        self.success_rate_card = MetricCard("Success Rate", "0%")
        self.positions_card = MetricCard("Active Positions", "0")
        
        metrics_layout.addWidget(self.profit_card, 0, 0)
        metrics_layout.addWidget(self.opportunities_card, 0, 1)
        metrics_layout.addWidget(self.success_rate_card, 1, 0)
        metrics_layout.addWidget(self.positions_card, 1, 1)
        
        layout.addWidget(metrics_group)
        
        # Activity Log
        log_group = QGroupBox("📝 Activity Log")
        log_layout = QVBoxLayout(log_group)
        
        self.activity_log = ActivityLog()
        log_layout.addWidget(self.activity_log)
        
        layout.addWidget(log_group)
        
        return widget
    
    def create_right_panel(self):
        """Create right panel with tables and charts"""
        tab_widget = QTabWidget()
        
        # Opportunities Tab
        opportunities_tab = QWidget()
        opp_layout = QVBoxLayout(opportunities_tab)
        
        opp_header = QLabel("🎯 Arbitrage Opportunities")
        opp_header.setProperty("class", "title")
        opp_layout.addWidget(opp_header)
        
        self.opportunities_table = OpportunityTable()
        opp_layout.addWidget(self.opportunities_table)
        
        tab_widget.addTab(opportunities_tab, "Opportunities")
        
        # Positions Tab
        positions_tab = QWidget()
        pos_layout = QVBoxLayout(positions_tab)
        
        pos_header = QLabel("📈 Active Positions")
        pos_header.setProperty("class", "title")
        pos_layout.addWidget(pos_header)
        
        self.positions_table = PositionTable()
        pos_layout.addWidget(self.positions_table)
        
        tab_widget.addTab(positions_tab, "Positions")
        
        # Recovery Tab
        recovery_tab = QWidget()
        rec_layout = QVBoxLayout(recovery_tab)
        
        rec_header = QLabel("🔄 Recovery System")
        rec_header.setProperty("class", "title")
        rec_layout.addWidget(rec_header)
        
        # Recovery status
        self.recovery_status = QLabel("Recovery System: Inactive")
        rec_layout.addWidget(self.recovery_status)
        
        # Recovery progress
        self.recovery_progress = QProgressBar()
        rec_layout.addWidget(self.recovery_progress)
        
        rec_layout.addStretch()
        
        tab_widget.addTab(recovery_tab, "Recovery")
        
        # Charts Tab
        charts_tab = QWidget()
        charts_layout = QVBoxLayout(charts_tab)
        
        charts_header = QLabel("📊 Performance Charts")
        charts_header.setProperty("class", "title")
        charts_layout.addWidget(charts_header)
        
        # Placeholder for charts
        chart_placeholder = QLabel("Charts will be implemented here")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet(f"color: {PhoenixStyle.TEXT_SECONDARY}; font-size: 16px;")
        charts_layout.addWidget(chart_placeholder)
        
        tab_widget.addTab(charts_tab, "Charts")
        
        return tab_widget
    
    def setup_timers(self):
        """Setup update timers"""
        # Main update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(1000)  # Update every second
        
        # Connection check timer
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection)
        self.connection_timer.start(5000)  # Check every 5 seconds
    
    def start_trading(self):
        """Start trading system"""
        try:
            self.logger.info("🚀 Starting trading system from GUI...")
            self.is_trading = True
            
            # Start engines if available
            if self.arbitrage_engine:
                asyncio.create_task(self.arbitrage_engine.start())
            
            if self.recovery_system:
                asyncio.create_task(self.recovery_system.start())
            
            if self.profit_harvester:
                asyncio.create_task(self.profit_harvester.start())
            
            self.activity_log.add_log("🚀 Trading system started", "SUCCESS")
            self.statusBar().showMessage("Trading Active")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start trading: {e}")
            self.activity_log.add_log(f"❌ Failed to start trading: {e}", "ERROR")
            self.control_panel.set_trading_state(False)
    
    def stop_trading(self):
        """Stop trading system"""
        try:
            self.logger.info("🛑 Stopping trading system from GUI...")
            self.is_trading = False
            
            # Stop engines if available
            if self.arbitrage_engine:
                asyncio.create_task(self.arbitrage_engine.stop())
            
            if self.recovery_system:
                asyncio.create_task(self.recovery_system.stop())
            
            if self.profit_harvester:
                asyncio.create_task(self.profit_harvester.stop())
            
            self.activity_log.add_log("🛑 Trading system stopped", "WARNING")
            self.statusBar().showMessage("Trading Stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to stop trading: {e}")
            self.activity_log.add_log(f"❌ Failed to stop trading: {e}", "ERROR")
    
    def pause_trading(self):
        """Pause trading system"""
        try:
            self.logger.info("⏸️ Pausing trading system...")
            
            if self.arbitrage_engine:
                asyncio.create_task(self.arbitrage_engine.pause())
            
            self.activity_log.add_log("⏸️ Trading system paused", "WARNING")
            self.statusBar().showMessage("Trading Paused")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to pause trading: {e}")
            self.activity_log.add_log(f"❌ Failed to pause trading: {e}", "ERROR")
    
    def update_dashboard(self):
        """Update dashboard with current data"""
        try:
            # Update metrics
            self.update_metrics()
            
            # Update tables
            self.update_tables()
            
            # Update recovery status
            self.update_recovery_status()
            
        except Exception as e:
            self.logger.error(f"❌ Dashboard update failed: {e}")
    
    def update_metrics(self):
        """Update performance metrics"""
        try:
            total_profit = 0.0
            opportunities_count = 0
            success_rate = 0.0
            positions_count = 0
            
            if self.arbitrage_engine:
                status = self.arbitrage_engine.get_status()
                opportunities_count = status.get('opportunities_found', 0)
                success_rate = status.get('success_rate', 0.0)
                total_profit = status.get('total_profit', 0.0)
                positions_count = status.get('active_positions', 0)
            
            # Update cards
            profit_color = PhoenixStyle.SUCCESS if total_profit >= 0 else PhoenixStyle.ERROR
            self.profit_card.update_value(f"${total_profit:.2f}", profit_color)
            
            self.opportunities_card.update_value(str(opportunities_count))
            self.success_rate_card.update_value(f"{success_rate:.1f}%")
            self.positions_card.update_value(str(positions_count))
            
        except Exception as e:
            self.logger.error(f"❌ Metrics update failed: {e}")
    
    def update_tables(self):
        """Update data tables"""
        try:
            # Update opportunities table
            if self.arbitrage_engine:
                opportunities = self.arbitrage_engine.get_opportunities()
                self.opportunities_table.update_opportunities(opportunities)
                
                # Update positions table
                positions = self.arbitrage_engine.get_positions()
                self.positions_table.update_positions(positions)
            
        except Exception as e:
            self.logger.error(f"❌ Tables update failed: {e}")
    
    def update_recovery_status(self):
        """Update recovery system status"""
        try:
            if self.recovery_system:
                status = self.recovery_system.get_status()
                recovery_status = status.get('status', 'inactive')
                active_recoveries = status.get('active_recoveries', 0)
                success_rate = status.get('success_rate', 0.0)
                
                status_text = f"Recovery System: {recovery_status.title()}"
                if active_recoveries > 0:
                    status_text += f" ({active_recoveries} active)"
                
                self.recovery_status.setText(status_text)
                self.recovery_progress.setValue(int(success_rate))
            
        except Exception as e:
            self.logger.error(f"❌ Recovery status update failed: {e}")
    
    def check_connection(self):
        """Check broker connection status"""
        try:
            is_connected = False
            
            if (self.arbitrage_engine and 
                hasattr(self.arbitrage_engine, 'pair_scanner') and
                self.arbitrage_engine.pair_scanner):
                
                connection_status = self.arbitrage_engine.pair_scanner.get_connection_status()
                is_connected = connection_status.get('is_connected', False)
                status_text = connection_status.get('status', 'Unknown')
                
                if is_connected:
                    self.connection_status.setText(f"🟢 {status_text}")
                    self.connection_status.setStyleSheet(f"color: {PhoenixStyle.SUCCESS}")
                else:
                    self.connection_status.setText(f"🔴 {status_text}")
                    self.connection_status.setStyleSheet(f"color: {PhoenixStyle.ERROR}")
                
                # Update control panel
                self.control_panel.set_connection_status(is_connected)
            
        except Exception as e:
            self.logger.error(f"❌ Connection check failed: {e}")
    
    async def start(self):
        """Start the dashboard"""
        self.logger.info("🖥️ Starting Phoenix Dashboard...")
        
        # Show the window
        self.show()
        
        # Initial log message
        self.activity_log.add_log("🔥 Phoenix Dashboard started", "SUCCESS")
        self.activity_log.add_log("Ready for trading operations", "INFO")
        
        # Check initial connection
        self.check_connection()
    
    async def stop(self):
        """Stop the dashboard"""
        self.logger.info("🖥️ Stopping Phoenix Dashboard...")
        
        # Stop timers
        self.update_timer.stop()
        self.connection_timer.stop()
        
        # Close window
        self.close()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.is_trading:
            reply = QMessageBox.question(
                self, 
                'Confirm Exit',
                'Trading is active. Are you sure you want to exit?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_trading()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """Main function for testing the dashboard"""
    app = QApplication(sys.argv)
    
    # Create and show dashboard
    dashboard = PhoenixDashboard()
    dashboard.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
