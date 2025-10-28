import docker
import os
import subprocess
from typing import Dict, Any

class DockerTools:
    client = docker.from_env()
    
    @staticmethod
    def create_dockerfile(app_content: str, requirements: list) -> str:
        """Create a Dockerfile for the application"""
        dockerfile_content = f"""
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
"""
        
        # Write Dockerfile
        with open("test_app/Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        return f"Dockerfile created successfully:\n{dockerfile_content}"
    
    @staticmethod
    def build_image(image_name: str = "test-app") -> str:
        """Build Docker image"""
        try:
            image, logs = DockerTools.client.images.build(
                path="./test_app",
                tag=image_name,
                rm=True
            )
            return f"✅ Docker image '{image_name}' built successfully. Image ID: {image.id}"
        except Exception as e:
            return f"❌ Failed to build Docker image: {str(e)}"
    
    @staticmethod
    def run_container(image_name: str = "test-app", port: int = 5000) -> str:
        """Run Docker container"""
        try:
            container = DockerTools.client.containers.run(
                image_name,
                ports={'5000/tcp': port},
                detach=True,
                name="test-app-container"
            )
            
            # Wait for container to start
            import time
            time.sleep(5)
            
            return f"✅ Container '{container.name}' started successfully. ID: {container.id}"
        except Exception as e:
            return f"❌ Failed to run container: {str(e)}"
    
    @staticmethod
    def stop_container(container_name: str = "test-app-container") -> str:
        """Stop and remove Docker container"""
        try:
            container = DockerTools.client.containers.get(container_name)
            container.stop()
            container.remove()
            return f"✅ Container '{container_name}' stopped and removed"
        except Exception as e:
            return f"❌ Failed to stop container: {str(e)}"