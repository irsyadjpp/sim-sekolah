# Step 1: Build the statically linked Go binary using Go 1.26.2
FROM golang:1.26.2-alpine AS builder

WORKDIR /app

# Copy dependency manifests
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Compile 100% statically linked Go binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -o sim-sekolah cmd/main.go

# Step 2: Minimal run stage
FROM alpine:3.19

WORKDIR /app

# Copy the statically linked binary from builder
COPY --from=builder /app/sim-sekolah ./main

# Copy other necessary assets and configurations
COPY docs ./docs
COPY .env.example ./.env
COPY config.yaml .
COPY migrations ./migrations

# Expose port
EXPOSE 8080

# Command to run
CMD ["./main"]
