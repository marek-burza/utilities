# Nexus 3

Quick start with Nexus 3:

```bash
mkdir /tmp/nexus-data && sudo chown -R 200 /tmp/nexus-data
docker run -p 8081:8081 -p 8082:8082 --name nexus -v /tmp/nexus-data:/nexus-data -it sonatype/nexus3:3.4.0
```
