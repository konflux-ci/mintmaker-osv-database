FROM quay.io/konflux-ci/mintmaker:latest as builder
RUN /osv-generator -destination-dir /tmp/osv-db -container-filename docker.nedb -rpm-filename rpm.nedb -days 120
RUN rm -f /tmp/osv-db/osv-offline.zip

FROM registry.access.redhat.com/ubi9/ubi-minimal:latest@sha256:b9b10f42d7eba7ad4a6d5ef26b7d34fdc892b2ffe59b8d0372ec884008569eb6
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
