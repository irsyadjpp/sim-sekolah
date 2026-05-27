# SimSekolah AI SDK (Go)

Go SDK for integrating with the SimSekolah AI Platform.

## Installation

```bash
go get github.com/upt-sdi-bonerate-no-85-kepulauan/simsekolah-ai-sdk
```

## Usage

```go
package main

import (
    "context"
    "time"
    "github.com/upt-sdi-bonerate-no-85-kepulauan/simsekolah-ai-sdk"
)

func main() {
    cfg := simsekolah.Config{
        GatewayServiceAddr: "localhost:8002",
        Timeout: time.Second * 30,
    }
    
    client, err := simsekolah.NewClient(cfg)
    if err != nil {
        panic(err)
    }
    defer client.Close()
    
    // Use the client
    err = client.HealthCheck(context.Background())
    if err != nil {
        panic(err)
    }
}
```

## Features

- gRPC client for AI Platform services
- Automatic connection management
- Health check support
- Configurable timeouts

## Configuration

The SDK accepts the following configuration options:

- `GatewayServiceAddr`: Address of the Gateway Service (default: localhost:8002)
- `Timeout`: Request timeout (default: 30s)

## Examples

See the `examples/` directory for more usage examples.
