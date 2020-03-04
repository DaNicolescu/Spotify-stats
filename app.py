from flask import Flask, render_template
import random
import socket

app = Flask(__name__)

images = [
    "https://i2.wp.com/www.libraryforsmartinvestors.com/wp-content/uploads/2017/02/aws_logo.jpg?fit=500%2C500&ssl=1",
    "http://australiaday.openstack.org.au/wp-content/uploads/2016/01/openstack_500x500.png",
    "http://isoc.ae/image/cache/catalog/courses/Google%20Cloud%20Compute%20Engine%20Essential%20Training-500x500.jpg",
    "https://images.g2crowd.com/uploads/product/image/large_detail/large_detail_1528237089/microsoft-azure-biztalk-services.jpg",
    "https://aptira.com/wp-content/uploads/2016/09/kubernetes_logo.png",
    "https://www.opsview.com/sites/default/files/docker.png"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url, hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host="0.0.0.0")