docker ps [-a|-q]

docker run [options] image_name exec_command
    -i, stdin
    -t, terminal
    -d, run in background
    -name,
    -rm

docker container ls
docker stop container_id
docker start container_id

docker images
docker rmi

https://docs.docker.com/get-started/part2/#run-the-app
Build the app
Dockerfile
docker build
docker build -t friendlyhello .

docker tag image username/repository:tag
docker tag friendlyhello john/get-started:part1

docker pull
docker push username/repository:tag
docker push