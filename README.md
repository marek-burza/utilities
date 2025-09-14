# Sovereign Compute

* [Sovereign Compute](sovereign-compute)

# Other Tools

* AWS CLI - [`amazon/aws-cli`](https://hub.docker.com/r/amazon/aws-cli)
* Azure CLI - [`mcr.microsoft.com/azure-cli`](https://hub.docker.com/_/microsoft-azure-cli)
* Expose Docker host ports on Docker networks - [`qoomon/docker-host`](https://github.com/qoomon/docker-host)
* Powerful tunneling software - [`socat`](https://www.redhat.com/sysadmin/getting-started-socat)
* Forward a service on a local port to an SSH jump server - [`autossh`](https://www.harding.motd.ca/autossh/)

# To Do

- Replace Tailscale ingress with local-only WireGuard
  - https://github.com/ivanmorenoj/k8s-wireguard
  - Bursting into cloud with [kilo](https://github.com/squat/kilo)?
- Add [Kueue](https://github.com/kubernetes-sigs/kueue) controller to the local cluster
- If necessery to govern the queue with a git repo then consider [Argo](https://github.com/argoproj) (possibly consider [Weave GitOps](https://github.com/weaveworks/weave-gitops) community driven project, and [Flux](https://github.com/fluxcd/flux2))
- Auto-update sovereign-utilities with https://github.com/containrrr/watchtower
- Replace gotty & filebrowser by VNC-in-a-container?
  - https://www.baeldung.com/linux/docker-container-gui-applications
  - https://akhilsharmaa.medium.com/ubuntu-gui-inside-docker-vnc-server-setup-f601687ec66d
- Consider switching from `Ansible` to [`pyinfra-dev/pyinfra`](https://github.com/pyinfra-dev/pyinfra)

# Secure the Cluster

- How to secure anything - https://github.com/veeral-patel/how-to-secure-anything
- Add this to CI? - https://github.com/ZeroPathAI/zeropathai
- Attack surface mapping and asset discovery - https://github.com/owasp-amass/amass
- All-in-one OSINT tool for analysing any website - https://github.com/Lissy93/web-check
- Fast subdomains enumeration tool for penetration testers - https://github.com/aboul3la/Sublist3r
- Certificate search - https://github.com/PaulSec/crt.sh
