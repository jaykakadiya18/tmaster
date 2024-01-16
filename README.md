Ticket master deployment
<<<<<<< HEAD

# Deployment process

Step-1:
==> Create a folder accordenly your requirement

Step-2:
==> Clone your project repo please use below commond
git clone {repo_remote}

==> If you have clone with specific branch then use below commond
git clone -b {branch_name} {repo_remote}

Step-3
==> Go to that project directory

Step-4
==> Create docker image using below commond
docker build -t {username/imagename:tag} .

Step-5
==> Create Docker container using below commond
docket container run -d -p {flaskport}:{forwardport} {yourimagename:yourtagname}

Step-6
==> Check docker image is running or not use below commond
sudo docker images

Step-7
==> Check docker container is present or not
sudo docker container ls
sudo docker ps -a

Step-8
==> Check docker logs
sudo docker logs {container_id}
=======
>>>>>>> 31255f2c352d93f2e6e4504617eb4a1da54dad42
