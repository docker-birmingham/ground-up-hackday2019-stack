FROM oracle/graalvm-ce:1.0.0-rc13 as builder

RUN curl http://www.mirrorservice.org/sites/ftp.apache.org/maven/maven-3/3.6.0/binaries/apache-maven-3.6.0-bin.tar.gz | tar -C /opt -xz

ENV PATH=/opt/apache-maven-3.6.0/bin:$PATH
ENV GRAALVM_HOME=/opt/graalvm-ce-1.0.0-rc13/

WORKDIR /work

COPY pom.xml /work/
COPY src /work/src

RUN mvn package -Pnative

FROM cescoffier/native-base:latest

COPY --from=builder /work/target/getting-started-1.0-SNAPSHOT-runner /application

EXPOSE 8080
CMD ["/application", "-Dquarkus.http.host=0.0.0.0"]
