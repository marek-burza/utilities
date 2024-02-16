FROM alpine:3.13.5

RUN apk add --no-cache --update openssh

ADD sshd_config /etc/ssh/sshd_config
ADD entrypoint.sh /entrypoint.sh

RUN rm -rf /etc/ssh/ssh_host_*_key

RUN adduser -s "/bin/true" -D -u 1000 -G "users" "user" && \
    passwd -u "user" &> /dev/null && \
    mkdir -p /home/user/.ssh

EXPOSE 22

ENTRYPOINT [ "/bin/sh", "/entrypoint.sh" ]
CMD [ "/usr/sbin/sshd", "-D", "-e" ]
