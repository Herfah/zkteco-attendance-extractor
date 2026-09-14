"""Configuration settings for ZKTeco Attendance Extractor"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Default configuration"""
    # ZKTeco Device Settings
    DEVICE_IP = os.getenv('DEVICE_IP', '192.168.1.201')
    DEVICE_PORT = int(os.getenv('DEVICE_PORT', 4370))
    DEVICE_TIMEOUT = int(os.getenv('DEVICE_TIMEOUT', 5))
    
    # Application Settings
    APP_NAME = "ZKTeco Attendance Extractor"
    APP_VERSION = "1.0.0"
    
    # Database
    DB_PATH = os.path.expanduser('~/.zkteco/attendance.db')
    
    # Export Settings
    EXPORT_PATH = os.path.expanduser('~/Documents/ZKTeco_Exports')
    
    # Polling Settings (in minutes)
    AUTO_SYNC_INTERVAL = int(os.getenv('AUTO_SYNC_INTERVAL', 30))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = DevelopmentConfig()
