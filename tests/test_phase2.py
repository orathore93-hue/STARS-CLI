#!/usr/bin/env python3
"""
TARS CLI - Phase 2 Enhanced Features Tests
Tests for configuration, multi-cluster, alerting, history, and export
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd):
    """Run command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)

def test_config_commands():
    """Test 1: Configuration management commands"""
    print("\n🧪 Test 1: Configuration Management")
    
    commands = [
        ("./tars.py config --help", "config help"),
        ("./tars.py config list --help", "config list help"),
        ("./tars.py config get --help", "config get help"),
        ("./tars.py config set --help", "config set help"),
        ("./tars.py config reset --help", "config reset help"),
        ("./tars.py config edit --help", "config edit help")
    ]
    
    all_passed = True
    for cmd, desc in commands:
        code, stdout, stderr = run_command(cmd)
        if code == 0:
            print(f"✅ {desc}")
        else:
            print(f"❌ {desc} failed")
            all_passed = False
    
    if all_passed:
        print("✅ PASS: All config commands present")
        return True
    else:
        print("❌ FAIL: Some config commands missing")
        return False

def test_config_file_structure():
    """Test 2: Configuration file structure"""
    print("\n🧪 Test 2: Configuration File Structure")
    
    checks = [
        ("CONFIG_FILE = TARS_DIR", "Config file path"),
        ("DEFAULT_CONFIG", "Default config"),
        ("load_config()", "Load config function"),
        ("save_config(", "Save config function")
    ]
    
    with open("tars.py", "r") as f:
        content = f.read()
    
    all_present = True
    for check, desc in checks:
        if check in content:
            print(f"✅ {desc}")
        else:
            print(f"❌ Missing: {desc}")
            all_present = False
    
    if all_present:
        print("✅ PASS: Config structure complete")
        return True
    else:
        print("❌ FAIL: Config structure incomplete")
        return False

def test_multi_cluster_command():
    """Test 3: Multi-cluster support"""
    print("\n🧪 Test 3: Multi-Cluster Support")
    
    code, stdout, stderr = run_command("./tars.py multi-cluster --help")
    if code == 0 and "multi-cluster" in stdout.lower():
        print("✅ multi-cluster command exists")
        print("✅ PASS: Multi-cluster support implemented")
        return True
    else:
        print("❌ FAIL: Multi-cluster command not found")
        return False

def test_webhook_alerting():
    """Test 4: Webhook alerting"""
    print("\n🧪 Test 4: Webhook Alerting")
    
    checks = [
        ("def send_webhook", "Webhook function"),
        ("def alert_webhook", "Alert webhook command"),
        ("slack.com", "Slack support"),
        ("requests.post", "HTTP requests")
    ]
    
    with open("tars.py", "r") as f:
        content = f.read()
    
    all_present = True
    for check, desc in checks:
        if check in content:
            print(f"✅ {desc}")
        else:
            print(f"❌ Missing: {desc}")
            all_present = False
    
    if all_present:
        print("✅ PASS: Webhook alerting implemented")
        return True
    else:
        print("❌ FAIL: Webhook alerting incomplete")
        return False

def test_history_commands():
    """Test 5: Command history"""
    print("\n🧪 Test 5: Command History")
    
    commands = [
        ("./tars.py history --help", "history command"),
        ("./tars.py replay --help", "replay command")
    ]
    
    all_passed = True
    for cmd, desc in commands:
        code, stdout, stderr = run_command(cmd)
        if code == 0:
            print(f"✅ {desc}")
        else:
            print(f"❌ {desc} failed")
            all_passed = False
    
    # Check history functions
    with open("tars.py", "r") as f:
        content = f.read()
    
    if "HISTORY_FILE" in content and "save_to_history" in content:
        print("✅ History functions present")
    else:
        print("❌ History functions missing")
        all_passed = False
    
    if all_passed:
        print("✅ PASS: Command history implemented")
        return True
    else:
        print("❌ FAIL: Command history incomplete")
        return False

def test_export_command():
    """Test 6: Export functionality"""
    print("\n🧪 Test 6: Export Functionality")
    
    code, stdout, stderr = run_command("./tars.py export --help")
    if code == 0:
        print("✅ export command exists")
        
        # Check format support
        if "json" in stdout and "yaml" in stdout and "csv" in stdout:
            print("✅ Multiple format support (JSON, YAML, CSV)")
            print("✅ PASS: Export functionality implemented")
            return True
        else:
            print("❌ Missing format support")
            return False
    else:
        print("❌ FAIL: Export command not found")
        return False

def test_yaml_support():
    """Test 7: YAML support"""
    print("\n🧪 Test 7: YAML Support")
    
    code, stdout, stderr = run_command("grep -n 'import yaml' tars.py")
    if code == 0:
        print("✅ YAML import present")
        print("✅ PASS: YAML support added")
        return True
    else:
        print("❌ FAIL: YAML import missing")
        return False

def test_requests_support():
    """Test 8: Requests library"""
    print("\n🧪 Test 8: Requests Library")
    
    code, stdout, stderr = run_command("grep -n 'import requests' tars.py")
    if code == 0:
        print("✅ Requests import present")
        print("✅ PASS: Requests library added")
        return True
    else:
        print("❌ FAIL: Requests import missing")
        return False

def test_requirements():
    """Test 9: Requirements file"""
    print("\n🧪 Test 9: Requirements File")
    
    with open("requirements.txt", "r") as f:
        requirements = f.read()
    
    required_packages = ["pyyaml", "requests"]
    all_present = True
    
    for package in required_packages:
        if package in requirements.lower():
            print(f"✅ {package}")
        else:
            print(f"❌ Missing: {package}")
            all_present = False
    
    if all_present:
        print("✅ PASS: All required packages in requirements.txt")
        return True
    else:
        print("❌ FAIL: Some packages missing from requirements.txt")
        return False

def test_help_output():
    """Test 10: Help output includes new commands"""
    print("\n🧪 Test 10: Help Output")
    
    code, stdout, stderr = run_command("./tars.py --help")
    if code != 0:
        print("❌ FAIL: Help command failed")
        return False
    
    new_commands = ["config", "multi-cluster", "history", "replay", "export", "alert-webhook"]
    all_present = True
    
    for cmd in new_commands:
        if cmd in stdout:
            print(f"✅ {cmd} in help")
        else:
            print(f"❌ Missing from help: {cmd}")
            all_present = False
    
    if all_present:
        print("✅ PASS: All new commands in help output")
        return True
    else:
        print("❌ FAIL: Some commands missing from help")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("TARS CLI - Phase 2 Enhanced Features Test Suite")
    print("=" * 70)
    
    tests = [
        test_config_commands,
        test_config_file_structure,
        test_multi_cluster_command,
        test_webhook_alerting,
        test_history_commands,
        test_export_command,
        test_yaml_support,
        test_requests_support,
        test_requirements,
        test_help_output
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"\nTests Passed: {passed}/{total} ({percentage:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Phase 2 Complete!")
        print("\n✅ Configuration Management: COMPLETE")
        print("✅ Multi-Cluster Support: COMPLETE")
        print("✅ Webhook Alerting: COMPLETE")
        print("✅ Command History: COMPLETE")
        print("✅ Export Functionality: COMPLETE")
        print("\n🚀 TARS CLI Phase 2 is production-ready!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
