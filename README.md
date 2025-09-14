# Sovereign Compute

* [Sovereign Compute](sovereign-compute)

# Other Tools

* AWS CLI - [`amazon/aws-cli`](https://hub.docker.com/r/amazon/aws-cli)
* Azure CLI - [`mcr.microsoft.com/azure-cli`](https://hub.docker.com/_/microsoft-azure-cli)

# To Do

- Add [Kueue](https://github.com/kubernetes-sigs/kueue) controller to the local cluster
- If necessery to govern the queue with a git repo then consider [Argo](https://github.com/argoproj) (possibly consider [Weave GitOps](https://github.com/weaveworks/weave-gitops) community driven project, and [Flux](https://github.com/fluxcd/flux2))
- Replace gotty & filebrowser by VNC-in-a-container?
  - https://www.baeldung.com/linux/docker-container-gui-applications
  - https://akhilsharmaa.medium.com/ubuntu-gui-inside-docker-vnc-server-setup-f601687ec66d
- Consider switching from `Ansible` to [`pyinfra-dev/pyinfra`](https://github.com/pyinfra-dev/pyinfra)

# Secure the Cluster

- How to secure anything - https://github.com/veeral-patel/how-to-secure-anything
- Add this to CI? - https://github.com/ZeroPathAI/zeropathai
