"""Module for exporting attendance data"""
import csv
import os
from datetime import datetime
import pandas as pd
from config import config

class ExportHandler:
    """Handle data export in various formats"""
    
    def __init__(self):
        self.export_path = config.EXPORT_PATH
        os.makedirs(self.export_path, exist_ok=True)
    
    def export_to_csv(self, records, filename=None):
        """Export records to CSV"""
        try:
            if not filename:
                filename = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            filepath = os.path.join(self.export_path, filename)
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'User ID', 'Name', 'Timestamp', 'Status', 'Device IP'])
                for record in records:
                    status_text = 'Check-In' if record[4] == 0 else 'Check-Out'
                    writer.writerow([
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        status_text,
                        record[5]
                    ])
            
            return filepath
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
    
    def export_to_excel(self, records, filename=None):
        """Export records to Excel"""
        try:
            if not filename:
                filename = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            filepath = os.path.join(self.export_path, filename)
            
            df = pd.DataFrame(records, columns=['ID', 'User ID', 'Name', 'Timestamp', 'Status', 'Device IP'])
            df['Status'] = df['Status'].apply(lambda x: 'Check-In' if x == 0 else 'Check-Out')
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df = df.sort_values('Timestamp', ascending=False)
            
            df.to_excel(filepath, index=False, sheet_name='Attendance')
            
            return filepath
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return None
    
    def export_summary_report(self, records, filename=None):
        """Export summary report (daily attendance)"""
        try:
            if not filename:
                filename = f"attendance_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            filepath = os.path.join(self.export_path, filename)
            
            df = pd.DataFrame(records, columns=['ID', 'User ID', 'Name', 'Timestamp', 'Status', 'Device IP'])
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = df['Timestamp'].dt.date
            df['Time'] = df['Timestamp'].dt.time
            df['Status'] = df['Status'].apply(lambda x: 'Check-In' if x == 0 else 'Check-Out')
            
            # Create pivot table
            summary = df.pivot_table(
                values='Timestamp',
                index=['Date', 'User ID', 'Name'],
                columns='Status',
                aggfunc='min'
            )
            
            summary.to_excel(filepath)
            
            return filepath
        except Exception as e:
            print(f"Error exporting summary: {e}")
            return None
