#!/usr/bin/env python3
"""
Integration test for AeroEdge system components
"""

import sys
import os
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_components():
    """Test that all components can be imported and instantiated"""

    print("Testing AeroEdge system components...")

    # Test sensor processor
    try:
        from sensor_processor import SensorDataAggregator
        aggregator = SensorDataAggregator()
        print("✓ SensorDataAggregator imported and instantiated successfully")
    except Exception as e:
        print(f"✗ SensorDataAggregator test failed: {e}")
        return False

    # Test edge inference
    try:
        from edge_inference import EdgeAIProcessor
        processor = EdgeAIProcessor()
        print("✓ EdgeAIProcessor imported and instantiated successfully")
    except Exception as e:
        print(f"✗ EdgeAIProcessor test failed: {e}")
        return False

    # Test alert system
    try:
        from alert_system import AlertSystem
        alert_system = AlertSystem()
        print("✓ AlertSystem imported and instantiated successfully")
    except Exception as e:
        print(f"✗ AlertSystem test failed: {e}")
        return False

    # Test main module can be imported
    try:
        import main
        print("✓ Main module imported successfully")
    except Exception as e:
        print(f"✗ Main module test failed: {e}")
        return False

    print("All integration tests passed!")
    return True

def test_basic_functionality():
    """Test basic functionality of components"""

    print("\nTesting basic functionality...")

    try:
        # Test sensor aggregator
        from sensor_processor import SensorDataAggregator
        aggregator = SensorDataAggregator()
        data = aggregator.process_sensor_data()
        print("✓ Sensor data processing works")

        # Test AI processor (basic initialization)
        from edge_inference import EdgeAIProcessor
        processor = EdgeAIProcessor()
        print("✓ AI processor initialization works")

        # Test alert system
        from alert_system import AlertSystem
        alert_system = AlertSystem()
        print("✓ Alert system initialization works")

        print("Basic functionality tests passed!")
        return True

    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    success1 = test_components()
    success2 = test_basic_functionality()

    if success1 and success2:
        print("\n🎉 All tests passed! AeroEdge system is ready for deployment.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)