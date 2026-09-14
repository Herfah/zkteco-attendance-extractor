"""Module to handle ZKTeco device communication"""
from zkteco_push_sdk import ZKDevice
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZKTecoDevice:
    """Wrapper for ZKTeco device communication"""
    
    def __init__(self, ip=None, port=None, timeout=None):
        self.ip = ip or config.DEVICE_IP
        self.port = port or config.DEVICE_PORT
        self.timeout = timeout or config.DEVICE_TIMEOUT
        self.conn = None
        self.zk = None
    
    def connect(self):
        """Connect to ZKTeco device"""
        try:
            self.zk = ZKDevice(self.ip, port=self.port, timeout=self.timeout)
            self.zk.connect()
            logger.info(f"Connected to ZKTeco device at {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to device: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from ZKTeco device"""
        try:
            if self.zk:
                self.zk.disconnect()
            logger.info("Disconnected from device")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
            return False
    
    def get_attendance_records(self):
        """Fetch all attendance records from device"""
        try:
            if not self.zk:
                return None
            
            # Get attendance records
            attendance = self.zk.get_attendance()
            
            logger.info(f"Retrieved {len(attendance)} attendance records")
            return attendance
        except Exception as e:
            logger.error(f"Error fetching attendance records: {e}")
            return None
    
    def get_users(self):
        """Get all users from device"""
        try:
            if not self.zk:
                return None
            return self.zk.get_users()
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return None
    
    def get_device_info(self):
        """Get device information"""
        try:
            if not self.zk:
                return None
            
            info = {
                'serial_number': self.zk.get_serial_number(),
                'device_name': self.zk.get_device_name(),
                'platform': self.zk.get_platform(),
                'firmware_version': self.zk.get_firmware_version(),
            }
            return info
        except Exception as e:
            logger.error(f"Error fetching device info: {e}")
            return None
    
    def test_connection(self):
        """Test device connection"""
        if self.connect():
            self.disconnect()
            return True
        return False
