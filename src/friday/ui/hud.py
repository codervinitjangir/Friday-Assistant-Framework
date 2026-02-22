import sys
import math
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer, QRectF, QPointF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen, QRadialGradient, QFont, QBrush, QLinearGradient

from ..core.assistant import FridayAssistant

class WorkerSignals(QObject):
    update_status = pyqtSignal(str)
    show_alert = pyqtSignal(str, str)  # message, severity

class AlertNotification(QWidget):
    """Slide-in holographic alert notification."""
    def __init__(self, message: str, severity: str = "info"):
        super().__init__()
        self.message = message
        self.severity = severity
        
        # Severity colors
        self.colors = {
            "info": (QColor(0, 150, 255), QColor(0, 100, 200)),
            "warning": (QColor(255, 165, 0), QColor(255, 140, 0)),
            "critical": (QColor(255, 69, 0), QColor(200, 30, 0))
        }
        
        # Dynamic sizing based on text length
        char_width = 9  # Approximate character width
        min_width = 300
        max_width = 600
        text_width = len(message) * char_width + 100  # +100 for icon and padding
        self.popup_width = min(max(min_width, text_width), max_width)
        
        # Calculate height based on text wrapping
        lines = 1 + (len(message) * char_width) // (self.popup_width - 100)
        self.popup_height = min(80 + (lines - 1) * 20, 150)
        
        # Get screen geometry for center positioning
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Position: bottom-center
        x_pos = (screen_width - self.popup_width) // 2
        self._start_y = screen_height  # Start below screen
        self._target_y = screen_height - self.popup_height - 80  # Final position (80px from bottom)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(x_pos, self._start_y, self.popup_width, self.popup_height)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"y_pos")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Auto-dismiss timer
        self.dismiss_timer = QTimer()
        self.dismiss_timer.timeout.connect(self.slide_out)
        self.dismiss_timer.setSingleShot(True)
    
    @pyqtProperty(int)
    def y_pos(self):
        return self.y()
    
    @y_pos.setter
    def y_pos(self, value):
        self.move(self.x(), value)
        self.update()
    
    def slide_in(self):
        """Slide alert from bottom-center."""
        self.show()
        self.animation.setStartValue(self._start_y)
        self.animation.setEndValue(self._target_y)
        self.animation.start()
        self.dismiss_timer.start(5000)  # Auto-dismiss after 5s
    
    def slide_out(self):
        """Slide alert out and close."""
        self.animation.setStartValue(self.y())
        self.animation.setEndValue(self._start_y)
        self.animation.finished.connect(self.close)
        self.animation.start()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get colors
        color1, color2 = self.colors.get(self.severity, self.colors["info"])
        
        # Background with gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 200))
        gradient.setColorAt(1, QColor(0, 0, 0, 150))
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(color1, 2))
        painter.drawRoundedRect(10, 10, self.width() - 20, self.height() - 20, 10, 10)
        
        # Icon (simple circle with glow)
        painter.setPen(Qt.PenStyle.NoPen)
        glow = QRadialGradient(40, 40, 15)
        glow.setColorAt(0, color1)
        glow.setColorAt(1, QColor(color1.red(), color1.green(), color1.blue(), 0))
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(25, 25, 30, 30)
        
        # Text with word wrap
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(70, 20, self.width() - 80, self.height() - 30, 
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter | Qt.TextFlag.TextWordWrap, 
                        self.message)

class HolographicHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.signals.update_status.connect(self.update_status)
        self.signals.show_alert.connect(self.show_alert)
        
        # Alert tracking
        self.active_alerts = []
        
        # Window Setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("F.R.I.D.A.Y.")
        self.setGeometry(100, 100, 400, 400) # Square for circular core
        
        # Colors (FRIDAY Orange Theme)
        self.primary_color = QColor(255, 140, 0) # Dark Orange
        self.secondary_color = QColor(255, 69, 0) # Red Orange
        self.glow_color = QColor(255, 165, 0, 150)
        
        # Error state colors (Red)
        self.error_primary = QColor(220, 20, 60)  # Crimson
        self.error_secondary = QColor(255, 0, 0)  # Red
        self.error_glow = QColor(220, 20, 60, 150)
        
        # State
        self.current_message = "F.R.I.D.A.Y."
        self.assistant_state = "IDLE" 
        self.animation_angle = 0
        self.audio_level = 0  # Real-time mic volume (0-100)
        
        # CACHED PAINT OBJECTS (Performance Optimization)
        # Gradients
        self.cached_gradient_normal = None
        self.cached_gradient_error = None
        self._update_cached_gradients()  # Will be called once geometry is set
        
        # Pens
        self.cached_pen_outer = QPen(self.primary_color)
        self.cached_pen_outer.setWidth(6)
        self.cached_pen_outer.setCapStyle(Qt.PenCapStyle.RoundCap)
        
        self.cached_pen_outer_error = QPen(self.error_primary)
        self.cached_pen_outer_error.setWidth(6)
        self.cached_pen_outer_error.setCapStyle(Qt.PenCapStyle.RoundCap)
        
        self.cached_pen_inner = QPen(self.secondary_color)
        self.cached_pen_inner.setWidth(2)
        
        self.cached_pen_arc = QPen(self.primary_color)
        self.cached_pen_arc.setWidth(4)
        
        # Animation Timer (60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_frame)
        self.timer.start(16)
        
        self.assistant = None
        self.thread = None
        
        # Dragging
        self.oldPos = self.pos()

    def contextMenuEvent(self, event):
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        quit_action = menu.addAction("Quit F.R.I.D.A.Y.")
        action = menu.exec(event.globalPos())
        if action == quit_action:
            self.close_app()

    def close_app(self):
        if self.assistant:
            self.assistant.stop()
        self.close()
        QApplication.quit()

    def init_ui_elements(self):
        # We draw directly, but can keep input box if needed
        pass

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def start_assistant(self):
        self.assistant = FridayAssistant(callback_ui=self.emit_status)
        # Store STT reference for audio visualization
        self.stt_engine = self.assistant.stt
        # Connect monitor to visual alerts
        self.assistant.monitor.ui_callback = self.emit_alert
        self.thread = threading.Thread(target=self.assistant.start)
        self.thread.daemon = True
        self.thread.start()

    def emit_status(self, text):
        self.signals.update_status.emit(text)
    
    def emit_alert(self, message: str, severity: str = "info"):
        """Emit alert signal (thread-safe)."""
        self.signals.show_alert.emit(message, severity)
    
    def show_alert(self, message: str, severity: str = "info"):
        """Show visual alert notification."""
        alert = AlertNotification(message, severity)
        self.active_alerts.append(alert)
        alert.slide_in()
        
        # Clean up closed alerts
        self.active_alerts = [a for a in self.active_alerts if not a.isHidden()]

    def update_status(self, text):
        # Update text but keep FRIDAY as brand if idle
        if "Friday is Online" in text or "Idle" in text:
            self.current_message = "FRIDAY"
        else:
            self.current_message = text
            
        if "Listening" in text:
            self.assistant_state = "LISTENING"
        elif "Thinking" in text:
            self.assistant_state = "THINKING"
        elif "Friday:" in text or "Done" in text or "Speaking" in text:
            self.assistant_state = "SPEAKING"
        elif "Idle" in text:
            self.assistant_state = "IDLE"
        elif "Error" in text or "connection" in text.lower():
            self.assistant_state = "ERROR"
        
        self.update()

    def _update_cached_gradients(self):
        """Update gradient caches when geometry changes."""
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 20
        
        # Normal gradient
        self.cached_gradient_normal = QRadialGradient(center, radius)
        self.cached_gradient_normal.setColorAt(0, QColor(40, 20, 0, 180))
        self.cached_gradient_normal.setColorAt(0.7, QColor(255, 69, 0, 50))
        self.cached_gradient_normal.setColorAt(1, QColor(0, 0, 0, 0))
        
        # Error gradient
        self.cached_gradient_error = QRadialGradient(center, radius)
        self.cached_gradient_error.setColorAt(0, QColor(60, 0, 0, 180))
        self.cached_gradient_error.setColorAt(0.7, QColor(255, 0, 0, 50))
        self.cached_gradient_error.setColorAt(1, QColor(0, 0, 0, 0))
    
    def animate_frame(self):
        self.animation_angle += 1 # Slower rotation for elegance
        if self.animation_angle >= 360:
            self.animation_angle = 0
        
        # Update audio level from STT if available
        if hasattr(self, 'stt_engine') and self.stt_engine:
            self.audio_level = self.stt_engine.current_audio_level
        
        self.update()

    def paintEvent(self, event):
        from PyQt6.QtCore import QLine
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 20
        
        # Ensure gradients are initialized
        if self.cached_gradient_normal is None:
            self._update_cached_gradients()
        
        # Select colors and gradient based on state
        if self.assistant_state == "ERROR":
            primary = self.error_primary
            secondary = self.error_secondary
            glow = self.error_glow
            gradient = self.cached_gradient_error
            pen_outer = self.cached_pen_outer_error
        else:
            primary = self.primary_color
            secondary = self.secondary_color
            glow = self.glow_color
            gradient = self.cached_gradient_normal
            pen_outer = self.cached_pen_outer
        
        # 1. Background Glow / Shield
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius, radius)
        
        # 2. Outer Segmented Ring (use cached pen)
        painter.setPen(pen_outer)
        painter.save()
        painter.translate(center)
        painter.rotate(self.animation_angle)
        
        num_segments = 4
        gap = 10
        span = (360 / num_segments) - gap
        
        rect = QRectF(-radius, -radius, radius*2, radius*2)
        for i in range(num_segments):
            painter.rotate(360/num_segments)
            painter.drawArc(rect, 0, int(span * 16))
            
        painter.restore()
        
        # 3. Inner Rotating UI (use cached pen)
        painter.save()
        painter.translate(center)
        painter.rotate(-self.animation_angle * 2)
        
        painter.setPen(self.cached_pen_inner)
        r2 = radius * 0.65  # Reduced from 0.75 for tighter look
        rect2 = QRectF(-r2, -r2, r2*2, r2*2)
        painter.drawArc(rect2, 0, 270 * 16) # Broken circle

        
        # Ticks
        for i in range(0, 360, 30):
            # Use QLine for explicit integer coordinates
            line = QLine(0, int(-r2+10), 0, int(-r2-5))
            painter.drawLine(line)
            painter.rotate(30)
            
        painter.restore()
        
        # 4. Central Text "F.R.I.D.A.Y."
        font_size = 24 if len(self.current_message) < 15 else 12
        font = QFont("Orbitron", font_size, QFont.Weight.Bold)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        
        text_rect = QRectF(center.x() - 150, center.y() - 30, 300, 60)
        
        # Draw Text Glow
        painter.save()
        painter.setPen(self.primary_color)
        painter.setOpacity(0.5)
        painter.drawText(text_rect.translated(2, 2), Qt.AlignmentFlag.AlignCenter, self.current_message)
        painter.restore()
        
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.current_message)
        
        # 5. Real-Time Audio Visualizer
        painter.save()
        painter.translate(center)
        painter.setPen(self.cached_pen_arc)
        r3 = radius * 0.9
        
        # Use real mic volume when listening/speaking, else idle pulse
        if self.assistant_state == "LISTENING" or self.assistant_state == "SPEAKING":
            # Real-time audio level (0-100) → arc span (30-180 degrees)
            limit = 30 + int((self.audio_level / 100) * 150)
        else:
            # Idle pulse animation
            limit = 30 + int(math.sin(self.animation_angle/10) * 20)
            
        angle_start = 270 - (limit / 2)
        painter.drawArc(QRectF(-r3, -r3, r3*2, r3*2), int(angle_start * 16), int(limit * 16))
        painter.restore()

def run_gui():
    app = QApplication(sys.argv)
    hud = HolographicHUD()
    hud.show()
    hud.start_assistant()
    sys.exit(app.exec())
