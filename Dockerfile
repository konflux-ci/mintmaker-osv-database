FROM quay.io/konflux-ci/mintmaker:latest as builder
RUN /osv-generator -destination-dir /tmp/osv-db -container-filename docker.nedb -rpm-filename rpm.nedb -days 120
RUN rm -f /tmp/osv-db/osv-offline.zip

FROM registry.access.redhat.com/ubi9/ubi-minimal:latest@sha256:7c372902c8d211db2d25c8277ba534a73b92742a334874dced829a63b0f21221
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
