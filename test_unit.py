#!/usr/bin/env python3
"""
Unit tests for AeroEdge system components
"""

import sys
import os
import logging
import unittest
from unittest.mock import patch, MagicMock
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sensor_processor import SensorDataAggregator
from edge_inference import EdgeAIProcessor
from alert_system import AlertSystem

class TestSensorDataAggregator(unittest.TestCase):
    """Test cases for SensorDataAggregator class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.aggregator = SensorDataAggregator()
        logging.basicConfig(level=logging.DEBUG)

    def test_init(self):
        """Test SensorDataAggregator initialization"""
        self.assertIsNotNone(self.aggregator)
        self.assertEqual(self.aggregator.config_file, "config/sensor_config.json")

    def test_collect_video_data(self):
        """Test video data collection"""
        video_data = self.aggregator.collect_video_data()
        self.assertIsInstance(video_data, dict)
        self.assertIn("timestamp", video_data)
        self.assertIn("frame_count", video_data)
        self.assertIn("resolution", video_data)

    def test_collect_environmental_data(self):
        """Test environmental data collection"""
        env_data = self.aggregator.collect_environmental_data()
        self.assertIsInstance(env_data, dict)
        self.assertIn("timestamp", env_data)
        self.assertIn("temperature", env_data)
        self.assertIn("humidity", env_data)
        self.assertIn("pressure", env_data)
        self.assertIn("light_level", env_data)

    def test_fuse_multimodal_data(self):
        """Test multimodal data fusion"""
        video_data = self.aggregator.collect_video_data()
        env_data = self.aggregator.collect_environmental_data()

        fused_data = self.aggregator.fuse_multimodal_data(video_data, env_data)
        self.assertIsInstance(fused_data, dict)
        self.assertIn("timestamp", fused_data)
        self.assertIn("video", fused_data)
        self.assertIn("environmental", fused_data)
        self.assertIn("fusion_timestamp", fused_data)
        self.assertIn("temperature_humidity_ratio", fused_data)

    def test_process_sensor_data(self):
        """Test full sensor data processing"""
        data = self.aggregator.process_sensor_data()
        self.assertIsInstance(data, dict)
        self.assertIn("timestamp", data)
        self.assertIn("video", data)
        self.assertIn("environmental", data)
        self.assertIn("fusion_timestamp", data)

class TestEdgeAIProcessor(unittest.TestCase):
    """Test cases for EdgeAIProcessor class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = EdgeAIProcessor()
        logging.basicConfig(level=logging.DEBUG)

    def test_init(self):
        """Test EdgeAIProcessor initialization"""
        self.assertIsNotNone(self.processor)
        self.assertEqual(self.processor.model_path, "models/")
        self.assertEqual(self.processor.config_file, "config/model_config.json")

    def test_run_inference_with_mocked_model(self):
        """Test inference execution with mocked model"""
        # Create mock data
        sample_data = {
            "timestamp": 1234567890,
            "video": {"frame_count": 100, "resolution": "1920x1080"},
            "environmental": {"temperature": 25.5, "humidity": 60.0}
        }

        # Test that the method structure works without actual model loading
        with patch.object(self.processor, '_load_model_config'):
            # Mock model as loaded
            self.processor.model_loaded = True

            # Test inference with valid data
            result = self.processor.run_inference(sample_data)
            self.assertIsInstance(result, dict)
            self.assertIn("timestamp", result)
            self.assertIn("input_data", result)
            self.assertIn("predictions", result)
            self.assertIn("processing_time", result)


class TestAlertSystem(unittest.TestCase):
    """Test cases for AlertSystem class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.alert_system = AlertSystem()
        logging.basicConfig(level=logging.DEBUG)

    def test_init(self):
        """Test AlertSystem initialization"""
        self.assertIsNotNone(self.alert_system)
        self.assertEqual(self.alert_system.config_file, "config/alert_config.json")

    def test_generate_alert(self):
        """Test alert generation"""
        # Create sample inference result
        inference_result = {
            "timestamp": 1234567890,
            "input_data": {
                "timestamp": 1234567890,
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

        alert = self.alert_system.generate_alert(inference_result)
        self.assertIsInstance(alert, dict)
        self.assertIn("timestamp", alert)
        self.assertIn("severity", alert)
        self.assertIn("risk_level", alert)
        self.assertIn("alert_id", alert)

    def test_determine_severity(self):
        """Test severity determination"""
        severity = self.alert_system._determine_severity("HIGH", 0.9, 0.8)
        self.assertIn(severity, ["LOW", "MODERATE", "HIGH", "CRITICAL"])

    def test_process_alert(self):
        """Test complete alert processing"""
        # Create sample inference result
        inference_result = {
            "timestamp": 1234567890,
            "input_data": {
                "timestamp": 1234567890,
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

        # Mock the transmit_alert method to avoid actual network calls
        with patch.object(self.alert_system, 'transmit_alert', return_value=True):
            success = self.alert_system.process_alert(inference_result)
            self.assertTrue(success)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)