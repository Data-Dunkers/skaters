FROM alpine:latest

# Define the PocketBase version
ARG PB_VERSION=0.22.21

# Install dependencies needed to download and extract PocketBase
RUN apk add --no-cache ca-certificates unzip wget curl

# Download and unzip PocketBase
ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/ \
    && rm /tmp/pb.zip \
    && chmod +x /pb/pocketbase

EXPOSE 8090

# Start PocketBase listening on all interfaces
CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8090", "--dir=/pb/pb_data", "--publicDir=/pb/pb_public"]