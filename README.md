# Dockerized SSH over Tor

To expose SSH over Tor from a remote box run this command on it:

     docker run --detach --restart always --network host --volume $PWD/tor:/var/lib/tor ghcr.io/altermarkive/ssh-over-tor:latest

The file `$PWD/tor/torssh/hostname` will then contain the remote address and remote secret to be used to connect to this box.

To connect to the remote box use this command:

     docker run --rm -it --env ADDRESS=$REMOTE_ADDRESS --env SECRET=$REMOTE_SECRET --env USER=$REMOTE_USER --volume $HOME/.ssh:/root/.ssh altermarkive/ssh-over-tor


# Source materials

* [https://medium.com/@tzhenghao/how-to-ssh-over-tor-onion-service-c6d06194147](https://medium.com/@tzhenghao/how-to-ssh-over-tor-onion-service-c6d06194147)
* [https://www.maths.tcd.ie/~fionn/misc/ssh_hidden_service.php](https://www.maths.tcd.ie/~fionn/misc/ssh_hidden_service.php)
* [Karangejo: SSH Over Tor](https://karangejo.com/posts/18)
