#!/usr/bin/env python3
"""
Alert System for AeroEdge System
Generates and transmits critical alerts to central dashboard.
"""

import logging
from typing import Dict, Any
import time
import json
from datetime import datetime

class AlertSystem:
    def __init__(self, config_file: str = "config/alert_config.json"):
        """
        Initialize the alert system

        Args:
            config_file: Path to alert configuration
        """
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.alert_history = []

    def generate_alert(self, inference_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate alert based on inference results

        Args:
            inference_result: Result from AI inference

        Returns:
            Alert data structure
        """
        try:
            # Extract risk level from inference
            risk_level = inference_result.get("predictions", {}).get("risk_level", "LOW")
            confidence = inference_result.get("predictions", {}).get("confidence", 0.0)
            anomaly_score = inference_result.get("predictions", {}).get("anomaly_score", 0.0)

            # Determine alert severity
            severity = self._determine_severity(risk_level, confidence, anomaly_score)

            # Create alert structure
            alert = {
                "timestamp": datetime.now().isoformat(),
                "severity": severity,
                "risk_level": risk_level,
                "confidence": confidence,
                "anomaly_score": anomaly_score,
                "alert_id": f"alert_{int(time.time())}",
                "source": "aeroedge_edge_node",
                "details": {
                    "inference_result": inference_result,
                    "processed_data": inference_result.get("input_data", {})
                }
            }

            self.logger.info(f"Generated {severity.lower()} severity alert: {alert['alert_id']}")
            return alert

        except Exception as e:
            self.logger.error(f"Error generating alert: {e}")
            raise

    def _determine_severity(self, risk_level: str, confidence: float, anomaly_score: float) -> str:
        """
        Determine alert severity based on risk factors

        Args:
            risk_level: Risk level from inference
            confidence: Confidence of prediction
            anomaly_score: Anomaly detection score

        Returns:
            Severity level (LOW, MODERATE, HIGH, CRITICAL)
        """
        # Convert risk level to numeric for comparison
        risk_map = {"LOW": 1, "MODERATE": 2, "HIGH": 3, "CRITICAL": 4}
        risk_value = risk_map.get(risk_level.upper(), 1)

        # Calculate composite score
        composite_score = (risk_value * 0.4) + (confidence * 0.3) + (anomaly_score * 0.3)

        # Determine severity based on composite score
        if composite_score >= 3.5:
            return "CRITICAL"
        elif composite_score >= 2.5:
            return "HIGH"
        elif composite_score >= 1.5:
            return "MODERATE"
        else:
            return "LOW"

    def transmit_alert(self, alert: Dict[str, Any]) -> bool:
        """
        Transmit alert to central dashboard

        Args:
            alert: Alert data to transmit

        Returns:
            True if transmission successful, False otherwise
        """
        try:
            # This would normally send to a central dashboard
            # For now, we'll simulate the transmission

            self.logger.info(f"Transmitting alert {alert['alert_id']} to dashboard...")

            # Simulate network transmission delay
            time.sleep(0.1)

            # Log to history for tracking
            self.alert_history.append(alert)

            self.logger.info(f"Alert {alert['alert_id']} transmitted successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to transmit alert {alert['alert_id']}: {e}")
            return False

    def process_alert(self, inference_result: Dict[str, Any]) -> bool:
        """
        Complete alert processing workflow

        Args:
            inference_result: Result from AI inference

        Returns:
            True if alert processed successfully, False otherwise
        """
        try:
            # Generate alert
            alert = self.generate_alert(inference_result)

            # Transmit alert
            success = self.transmit_alert(alert)

            if success:
                self.logger.info("Alert processing completed successfully")
                return True
            else:
                self.logger.error("Alert transmission failed")
                return False

        except Exception as e:
            self.logger.error(f"Error in alert processing: {e}")
            return False

    def get_alert_history(self) -> List[Dict[str, Any]]:
        """
        Get recent alert history

        Returns:
            List of alert records
        """
        return self.alert_history.copy()

    def clear_alert_history(self):
        """
        Clear alert history
        """
        self.alert_history.clear()
        self.logger.info("Alert history cleared")

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create alert system
    alert_system = AlertSystem()

    # Create sample inference result
    sample_result = {
        "timestamp": time.time(),
        "input_data": {
            "timestamp": time.time(),
            "video": {"frame_count": 100, "resolution": "1920x1080"},
            "environmental": {"temperature": 25.5, "humidity": 60.0}
        },
        "predictions": {
            "anomaly_score": 0.75,
            "risk_level": "MODERATE",
            "confidence": 0.85,
            "detected_objects": ["vehicle", "person"]
        },
        "processing_time": 0.2
    }

    # Process alert
    try:
        success = alert_system.process_alert(sample_result)
        if success:
            print("Alert processed successfully")
            print("Alert history:", len(alert_system.get_alert_history()), "alerts")
        else:
            print("Alert processing failed")
    except Exception as e:
        print(f"Failed to process alert: {e}")