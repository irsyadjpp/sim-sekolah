# AI Platform Architecture Diagrams

## High-Level Architecture

```mermaid
graph TB
    subgraph External
        EC["External Clients<br/>Web, Mobile, API Consumers, Partners"]
    end
    
    EC -->|HTTPS| GW["Gateway Service<br/>Port: 8002<br/>- JWT Authentication<br/>- Request Routing<br/>- Rate Limiting<br/>- API Aggregation<br/>- Security Headers"]
    
    GW -->|REST API| BE["Backend (Go)<br/>- Business Logic<br/>- Data Validation<br/>- Request Orchestration<br/>- Database Operations<br/>- Cache Management<br/>- File Storage"]
    
    BE -->|gRPC Sync| AI["AI Platform Services (Internal)"]
    BE -->|RabbitMQ Async| AI
    
    subgraph AI_Services["AI Platform Services"]
        PS["Parser Service<br/>gRPC: 50051<br/>Queue: parser.q"]
        VS["Vision Service<br/>gRPC: 50055<br/>Queue: vision.q"]
        CS["Chunk Service<br/>gRPC: 50056<br/>Queue: chunk.q"]
        MS["Metadata Service<br/>gRPC: 50057<br/>Queue: metadata.q"]
        ES["Embedding Service<br/>gRPC: 50052<br/>Queue: embed.q"]
        RS["Retrieval Service<br/>gRPC: 50054<br/>Queue: retrieval.q"]
        RRS["Reranking Service<br/>gRPC: 50058<br/>Queue: rerank.q"]
        GS["Generation Service<br/>gRPC: 50053<br/>Queue: generation.q"]
    end
    
    AI_Services --> INF["Supporting Infrastructure"]
    
    subgraph Infrastructure["Supporting Infrastructure"]
        PG["PostgreSQL<br/>Port: 5432<br/>- User Data<br/>- Content<br/>- Metadata"]
        QD["Qdrant<br/>Port: 6333<br/>- Vectors<br/>- Embeddings<br/>- Chunks"]
        RD["Redis<br/>Port: 6379<br/>- Cache<br/>- Sessions<br/>- Rate Limit"]
        RMQ["RabbitMQ<br/>Port: 5672 (AMQP)<br/>- Task Queues<br/>- Result Queues"]
        MN["MinIO<br/>Port: 9000<br/>- Documents<br/>- Images<br/>- Files"]
    end
    
    style EC fill:#e1f5ff
    style GW fill:#fff4e6
    style BE fill:#e8f5e9
    style AI_Services fill:#f3e5f5
    style Infrastructure fill:#fce4ec
```

## Communication Flow Diagrams

### Synchronous Communication (gRPC)

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant B as Backend (Go)
    participant P as Parser Service
    participant Q as Qdrant
    
    C->>G: HTTPS Request
    G->>B: REST API
    B->>P: gRPC Call
    P->>Q: Query Vectors
    Q-->>P: Vector Results
    P-->>B: gRPC Response
    B-->>G: REST Response
    G-->>C: HTTPS Response
    
    Note over C,Q: Use Case: Real-time retrieval, synchronous operations
    Note over C,Q: Latency: Low (< 500ms)
```

### Asynchronous Communication (RabbitMQ)

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant B as Backend (Go)
    participant RMQ as RabbitMQ
    participant P as Parser Service
    participant RMQR as RabbitMQ (Result)
    
    C->>G: HTTPS Request
    G->>B: REST API
    B->>RMQ: Publish to parser.queue
    
    RMQ->>P: Consume Message
    P->>P: Process Document
    P->>RMQR: Publish Result
    
    RMQR->>B: Consume Result
    B-->>G: REST Response
    G-->>C: HTTPS Response
    
    Note over C,RMQR: Use Case: Document parsing, embedding generation, batch operations
    Note over C,RMQR: Latency: Variable (depends on task complexity)
```

## Service Interaction Diagram

### Document Processing Pipeline

```mermaid
graph TD
    C["Client"] -->|Upload Document| GW["Gateway"]
    GW -->|Forward to Backend| BE["Backend"]
    BE -->|Publish to RabbitMQ| RMQ1["RabbitMQ<br/>parser.q"]
    RMQ1 --> PS["Parser Service"]
    PS -->|Process Document| PS
    PS -->|Extract Text| PS
    PS -->|Extract Images| PS
    PS -->|OCR Processing| PS
    PS -->|Publish to RabbitMQ| RMQ2["RabbitMQ<br/>vision.q"]
    RMQ2 --> VS["Vision Service"]
    VS -->|Process Images| VS
    VS -->|Publish to RabbitMQ| RMQ3["RabbitMQ<br/>chunk.q"]
    RMQ3 --> CS["Chunk Service"]
    CS -->|Curriculum-aware Chunking| CS
    CS -->|Publish to RabbitMQ| RMQ4["RabbitMQ<br/>metadata.q"]
    RMQ4 --> MS["Metadata Service"]
    MS -->|Enrich Chunks| MS
    MS -->|Publish to RabbitMQ| RMQ5["RabbitMQ<br/>embed.q"]
    RMQ5 --> ES["Embedding Service"]
    ES -->|Generate Embeddings| ES
    ES -->|Store in Qdrant| QD["Qdrant"]
    ES -->|Publish Result| RMQ6["RabbitMQ<br/>parser.r.q"]
    RMQ6 --> BE2["Backend<br/>Consumer"]
    BE2 -->|Return to Client| GW2["Gateway"]
    GW2 -->|Response| C2["Client"]
    
    style C fill:#e1f5ff
    style C2 fill:#e1f5ff
    style PS fill:#fff4e6
    style VS fill:#fff4e6
    style CS fill:#fff4e6
    style MS fill:#fff4e6
    style ES fill:#fff4e6
```

### Query Processing Pipeline

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant B as Backend
    participant RS as Retrieval Service
    participant Q as Qdrant
    participant RRS as Reranking Service
    participant GS as Generation Service
    
    C->>G: Submit Query
    G->>B: Forward to Backend
    B->>RS: gRPC Call
    RS->>Q: Semantic Search
    Q-->>RS: Results
    RS-->>B: Return Results
    
    B->>RRS: gRPC Call
    RRS->>RRS: Re-rank Results
    RRS-->>B: Return Ranked
    
    B->>GS: gRPC Call
    GS->>GS: Generate Response
    GS-->>B: Return Response
    
    B-->>G: Response
    G-->>C: Response
```

## Security Architecture

```mermaid
graph TB
    subgraph Security["Security Layers"]
        L1["Layer 1: Network Security<br/>- Nginx Reverse Proxy<br/>- SSL/TLS Termination<br/>- DDoS Protection<br/>- IP Whitelisting"]
        L2["Layer 2: Gateway Security<br/>- JWT Authentication<br/>- RBAC<br/>- Rate Limiting<br/>- Request Validation<br/>- Security Headers"]
        L3["Layer 3: Backend Security<br/>- Input Validation<br/>- SQL Injection Prevention<br/>- XSS Protection<br/>- CSRF Protection<br/>- Secure Session Management"]
        L4["Layer 4: Service Security<br/>- Internal Network Only<br/>- gRPC with TLS<br/>- RabbitMQ with TLS<br/>- Service-to-Service Auth<br/>- Secret Management"]
        L5["Layer 5: Data Security<br/>- Encryption at Rest<br/>- Encryption in Transit<br/>- Data Masking<br/>- Audit Logging<br/>- Backup & Recovery"]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    
    style L1 fill:#ffebee
    style L2 fill:#fff3e0
    style L3 fill:#e8f5e9
    style L4 fill:#e3f2fd
    style L5 fill:#f3e5f5
```

## Deployment Architecture

### Docker Compose Deployment

```mermaid
graph TB
    subgraph DockerHost["Docker Host"]
        subgraph Network["Docker Network: ai-platform-network"]
            subgraph Services["AI Platform Services"]
                GW["Gateway<br/>:8002"]
                BE["Backend (Go)"]
                PS["Parser<br/>:50051"]
                VS["Vision<br/>:50055"]
                CS["Chunk<br/>:50056"]
                MS["Metadata<br/>:50057"]
                ES["Embedding<br/>:50052"]
                RS["Retrieval<br/>:50054"]
                RRS["Reranking<br/>:50058"]
                GS["Generation<br/>:50053"]
            end
            
            subgraph Infra["Infrastructure"]
                PG["PostgreSQL<br/>:5432"]
                QD["Qdrant<br/>:6333"]
                RD["Redis<br/>:6379"]
                RMQ["RabbitMQ<br/>:5672"]
                MN["MinIO<br/>:9000"]
            end
            
            subgraph Monitoring["Monitoring Stack"]
                PR["Prometheus<br/>:9090"]
                GF["Grafana<br/>:3000"]
                LK["Loki<br/>:3100"]
                TP["Tempo<br/>:3200"]
            end
        end
    end
    
    style GW fill:#fff4e6
    style BE fill:#e8f5e9
    style PS fill:#f3e5f5
    style VS fill:#f3e5f5
    style CS fill:#f3e5f5
    style MS fill:#f3e5f5
    style ES fill:#f3e5f5
    style RS fill:#f3e5f5
    style RRS fill:#f3e5f5
    style GS fill:#f3e5f5
    style PG fill:#e1f5ff
    style QD fill:#e1f5ff
    style RD fill:#e1f5ff
    style RMQ fill:#e1f5ff
    style MN fill:#e1f5ff
    style PR fill:#fce4ec
    style GF fill:#fce4ec
    style LK fill:#fce4ec
    style TP fill:#fce4ec
```

### Kubernetes Deployment

```mermaid
graph TB
    subgraph K8S["Kubernetes Cluster<br/>Namespace: ai-platform"]
        IC["Ingress Controller<br/>Nginx<br/>LoadBalancer"]
        
        GW["Gateway Service<br/>Deployment<br/>Replicas: 3 (HPA: 3-10)<br/>Service: LoadBalancer"]
        
        BE["Backend<br/>Deployment<br/>Replicas: 3 (HPA: 3-10)<br/>Service: ClusterIP"]
        
        subgraph AI_Services["AI Services (Pods)"]
            PS["Parser<br/>2-8 replicas"]
            VS["Vision<br/>2-6 replicas"]
            CS["Chunk<br/>3-10 replicas"]
            MS["Metadata<br/>2-8 replicas"]
            ES["Embedding<br/>2-6 replicas"]
            RS["Retrieval<br/>2-8 replicas"]
            RRS["Reranking<br/>2-6 replicas"]
            GS["Generation<br/>2-6 replicas"]
        end
        
        subgraph Infra_Pods["Infrastructure (Pods)"]
            PG["PostgreSQL<br/>1 replica"]
            QD["Qdrant<br/>3 replicas"]
            RD["Redis<br/>3 replicas"]
            RMQ["RabbitMQ<br/>3 replicas"]
            MN["MinIO<br/>2 replicas"]
        end
        
        subgraph Mon["Monitoring Stack"]
            PR["Prometheus<br/>Deployment"]
            GF["Grafana<br/>Deployment"]
            LK["Loki<br/>StatefulSet"]
            TP["Tempo<br/>Deployment"]
        end
    end
    
    IC --> GW
    GW --> BE
    BE --> AI_Services
    BE --> Infra_Pods
    
    style IC fill:#e1f5ff
    style GW fill:#fff4e6
    style BE fill:#e8f5e9
    style AI_Services fill:#f3e5f5
    style Infra_Pods fill:#e1f5ff
    style Mon fill:#fce4ec
```

## Data Flow Architecture

### Document Upload Flow

```mermaid
graph LR
    C["Client"] --> GW["Gateway"]
    GW --> BE["Backend"]
    BE --> MN["MinIO<br/>Store"]
    BE --> RMQ1["RabbitMQ<br/>Publish"]
    RMQ1 --> PS["Parser Service<br/>Consume"]
    PS --> PS1["Process Document"]
    PS1 --> PS2["Extract Content"]
    PS2 --> VS["Vision Service<br/>via RabbitMQ"]
    VS --> VS1["Process Images"]
    VS1 --> CS["Chunk Service<br/>via RabbitMQ"]
    CS --> CS1["Curriculum-aware Chunking"]
    CS1 --> MS["Metadata Service<br/>via RabbitMQ"]
    MS --> MS1["Enrich Chunks"]
    MS1 --> ES["Embedding Service<br/>via RabbitMQ"]
    ES --> ES1["Generate Embeddings"]
    ES1 --> QD["Qdrant<br/>Store Vectors"]
    ES1 --> RMQ2["RabbitMQ<br/>Publish Result"]
    RMQ2 --> BE2["Backend<br/>Consume Result"]
    BE2 --> DB["Update Database"]
    DB --> GW2["Gateway"]
    GW2 --> C2["Client<br/>Response"]
    
    style C fill:#e1f5ff
    style C2 fill:#e1f5ff
    style PS fill:#fff4e6
    style VS fill:#fff4e6
    style CS fill:#fff4e6
    style MS fill:#fff4e6
    style ES fill:#fff4e6
```

### Query Flow

```mermaid
graph LR
    C["Client"] --> GW["Gateway"]
    GW --> BE["Backend<br/>Query"]
    BE --> RS["Retrieval Service<br/>gRPC"]
    RS --> QD["Qdrant<br/>Semantic Search"]
    QD --> BE1["Backend<br/>Return Results"]
    BE1 --> RRS["Reranking Service<br/>gRPC"]
    RRS --> RRS1["Re-rank Results"]
    RRS1 --> BE2["Backend<br/>Return Ranked"]
    BE2 --> GS["Generation Service<br/>gRPC"]
    GS --> GS1["Generate Response"]
    GS1 --> BE3["Backend<br/>Return Response"]
    BE3 --> GW2["Gateway"]
    GW2 --> C2["Client<br/>Response"]
    
    style C fill:#e1f5ff
    style C2 fill:#e1f5ff
    style RS fill:#fff4e6
    style RRS fill:#fff4e6
    style GS fill:#fff4e6
```

## Monitoring Architecture

```mermaid
graph TB
    subgraph Monitoring["Monitoring Stack"]
        subgraph Metrics["Metrics Collection"]
            S["Services"] --> PE["Prometheus Exporters"]
            PE --> PR["Prometheus Scrape"]
            PR -->|Scrape| GW["Gateway Service<br/>HTTP metrics"]
            PR -->|Scrape| BE["Backend<br/>Go metrics"]
            PR -->|Scrape| AI["AI Services<br/>Python metrics"]
            PR -->|Scrape| INF["Infrastructure<br/>Node, PostgreSQL, Redis,<br/>RabbitMQ, Qdrant"]
        end
        
        subgraph Logs["Log Aggregation"]
            S2["Services"] --> LA["Loki Agents"]
            LA --> LK["Loki"]
            LK --> GL["Grafana Logs"]
            LA -->|Structured JSON logs| S2
            LA -->|Service-specific loggers| S2
            LA -->|Request ID tracing| S2
        end
        
        subgraph Tracing["Distributed Tracing"]
            S3["Services"] --> OTLP["OTLP"]
            OTLP --> TP["Tempo"]
            TP --> GT["Grafana Traces"]
            OTLP -->|Service-to-service tracing| S3
            OTLP -->|Request latency tracking| S3
            OTLP -->|Error tracking| S3
        end
        
        subgraph Viz["Visualization"]
            GD["Grafana Dashboards"]
            GD --> D1["AI Platform Overview"]
            GD --> D2["Service Health Status"]
            GD --> D3["Request Rate & Latency"]
            GD --> D4["Error Rate Tracking"]
            GD --> D5["Resource Utilization"]
            GD --> D6["RabbitMQ Queue Depth"]
            GD --> D7["Qdrant Performance"]
        end
    end
    
    style Metrics fill:#e8f5e9
    style Logs fill:#e1f5ff
    style Tracing fill:#fff4e6
    style Viz fill:#f3e5f5
```

## Port Summary

| Service | REST Port | gRPC Port | RabbitMQ Queue | External Access |
|---------|-----------|-----------|---------------|-----------------|
| Gateway | 8002 | N/A | N/A | Yes (HTTPS) |
| Backend | N/A | N/A | N/A | No (via Gateway) |
| Parser | 8001 (deprecated) | 50051 | parser.queue | No |
| Vision | 8005 (deprecated) | 50055 | vision.queue | No |
| Chunk | 8003 (deprecated) | 50056 | chunk.queue | No |
| Metadata | 8004 (deprecated) | 50057 | metadata.queue | No |
| Embedding | 8006 (deprecated) | 50052 | embedding.queue | No |
| Retrieval | 8007 (deprecated) | 50054 | retrieval.queue | No |
| Reranking | 8008 (deprecated) | 50058 | reranking.queue | No |
| Generation | 8009 (deprecated) | 50053 | generation.queue | No |
| PostgreSQL | 5432 | N/A | N/A | No |
| Qdrant | 6333 | N/A | N/A | No |
| Redis | 6379 | N/A | N/A | No |
| RabbitMQ | 5672 (AMQP) | N/A | N/A | No |
| MinIO | 9000 (API) | N/A | N/A | No |
| Prometheus | 9090 | N/A | N/A | No |
| Grafana | 3000 | N/A | N/A | No |
| Loki | 3100 | N/A | N/A | No |
| Tempo | 3200 | N/A | N/A | No |
