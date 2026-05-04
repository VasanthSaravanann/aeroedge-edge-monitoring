#!/usr/bin/env python3
"""
Sensor Data Aggregator for AeroEdge System
Handles collection and fusion of video and environmental sensor data.
"""

import logging
from typing import Dict, Any, List
import time
import random

class SensorDataAggregator:
    def __init__(self, config_file: str = "config/sensor_config.json"):
        """
        Initialize the sensor data aggregator

        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)

        # Initialize data structures
        self.sensor_data = {}
        self.processed_data = {}

        # Load configuration
        self._load_config()

    def _load_config(self):
        """Load sensor configuration"""
        try:
            import json
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            self.logger.info("Sensor configuration loaded successfully")
        except Exception as e:
            self.logger.warning(f"Could not load sensor config: {e}. Using defaults.")
            # Default configuration
            self.config = {
                "sensor_types": ["camera", "temperature", "humidity", "pressure", "light", "motion"],
                "sampling_rates": {
                    "camera": 10,
                    "temperature": 60,
                    "humidity": 60,
                    "pressure": 60,
                    "light": 30,
                    "motion": 5
                },
                "data_validation": {
                    "enabled": True,
                    "thresholds": {
                        "temperature_min": -40,
                        "temperature_max": 85,
                        "humidity_min": 0,
                        "humidity_max": 100
                    }
                }
            }

    def collect_video_data(self) -> Dict[str, Any]:
        """
        Collect video frame data from device camera
        """
        # Simulated video data collection for demonstration
        # In a real implementation, this would interface with actual camera APIs
        self.logger.info("Collecting video frame data...")

        # Simulate video frame data
        video_data = {
            "timestamp": time.time(),
            "frame_count": random.randint(0, 100),
            "resolution": "1920x1080",
            "fps": 30,
            "frame_width": 1920,
            "frame_height": 1080,
            "quality_score": random.uniform(0.8, 1.0)
        }

        self.logger.info("Video data collected successfully")
        return video_data

    def collect_environmental_data(self) -> Dict[str, Any]:
        """
        Collect environmental sensor data
        """
        # Simulated environmental sensor data for demonstration
        # In a real implementation, this would interface with actual sensors
        self.logger.info("Collecting environmental sensor data...")

        # Simulate environmental data
        environmental_data = {
            "timestamp": time.time(),
            "temperature": round(random.uniform(-10.0, 40.0), 2),
            "humidity": round(random.uniform(0.0, 100.0), 2),
            "pressure": round(random.uniform(950.0, 1050.0), 2),
            "light_level": random.randint(0, 1000),
            "motion_detected": random.choice([True, False]),
            "battery_level": round(random.uniform(20.0, 100.0), 2)
        }

        # Validate data if validation is enabled
        if self.config.get("data_validation", {}).get("enabled", False):
            thresholds = self.config["data_validation"]["thresholds"]
            # Validate temperature
            temp = environmental_data["temperature"]
            if temp < thresholds["temperature_min"] or temp > thresholds["temperature_max"]:
                self.logger.warning(f"Temperature out of range: {temp}")

            # Validate humidity
            humidity = environmental_data["humidity"]
            if humidity < thresholds["humidity_min"] or humidity > thresholds["humidity_max"]:
                self.logger.warning(f"Humidity out of range: {humidity}")

        self.logger.info("Environmental data collected successfully")
        return environmental_data

    def fuse_multimodal_data(self, video_data: Dict[str, Any],
                            environmental_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fuse video and environmental sensor data for AI processing

        Args:
            video_data: Collected video frame data
            environmental_data: Collected environmental data

        Returns:
            Combined multimodal data
        """
        fused_data = {
            "timestamp": video_data["timestamp"],
            "video": video_data,
            "environmental": environmental_data,
            "fusion_timestamp": time.time()
        }

        # Add derived features for enhanced AI processing
        try:
            if environmental_data["humidity"] > 0:
                fused_data["temperature_humidity_ratio"] = \
                    environmental_data["temperature"] / environmental_data["humidity"]
            else:
                fused_data["temperature_humidity_ratio"] = 0.0

            # Add light intensity ratio
            fused_data["light_temperature_ratio"] = \
                environmental_data["light_level"] / (environmental_data["temperature"] + 1)

            # Motion and temperature correlation
            fused_data["motion_temperature_correlation"] = \
                1 if environmental_data["motion_detected"] and environmental_data["temperature"] > 25 else 0

        except Exception as e:
            self.logger.warning(f"Error calculating derived features: {e}")
            fused_data["temperature_humidity_ratio"] = 0.0
            fused_data["light_temperature_ratio"] = 0.0
            fused_data["motion_temperature_correlation"] = 0

        self.logger.info("Multimodal data fusion completed")
        return fused_data

    def process_sensor_data(self) -> Dict[str, Any]:
        """
        Main method to process all sensor data

        Returns:
            Processed and fused sensor data
        """
        try:
            # Collect data from all sources
            video_data = self.collect_video_data()
            environmental_data = self.collect_environmental_data()

            # Fuse the data
            processed_data = self.fuse_multimodal_data(video_data, environmental_data)

            self.logger.info("Sensor data processing completed successfully")
            return processed_data

        except Exception as e:
            self.logger.error(f"Error in sensor data processing: {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create aggregator
    aggregator = SensorDataAggregator()

    # Process data
    try:
        result = aggregator.process_sensor_data()
        print("Sensor data processed:", result)
    except Exception as e:
        print(f"Failed to process sensor data: {e}")