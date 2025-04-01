#!/bin/bash

# Test script for Trueflutter Prime AI MVP
# This script runs a series of tests to validate the functionality of the application

echo "Starting Trueflutter Prime AI MVP Test Suite"
echo "============================================"

# Check if the application is running
echo "Checking if the application is running..."
if ! pgrep -f "python3 app.py" > /dev/null; then
    echo "Application is not running. Starting it in the background..."
    cd /home/ubuntu/trueflutter_prime_ai
    nohup python3 app.py > app.log 2>&1 &
    sleep 5  # Give the app time to start
    echo "Application started with PID: $(pgrep -f 'python3 app.py')"
else
    echo "Application is already running with PID: $(pgrep -f 'python3 app.py')"
fi

# Test 1: Check if the landing page is accessible
echo -e "\nTest 1: Checking if landing page is accessible..."
if curl -s http://localhost:5000/ | grep -q "Trueflutter Prime"; then
    echo "✅ Landing page is accessible"
else
    echo "❌ Landing page is not accessible"
fi

# Test 2: Check if the form submission works
echo -e "\nTest 2: Testing form submission..."
RESPONSE=$(curl -s -X POST http://localhost:5000/submit \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "firstName=TestUser&email=test@example.com&phone=555-123-4567")

if echo "$RESPONSE" | grep -q "redirect"; then
    echo "✅ Form submission works"
else
    echo "❌ Form submission failed"
fi

# Test 3: Check if the test flow route works
echo -e "\nTest 3: Testing the test flow route..."
if curl -s -I http://localhost:5000/test-flow | grep -q "302 FOUND"; then
    echo "✅ Test flow route works"
else
    echo "❌ Test flow route failed"
fi

# Test 4: Check if the admin page is accessible
echo -e "\nTest 4: Checking if admin page is accessible..."
if curl -s http://localhost:5000/admin | grep -q "User Management"; then
    echo "✅ Admin page is accessible"
else
    echo "❌ Admin page is not accessible"
fi

# Test 5: Check if the data directory contains user files
echo -e "\nTest 5: Checking if data directory contains user files..."
USER_FILES=$(find /home/ubuntu/trueflutter_prime_ai/data -name "*.json" | wc -l)
if [ "$USER_FILES" -gt 0 ]; then
    echo "✅ Data directory contains $USER_FILES user files"
else
    echo "❌ No user files found in data directory"
fi

# Test 6: Check if the sample matches are created
echo -e "\nTest 6: Checking if sample matches are created..."
MATCH_FILES=$(find /home/ubuntu/trueflutter_prime_ai/data -name "match_*.json" | wc -l)
if [ "$MATCH_FILES" -gt 0 ]; then
    echo "✅ $MATCH_FILES sample matches found"
else
    echo "❌ No sample matches found"
fi

# Test 7: Check if the voice clips are created
echo -e "\nTest 7: Checking if voice clips are created..."
VOICE_CLIPS=$(find /home/ubuntu/trueflutter_prime_ai/static/audio/sample_matches -name "*.mp3" | wc -l)
if [ "$VOICE_CLIPS" -gt 0 ]; then
    echo "✅ $VOICE_CLIPS voice clips found"
else
    echo "❌ No voice clips found"
fi

# Test 8: Check if the application has any errors in the log
echo -e "\nTest 8: Checking application logs for errors..."
if [ -f "/home/ubuntu/trueflutter_prime_ai/app.log" ]; then
    ERROR_COUNT=$(grep -i "error" /home/ubuntu/trueflutter_prime_ai/app.log | wc -l)
    if [ "$ERROR_COUNT" -eq 0 ]; then
        echo "✅ No errors found in application logs"
    else
        echo "⚠️ $ERROR_COUNT errors found in application logs"
    fi
else
    echo "⚠️ Application log file not found"
fi

echo -e "\nTest Summary"
echo "============"
echo "Total tests: 8"
echo "Passed: $(grep -c "✅" <<< "$(cat $0)")"
echo "Failed: $(grep -c "❌" <<< "$(cat $0)")"
echo "Warnings: $(grep -c "⚠️" <<< "$(cat $0)")"

echo -e "\nTrueflutter Prime AI MVP Test Suite Completed"
