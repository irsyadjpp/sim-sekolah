# Troubleshooting Guide

## Enterprise Educational AI Platform

---

# Common Issues and Solutions

## Service Startup Issues

### Issue: Service fails to start

#### Symptoms
- Service container exits immediately
- Health check fails
- Service logs show connection errors

#### Possible Causes
- Database connection failure
- Missing environment variables
- Port conflicts
- Dependency issues

#### Troubleshooting Steps

1. **Check service logs**
```bash
docker logs <service-name>
kubectl logs <pod-name>
```

2. **Verify environment variables**
```bash
docker exec <container-name> env
kubectl exec <pod-name> -- env
```

3. **Check database connectivity**
```bash
docker exec <container-name> pg_isready -h <db-host> -p 5432
```

4. **Check port availability**
```bash
netstat -tuln | grep <port>
lsof -i :<port>
```

5. **Verify dependencies**
```bash
docker exec <container-name> pip list
docker exec <container-name> python -c "import <module>"
```

---

## Performance Issues

### Issue: Slow response times

#### Symptoms
- API requests timeout
- High latency
- Poor user experience

#### Possible Causes
- Database query performance
- Network latency
- Resource constraints
- Inefficient code

#### Troubleshooting Steps

1. **Check system resources**
```bash
top
htop
docker stats
kubectl top pods
```

2. **Check database performance**
```sql
SELECT * FROM pg_stat_activity WHERE state = 'active';
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

3. **Check network latency**
```bash
ping <service-host>
traceroute <service-host>
```

4. **Profile application**
```python
# Add performance profiling
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# ... code ...
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(20)
```

---

## Memory Issues

### Issue: Out of memory errors

#### Symptoms
- Service crashes with OOM
- High memory usage
- Swap usage increases

#### Possible Causes
- Memory leaks
- Large dataset processing
- Insufficient resources
- Caching issues

#### Troubleshooting Steps

1. **Check memory usage**
```bash
free -h
docker stats --no-stream
kubectl describe pod <pod-name>
```

2. **Check for memory leaks**
```python
import tracemalloc
tracemalloc.start()

# ... code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

3. **Increase memory limits**
```yaml
# Kubernetes
resources:
  limits:
    memory: "2Gi"
  requests:
    memory: "1Gi"

# Docker
docker run -m 2g <image>
```

---

## Database Issues

### Issue: Database connection failures

#### Symptoms
- Connection refused
- Connection timeout
- Too many connections

#### Possible Causes
- Database not running
- Network issues
- Connection pool exhaustion
- Authentication issues

#### Troubleshooting Steps

1. **Check database status**
```bash
sudo systemctl status postgresql
docker ps | grep postgres
kubectl get pods | grep postgres
```

2. **Test database connection**
```bash
psql -h <host> -p 5432 -U <user> -d <database>
```

3. **Check connection pool**
```sql
SELECT count(*) FROM pg_stat_activity;
SELECT * FROM pg_stat_activity WHERE datname = '<database>';
```

4. **Check database logs**
```bash
tail -f /var/log/postgresql/postgresql.log
docker logs <postgres-container>
```

---

## Vector Database Issues

### Issue: Qdrant search failures

#### Symptoms
- Search returns no results
- Search timeout
- Poor search quality

#### Possible Causes
- Collection not created
- No indexed vectors
- Embedding mismatch
- Network issues

#### Troubleshooting Steps

1. **Check Qdrant status**
```bash
curl http://qdrant:6333/health
curl http://qdrant:6333/collections
```

2. **Check collection status**
```bash
curl http://qdrant:6333/collections/<collection-name>
```

3. **Verify embeddings**
```python
# Check embedding dimensions
import numpy as np
embedding = model.encode("test")
print(f"Embedding shape: {embedding.shape}")
```

4. **Test search manually**
```bash
curl -X POST "http://qdrant:6333/collections/<collection-name>/points/search" \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, 0.3],
    "limit": 10
  }'
```

---

## Object Storage Issues

### Issue: MinIO upload/download failures

#### Symptoms
- Upload timeout
- Download fails
- File not found

#### Possible Causes
- Bucket not created
- Permission issues
- Network issues
- Storage full

#### Troubleshooting Steps

1. **Check MinIO status**
```bash
curl http://minio:9000/minio/health/live
mc alias list
```

2. **Check bucket existence**
```bash
mc ls aiplatform/
mc ls aiplatform/documents
```

3. **Check permissions**
```bash
mc admin policy info aiplatform
```

4. **Check storage space**
```bash
df -h
mc admin info aiplatform
```

---

## Authentication Issues

### Issue: Authentication failures

#### Symptoms
- 401 Unauthorized
- Token validation fails
- Login fails

#### Possible Causes
- Invalid credentials
- Token expired
- JWT configuration issues
- Database authentication issues

#### Troubleshooting Steps

1. **Verify JWT configuration**
```bash
# Check environment variables
echo $JWT_SECRET
echo $JWT_ALGORITHM
```

2. **Test token generation**
```python
import jwt
token = jwt.encode({"user": "test"}, "secret", algorithm="HS256")
print(token)
```

3. **Test token validation**
```python
decoded = jwt.decode(token, "secret", algorithms=["HS256"])
print(decoded)
```

4. **Check database authentication**
```sql
SELECT * FROM users WHERE username = '<username>';
```

---

## Logging Issues

### Issue: Logs not appearing

#### Symptoms
- No logs in monitoring
- Logs missing events
- Log format incorrect

#### Possible Causes
- Log level too high
- Log aggregation issues
- Log service down
- Configuration issues

#### Troubleshooting Steps

1. **Check log level**
```bash
# Check environment variable
echo $LOG_LEVEL
```

2. **Check log aggregation**
```bash
# Check Loki
curl http://loki:3100/ready
# Check Prometheus
curl http://prometheus:9090/-/healthy
```

3. **Check log files**
```bash
tail -f /var/log/ai-platform/*.log
docker logs <container-name> --tail 100
```

4. **Test logging**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

---

## Monitoring Issues

### Issue: Metrics not appearing

#### Symptoms
- No metrics in Grafana
- Metrics missing data
- Alerts not firing

#### Possible Causes
- Prometheus not scraping
- Metrics endpoint down
- Configuration issues
- Network issues

#### Troubleshooting Steps

1. **Check Prometheus status**
```bash
curl http://prometheus:9090/-/healthy
curl http://prometheus:9090/api/v1/targets
```

2. **Check metrics endpoint**
```bash
curl http://<service>:<port>/metrics
```

3. **Check Prometheus configuration**
```bash
cat /etc/prometheus/prometheus.yml
```

4. **Check Grafana data source**
```bash
# In Grafana UI
# Configuration > Data Sources > Prometheus > Test
```

---

## Network Issues

### Issue: Service communication failures

#### Symptoms
- Connection refused
- Connection timeout
- DNS resolution failures

#### Possible Causes
- Network policies
- Firewall rules
- DNS issues
- Service discovery issues

#### Troubleshooting Steps

1. **Check network connectivity**
```bash
ping <service-host>
telnet <service-host> <port>
nc -zv <service-host> <port>
```

2. **Check DNS resolution**
```bash
nslookup <service-host>
dig <service-host>
```

3. **Check network policies**
```bash
kubectl get networkpolicies
kubectl describe networkpolicy <policy-name>
```

4. **Check firewall rules**
```bash
sudo iptables -L
sudo ufw status
```

---

## Escalation Procedures

### When to Escalate

1. **Critical Issues**
   - Complete service outage
   - Data loss
   - Security breach
   - SLA violation

2. **High Priority Issues**
   - Service degradation
   - Performance issues
   - Data corruption
   - Authentication failures

3. **Medium Priority Issues**
   - Intermittent failures
   - Performance degradation
   - Configuration issues

### Escalation Contacts

- **On-call Engineer**: +62-XXX-XXXX-XXXX
- **Engineering Manager**: +62-XXX-XXXX-XXXX
- **CTO**: +62-XXX-XXXX-XXXX
- **Security Team**: security@example.com

---

# Prevention

## Regular Maintenance

- Weekly: Review logs and metrics
- Monthly: Test backup restoration
- Quarterly: Full DR test
- Annually: Review and update procedures

## Monitoring

- Set up alerts for critical metrics
- Monitor system resources
- Track error rates
- Monitor performance SLAs

## Documentation

- Keep troubleshooting guide updated
- Document new issues and solutions
- Share lessons learned
- Maintain runbooks
