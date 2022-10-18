# How to build the image, run the container and use the program.


## Install and start the program

1 Download the files from this repom navigate to the folder with the docker file and build the container by running the command

    docker compose build zebralint

2 Change the path-to-local-folder in the docker-compose.yml to a local directory on your computer which has the .tex files you wish to format

This is where you should edit:

    volumes: [path-to-local-folder:/home/app/tex]



3 To start the container run the command

    docker compose run --rm zebralint

## Use the program
While inside the container you can format files and save them as new files by using the command

    python zebralint.py ./tex/<file-to-be-formatted> -n ./tex/<new-file>

You can also format the file and override the old file by using the command

    python zebralint.py ./tex/<file-to-be-formatted>

