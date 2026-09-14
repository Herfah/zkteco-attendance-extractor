"""Main GUI Application for ZKTeco Attendance Extractor"""
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QSpinBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QFileDialog, QProgressBar, QDialog,
    QComboBox, QCheckBox, QDateEdit, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QColor
from datetime import datetime, timedelta
import logging

from config import config
from zk_device import ZKTecoDevice
from database import AttendanceDB
from export_handler import ExportHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyncWorker(QThread):
    """Worker thread for syncing attendance data"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, device_ip, device_port):
        super().__init__()
        self.device_ip = device_ip
        self.device_port = device_port
    
    def run(self):
        try:
            self.progress.emit("Connecting to device...")
            device = ZKTecoDevice(self.device_ip, self.device_port)
            
            if not device.connect():
                self.finished.emit(False, "Failed to connect to device")
                return
            
            self.progress.emit("Fetching attendance records...")
            attendance = device.get_attendance_records()
            
            if not attendance:
                device.disconnect()
                self.finished.emit(False, "No records found or error reading data")
                return
            
            self.progress.emit(f"Saving {len(attendance)} records to database...")
            db = AttendanceDB()
            saved_count = 0
            
            for record in attendance:
                if db.insert_attendance(
                    user_id=record.user_id,
                    user_name=record.user_name or "Unknown",
                    timestamp=record.timestamp,
                    status=record.status,
                    device_ip=self.device_ip
                ):
                    saved_count += 1
            
            db.log_sync(self.device_ip, saved_count, "success")
            device.disconnect()
            
            message = f"Successfully synced {saved_count} records from {len(attendance)} fetched"
            self.finished.emit(True, message)
        except Exception as e:
            logger.error(f"Sync error: {e}")
            self.finished.emit(False, f"Error: {str(e)}")

class SettingsDialog(QDialog):
    """Settings dialog for device configuration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Device Settings")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout()
        
        self.ip_input = QLineEdit(config.DEVICE_IP)
        self.port_input = QSpinBox()
        self.port_input.setValue(config.DEVICE_PORT)
        self.port_input.setRange(1, 65535)
        
        self.timeout_input = QSpinBox()
        self.timeout_input.setValue(config.DEVICE_TIMEOUT)
        self.timeout_input.setRange(1, 60)
        self.timeout_input.setSuffix(" seconds")
        
        layout.addRow("Device IP:", self.ip_input)
        layout.addRow("Port:", self.port_input)
        layout.addRow("Timeout:", self.timeout_input)
        
        button_layout = QHBoxLayout()
        test_btn = QPushButton("Test Connection")
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        test_btn.clicked.connect(self.test_connection)
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(test_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
    
    def test_connection(self):
        ip = self.ip_input.text()
        port = self.port_input.value()
        
        device = ZKTecoDevice(ip, port)
        if device.test_connection():
            QMessageBox.information(self, "Success", "Connection test successful!")
        else:
            QMessageBox.warning(self, "Failed", "Could not connect to device")

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.setGeometry(100, 100, 1200, 700)
        self.db = AttendanceDB()
        self.export_handler = ExportHandler()
        self.sync_worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel(config.APP_NAME)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_btn)
        
        main_layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_sync_tab(), "Sync")
        tabs.addTab(self.create_view_tab(), "View Data")
        tabs.addTab(self.create_export_tab(), "Export")
        tabs.addTab(self.create_device_tab(), "Device Info")
        
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
    
    def create_sync_tab(self):
        """Create sync tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Status group
        status_group = QGroupBox("Sync Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Ready to sync")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        status_group.setLayout(status_layout)
        
        # Sync buttons
        button_layout = QHBoxLayout()
        sync_btn = QPushButton("🔄 Sync Now")
        sync_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        sync_btn.clicked.connect(self.sync_attendance)
        
        clear_btn = QPushButton("🗑️ Clear Old Records")
        clear_btn.clicked.connect(self.clear_old_records)
        
        button_layout.addWidget(sync_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addWidget(status_group)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_view_tab(self):
        """Create view data tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filter group
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("From:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel("To:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date)
        
        filter_layout.addWidget(QLabel("User ID:"))
        self.user_filter = QLineEdit()
        self.user_filter.setPlaceholderText("Leave empty to see all")
        filter_layout.addWidget(self.user_filter)
        
        apply_filter_btn = QPushButton("Apply Filter")
        apply_filter_btn.clicked.connect(self.apply_filters)
        filter_layout.addWidget(apply_filter_btn)
        
        filter_group.setLayout(filter_layout)
        
        # Table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(6)
        self.data_table.setHorizontalHeaderLabels(['ID', 'User ID', 'Name', 'Timestamp', 'Status', 'Device IP'])
        self.data_table.resizeColumnsToContents()
        
        layout.addWidget(filter_group)
        layout.addWidget(self.data_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_export_tab(self):
        """Create export tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Export options
        options_group = QGroupBox("Export Options")
        options_layout = QVBoxLayout()
        
        self.export_all_checkbox = QCheckBox("Export all records")
        self.export_all_checkbox.setChecked(True)
        self.export_all_checkbox.stateChanged.connect(self.toggle_date_range)
        options_layout.addWidget(self.export_all_checkbox)
        
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("From:"))
        self.export_start_date = QDateEdit()
        self.export_start_date.setDate(QDate.currentDate().addDays(-30))
        self.export_start_date.setEnabled(False)
        date_layout.addWidget(self.export_start_date)
        
        date_layout.addWidget(QLabel("To:"))
        self.export_end_date = QDateEdit()
        self.export_end_date.setDate(QDate.currentDate())
        self.export_end_date.setEnabled(False)
        date_layout.addWidget(self.export_end_date)
        
        options_layout.addLayout(date_layout)
        options_group.setLayout(options_layout)
        
        # Export buttons
        button_layout = QHBoxLayout()
        
        csv_btn = QPushButton("📄 Export to CSV")
        csv_btn.clicked.connect(self.export_csv)
        
        excel_btn = QPushButton("📊 Export to Excel")
        excel_btn.clicked.connect(self.export_excel)
        
        summary_btn = QPushButton("📈 Export Summary Report")
        summary_btn.clicked.connect(self.export_summary)
        
        button_layout.addWidget(csv_btn)
        button_layout.addWidget(excel_btn)
        button_layout.addWidget(summary_btn)
        button_layout.addStretch()
        
        layout.addWidget(options_group)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_device_tab(self):
        """Create device info tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_group = QGroupBox("Device Information")
        info_layout = QVBoxLayout()
        
        self.device_info_label = QLabel("Click 'Refresh' to load device information")
        self.device_info_label.setWordWrap(True)
        info_layout.addWidget(self.device_info_label)
        
        info_group.setLayout(info_layout)
        
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Refresh Device Info")
        refresh_btn.clicked.connect(self.refresh_device_info)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        
        layout.addWidget(info_group)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def sync_attendance(self):
        """Start attendance sync"""
        if self.sync_worker and self.sync_worker.isRunning():
            QMessageBox.warning(self, "Already Syncing", "A sync operation is already in progress")
            return
        
        self.sync_worker = SyncWorker(config.DEVICE_IP, config.DEVICE_PORT)
        self.sync_worker.progress.connect(self.update_status)
        self.sync_worker.finished.connect(self.sync_finished)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.sync_worker.start()
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.setText(message)
    
    def sync_finished(self, success, message):
        """Handle sync completion"""
        self.progress_bar.setVisible(False)
        self.status_label.setText(message)
        
        if success:
            QMessageBox.information(self, "Sync Complete", message)
        else:
            QMessageBox.warning(self, "Sync Failed", message)
    
    def apply_filters(self):
        """Apply filters and load data"""
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        user_id = self.user_filter.text().strip()
        
        if user_id:
            records = self.db.get_records_by_user(user_id)
        else:
            records = self.db.get_records_by_date(start_date, end_date)
        
        self.populate_table(records)
    
    def populate_table(self, records):
        """Populate data table"""
        self.data_table.setRowCount(0)
        
        for row, record in enumerate(records):
            self.data_table.insertRow(row)
            
            status_text = "Check-In" if record[4] == 0 else "Check-Out"
            
            self.data_table.setItem(row, 0, QTableWidgetItem(str(record[0])))
            self.data_table.setItem(row, 1, QTableWidgetItem(str(record[1])))
            self.data_table.setItem(row, 2, QTableWidgetItem(str(record[2])))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(record[3])))
            self.data_table.setItem(row, 4, QTableWidgetItem(status_text))
            self.data_table.setItem(row, 5, QTableWidgetItem(str(record[5])))
        
        self.data_table.resizeColumnsToContents()
    
    def export_csv(self):
        """Export to CSV"""
        records = self.get_export_records()
        if not records:
            QMessageBox.warning(self, "No Data", "No records to export")
            return
        
        filepath = self.export_handler.export_to_csv(records)
        if filepath:
            QMessageBox.information(self, "Success", f"Exported to: {filepath}")
        else:
            QMessageBox.warning(self, "Error", "Failed to export data")
    
    def export_excel(self):
        """Export to Excel"""
        records = self.get_export_records()
        if not records:
            QMessageBox.warning(self, "No Data", "No records to export")
            return
        
        filepath = self.export_handler.export_to_excel(records)
        if filepath:
            QMessageBox.information(self, "Success", f"Exported to: {filepath}")
        else:
            QMessageBox.warning(self, "Error", "Failed to export data")
    
    def export_summary(self):
        """Export summary report"""
        records = self.get_export_records()
        if not records:
            QMessageBox.warning(self, "No Data", "No records to export")
            return
        
        filepath = self.export_handler.export_summary_report(records)
        if filepath:
            QMessageBox.information(self, "Success", f"Exported to: {filepath}")
        else:
            QMessageBox.warning(self, "Error", "Failed to export data")
    
    def get_export_records(self):
        """Get records for export"""
        if self.export_all_checkbox.isChecked():
            return self.db.get_all_records()
        else:
            start_date = self.export_start_date.date().toString("yyyy-MM-dd")
            end_date = self.export_end_date.date().toString("yyyy-MM-dd")
            return self.db.get_records_by_date(start_date, end_date)
    
    def toggle_date_range(self):
        """Toggle date range enabled state"""
        enabled = not self.export_all_checkbox.isChecked()
        self.export_start_date.setEnabled(enabled)
        self.export_end_date.setEnabled(enabled)
    
    def clear_old_records(self):
        """Clear old records"""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete attendance records older than 1 year?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            deleted = self.db.delete_old_records(365)
            QMessageBox.information(self, "Success", f"Deleted {deleted} old records")
    
    def refresh_device_info(self):
        """Refresh device information"""
        device = ZKTecoDevice()
        if device.connect():
            info = device.get_device_info()
            device.disconnect()
            
            if info:
                info_text = f"""
                Serial Number: {info.get('serial_number', 'N/A')}
                Device Name: {info.get('device_name', 'N/A')}
                Platform: {info.get('platform', 'N/A')}
                Firmware Version: {info.get('firmware_version', 'N/A')}
                """
                self.device_info_label.setText(info_text)
            else:
                self.device_info_label.setText("Could not retrieve device information")
        else:
            self.device_info_label.setText("Failed to connect to device")
    
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            config.DEVICE_IP = dialog.ip_input.text()
            config.DEVICE_PORT = dialog.port_input.value()
            config.DEVICE_TIMEOUT = dialog.timeout_input.value()
            QMessageBox.information(self, "Settings Updated", "Settings have been saved")

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
