FROM debian:latest

# Disable interactive configuration prompts
ARG DEBIAN_FRONTEND=noninteractive

COPY install_utilities.sh /tmp/install_utilities.sh
RUN /bin/sh /tmp/install_utilities.sh && rm /tmp/install_utilities.sh

COPY install_tailscale.sh /tmp/install_tailscale.sh
RUN /bin/sh /tmp/install_tailscale.sh && rm /tmp/install_tailscale.sh

COPY install_coder.sh /tmp/install_coder.sh
RUN /bin/sh /tmp/install_coder.sh && rm /tmp/install_coder.sh

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/bin/bash"]
