"""
Core security monitor module for Sentinel-X.

This module provides real-time monitoring, threat detection, and security event handling
for enterprise communication systems. It includes classes for managing threat levels,
security events, and the main security monitoring system.

Author: shivamgawade-droid
Created: 2025-12-27 13:41:13 UTC
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import List, Optional, Dict, Any
from threading import Thread, Lock, Event
import logging
import json


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """Enumeration of threat severity levels."""
    
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"
    
    def __lt__(self, other):
        """Compare threat levels by severity."""
        if not isinstance(other, ThreatLevel):
            return NotImplemented
        severity_order = {
            ThreatLevel.CRITICAL: 5,
            ThreatLevel.HIGH: 4,
            ThreatLevel.MEDIUM: 3,
            ThreatLevel.LOW: 2,
            ThreatLevel.INFO: 1,
        }
        return severity_order[self] < severity_order[other]
    
    def __le__(self, other):
        """Check if threat level is less than or equal."""
        return self == other or self < other
    
    def __gt__(self, other):
        """Check if threat level is greater than."""
        return not (self <= other)
    
    def __ge__(self, other):
        """Check if threat level is greater than or equal."""
        return not (self < other)


@dataclass
class SecurityEvent:
    """Represents a security event in the monitoring system."""
    
    event_id: str
    timestamp: datetime
    threat_level: ThreatLevel
    event_type: str
    source: str
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate security event data."""
        if not self.event_id:
            raise ValueError("event_id cannot be empty")
        if not self.event_type:
            raise ValueError("event_type cannot be empty")
        if not self.source:
            raise ValueError("source cannot be empty")
        if not self.description:
            raise ValueError("description cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert security event to dictionary format."""
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'threat_level': self.threat_level.value,
            'event_type': self.event_type,
            'source': self.source,
            'description': self.description,
            'details': self.details,
        }
    
    def to_json(self) -> str:
        """Convert security event to JSON format."""
        return json.dumps(self.to_dict(), indent=2)
    
    def __str__(self) -> str:
        """String representation of the security event."""
        return (f"SecurityEvent(id={self.event_id}, level={self.threat_level.value}, "
                f"type={self.event_type}, source={self.source})")


class SecurityMonitor:
    """
    Main security monitoring system for enterprise communication infrastructure.
    
    Provides real-time monitoring, threat detection, and security event handling
    with comprehensive logging and filtering capabilities.
    """
    
    def __init__(self, name: str = "Sentinel-X Monitor", max_events: int = 10000):
        """
        Initialize the SecurityMonitor.
        
        Args:
            name: Name identifier for the monitor instance
            max_events: Maximum number of events to store in memory
        """
        self.name = name
        self.max_events = max_events
        self.events: List[SecurityEvent] = []
        self._lock = Lock()
        self._monitoring = False
        self._stop_event = Event()
        self._monitor_thread: Optional[Thread] = None
        logger.info(f"SecurityMonitor '{name}' initialized with capacity {max_events} events")
    
    def log_event(self, event: SecurityEvent) -> None:
        """
        Log a security event to the monitoring system.
        
        Args:
            event: SecurityEvent object to log
            
        Raises:
            TypeError: If event is not a SecurityEvent instance
        """
        if not isinstance(event, SecurityEvent):
            raise TypeError("event must be an instance of SecurityEvent")
        
        with self._lock:
            # Maintain max_events limit by removing oldest events
            if len(self.events) >= self.max_events:
                self.events.pop(0)
            
            self.events.append(event)
            logger.log(
                getattr(logging, event.threat_level.name),
                f"Event logged: {event.event_id} - {event.description}"
            )
    
    def start_monitoring(self) -> None:
        """
        Start the security monitoring system.
        
        Initializes background monitoring thread for continuous threat detection.
        """
        if self._monitoring:
            logger.warning("Monitoring is already active")
            return
        
        self._monitoring = True
        self._stop_event.clear()
        self._monitor_thread = Thread(
            target=self._monitor_loop,
            daemon=True,
            name=f"{self.name}-Monitor-Thread"
        )
        self._monitor_thread.start()
        logger.info(f"Security monitoring started for '{self.name}'")
    
    def stop_monitoring(self) -> None:
        """
        Stop the security monitoring system.
        
        Gracefully halts background monitoring thread and cleanup.
        """
        if not self._monitoring:
            logger.warning("Monitoring is not currently active")
            return
        
        self._monitoring = False
        self._stop_event.set()
        
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)
        
        logger.info(f"Security monitoring stopped for '{self.name}'")
    
    def _monitor_loop(self) -> None:
        """
        Internal monitoring loop for continuous threat detection.
        
        Runs in background thread to perform periodic security checks.
        """
        logger.debug(f"Monitor loop started for '{self.name}'")
        
        while self._monitoring and not self._stop_event.is_set():
            try:
                # Perform background monitoring tasks
                self._stop_event.wait(timeout=5)
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
        
        logger.debug(f"Monitor loop ended for '{self.name}'")
    
    def get_events(
        self,
        threat_level: Optional[ThreatLevel] = None,
        event_type: Optional[str] = None,
        source: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[SecurityEvent]:
        """
        Retrieve security events with optional filtering.
        
        Args:
            threat_level: Filter by minimum threat level (returns >= this level)
            event_type: Filter by event type
            source: Filter by event source
            start_time: Filter events after this timestamp
            end_time: Filter events before this timestamp
        
        Returns:
            List of SecurityEvent objects matching the filters
        """
        with self._lock:
            filtered_events = self.events.copy()
        
        if threat_level is not None:
            filtered_events = [
                e for e in filtered_events
                if e.threat_level >= threat_level
            ]
        
        if event_type is not None:
            filtered_events = [
                e for e in filtered_events
                if e.event_type.lower() == event_type.lower()
            ]
        
        if source is not None:
            filtered_events = [
                e for e in filtered_events
                if e.source.lower() == source.lower()
            ]
        
        if start_time is not None:
            filtered_events = [
                e for e in filtered_events
                if e.timestamp >= start_time
            ]
        
        if end_time is not None:
            filtered_events = [
                e for e in filtered_events
                if e.timestamp <= end_time
            ]
        
        return filtered_events
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the security monitor.
        
        Returns:
            Dictionary containing monitor status information
        """
        with self._lock:
            event_count = len(self.events)
            threat_summary = self._calculate_threat_summary()
        
        return {
            'name': self.name,
            'monitoring_active': self._monitoring,
            'total_events': event_count,
            'max_capacity': self.max_events,
            'capacity_usage_percent': (event_count / self.max_events * 100) if self.max_events > 0 else 0,
            'threat_summary': threat_summary,
            'timestamp': datetime.now(UTC).isoformat(),
        }
    
    def _calculate_threat_summary(self) -> Dict[str, int]:
        """
        Calculate threat level distribution summary.
        
        Returns:
            Dictionary with count of events per threat level
        """
        summary = {level.value: 0 for level in ThreatLevel}
        
        for event in self.events:
            summary[event.threat_level.value] += 1
        
        return summary
    
    def clear_events(self, threat_level: Optional[ThreatLevel] = None) -> int:
        """
        Clear security events from the monitoring system.
        
        Args:
            threat_level: If specified, only clear events at or below this level
        
        Returns:
            Number of events cleared
        """
        with self._lock:
            if threat_level is None:
                cleared_count = len(self.events)
                self.events.clear()
            else:
                initial_count = len(self.events)
                self.events = [
                    e for e in self.events
                    if e.threat_level > threat_level
                ]
                cleared_count = initial_count - len(self.events)
            
            logger.info(f"Cleared {cleared_count} events from '{self.name}'")
            return cleared_count
    
    def get_critical_events(self) -> List[SecurityEvent]:
        """
        Retrieve all critical and high-severity events.
        
        Returns:
            List of critical and high-threat events
        """
        with self._lock:
            return [
                e for e in self.events
                if e.threat_level in (ThreatLevel.CRITICAL, ThreatLevel.HIGH)
            ]
    
    def get_event_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of monitored events.
        
        Returns:
            Dictionary containing event statistics and summaries
        """
        with self._lock:
            events_copy = self.events.copy()
        
        if not events_copy:
            return {
                'total_events': 0,
                'events_by_type': {},
                'events_by_source': {},
                'critical_events': 0,
                'latest_event': None,
            }
        
        # Count by event type
        events_by_type = {}
        for event in events_copy:
            events_by_type[event.event_type] = events_by_type.get(event.event_type, 0) + 1
        
        # Count by source
        events_by_source = {}
        for event in events_copy:
            events_by_source[event.source] = events_by_source.get(event.source, 0) + 1
        
        critical_count = sum(
            1 for e in events_copy
            if e.threat_level in (ThreatLevel.CRITICAL, ThreatLevel.HIGH)
        )
        
        return {
            'total_events': len(events_copy),
            'events_by_type': events_by_type,
            'events_by_source': events_by_source,
            'critical_events': critical_count,
            'latest_event': events_copy[-1].to_dict() if events_copy else None,
        }
    
    def __repr__(self) -> str:
        """String representation of the SecurityMonitor."""
        return (f"SecurityMonitor(name='{self.name}', monitoring={self._monitoring}, "
                f"events={len(self.events)}/{self.max_events})")
