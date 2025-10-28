import subprocess
import os
import requests
import time

class TestingTools:
    
    @staticmethod
    def write_tests() -> str:
        """Write test cases for the application"""
        test_code = '''
import pytest
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test the home route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Agentic Engineering Team' in response.data

def test_health_route(client):
    """Test the health check API"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
    assert 'service' in response.json

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert 'error' in response.json

def test_health_structure(client):
    """Test health endpoint structure"""
    response = client.get('/api/health')
    data = response.json
    assert 'status' in data
    assert 'service' in data
    assert 'version' in data
'''
        
        with open("test_app/test_app.py", "w") as f:
            f.write(test_code)
        
        return "✅ Test cases written successfully: test_app.py created"
    
    @staticmethod
    def run_tests() -> str:
        """Run the test suite"""
        try:
            # Change to test directory
            original_dir = os.getcwd()
            os.chdir("test_app")
            
            # Run pytest
            result = subprocess.run(
                ["python", "-m", "pytest", "test_app.py", "-v", "--html=test_report.html"],
                capture_output=True,
                text=True
            )
            
            # Return to original directory
            os.chdir(original_dir)
            
            test_report = f"""
Test Execution Results:
Exit Code: {result.returncode}
Stdout: {result.stdout}
Stderr: {result.stderr}
"""
            
            if result.returncode == 0:
                return f"✅ All tests passed!\n{test_report}"
            else:
                return f"❌ Some tests failed!\n{test_report}"
                
        except Exception as e:
            return f"❌ Test execution failed: {str(e)}"
    
    @staticmethod
    def test_deployed_app(port: int = 5000) -> str:
        """Test the deployed application"""
        try:
            base_url = f"http://localhost:{port}"
            
            tests = []
            
            # Test home route
            try:
                response = requests.get(f"{base_url}/", timeout=5)
                tests.append((
                    "Home Route", 
                    response.status_code == 200,
                    f"Status: {response.status_code}"
                ))
            except:
                tests.append(("Home Route", False, "Connection failed"))
            
            # Test health route
            try:
                response = requests.get(f"{base_url}/api/health", timeout=5)
                tests.append((
                    "Health API", 
                    response.status_code == 200 and response.json().get('status') == 'healthy',
                    f"Status: {response.status_code}, Response: {response.json()}"
                ))
            except:
                tests.append(("Health API", False, "Connection failed"))
            
            # Generate report
            report = ["Deployment Test Results:"]
            for test_name, passed, details in tests:
                status = "✅ PASS" if passed else "❌ FAIL"
                report.append(f"{status} {test_name}: {details}")
            
            return "\n".join(report)
            
        except Exception as e:
            return f"❌ Deployment testing failed: {str(e)}"