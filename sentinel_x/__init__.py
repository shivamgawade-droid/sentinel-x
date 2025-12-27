"""
Sentinel-X: Advanced Security and Monitoring System

A comprehensive package for security monitoring, threat detection, and system analysis.
"""

__version__ = "1.0.0"
__author__ = "Shivam Gawade"
__license__ = "MIT"

# Import main components for easy access
try:
    from sentinel_x.core import SecurityMonitor
    from sentinel_x.detector import ThreatDetector
    from sentinel_x.analyzer import SystemAnalyzer
    from sentinel_x.logger import SecurityLogger
except ImportError:
    # Handle cases where submodules haven't been fully installed yet
    pass

# Define public API
__all__ = [
    "SecurityMonitor",
    "ThreatDetector",
    "SystemAnalyzer",
    "SecurityLogger",
    "__version__",
    "__author__",
]
