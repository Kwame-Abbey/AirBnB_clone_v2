#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared/
echo "Ablordey Morgan Test" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
link_file="/data/web_static/current"
config="/etc/nginx/sites-enabled/default"
sudo sed -i "41i \\\\tlocation /hbnb_static/ {\n\t\talias $link_file/;\n\t\tautoindex off;\n\t}\n" "$config"
sudo service nginx restart
