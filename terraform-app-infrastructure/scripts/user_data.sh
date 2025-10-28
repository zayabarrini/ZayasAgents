#!/bin/bash
apt-get update
apt-get install -y nginx python3-pip

# Configure application
cat > /etc/nginx/conf.d/app.conf << EOF
server {
    listen 8080;
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF

systemctl enable nginx
systemctl start nginx

# Install cloudwatch agent for monitoring
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb