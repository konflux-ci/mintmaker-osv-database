FROM quay.io/konflux-ci/mintmaker:latest as builder
RUN /osv-generator -destination-dir /tmp/osv-db -container-filename docker.nedb -rpm-filename rpm.nedb -days 120
RUN rm -f /tmp/osv-db/osv-offline.zip

FROM registry.access.redhat.com/ubi9/ubi-minimal:9.5@sha256:b87097994ed62fbf1de70bc75debe8dacf3ea6e00dd577d74503ef66452c59d6
WORKDIR /
COPY --from=builder /tmp/osv-db /data/osv-db

# It is mandatory to set these labels
LABEL name="Konflux Mintmaker OSV database"
LABEL description="Konflux Mintmaker OSV database"
LABEL io.k8s.description="Konflux Mintmaker OSV database"
LABEL io.k8s.display-name="mintmaker-osv-db"
LABEL summary="Konflux Mintmaker OSV database"
LABEL com.redhat.component="mintmaker-osv-db"

USER 65532:65532
