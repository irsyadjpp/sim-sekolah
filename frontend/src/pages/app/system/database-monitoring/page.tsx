"use client";

import { useEffect, useState } from "react";

import {
  CheckCircle as CheckCircleIcon,
  Refresh as RefreshIcon,
  Speed as SpeedIcon,
  Storage as StorageIcon,
  Warning as WarningIcon,
} from "@mui/icons-material";
import {
  Alert,
  AlertTitle,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Grid,
  LinearProgress,
  Paper,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Typography,
} from "@mui/material";

interface DatabaseMetrics {
  total_size_bytes: number;
  total_size_formatted: string;
  total_tables: number;
  total_indexes: number;
  total_sequences: number;
  active_connections: number;
  max_connections: number;
  cache_hit_ratio: number;
  collected_at: string;
}

interface TableSize {
  schema_name: string;
  table_name: string;
  size_bytes: number;
  size_formatted: string;
  partition_type: string;
  row_count: number;
  index_size_bytes: number;
  index_size_formatted: string;
}

interface IndexUsage {
  schema_name: string;
  table_name: string;
  index_name: string;
  index_scans: number;
  tuples_read: number;
  tuples_fetched: number;
  index_size_bytes: number;
  index_size_formatted: string;
  recommendation: string;
  priority: string;
}

interface TableStatistics {
  schema_name: string;
  table_name: string;
  live_tuples: number;
  dead_tuples: number;
  last_vacuum: string | null;
  last_autovacuum: string | null;
  vacuum_count: number;
  autovacuum_count: number;
  bloat_percentage: number;
  requires_action: boolean;
  recommended_action: string;
}

interface SecurityEvent {
  id: string;
  event_type: string;
  event_description: string;
  severity: string;
  user_id: string;
  ip_address: string;
  event_time: string;
  additional_data: string;
}

interface DatabaseHealth {
  overall_status: string;
  health_score: number;
  issues: string[];
  recommendations: string[];
  last_check: string;
}

export default function DatabaseMonitoringPage() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState<DatabaseMetrics | null>(null);
  const [tableSizes, setTableSizes] = useState<TableSize[]>([]);
  const [indexUsage, setIndexUsage] = useState<IndexUsage[]>([]);
  const [tableStats, setTableStats] = useState<TableStatistics[]>([]);
  const [securityEvents, setSecurityEvents] = useState<SecurityEvent[]>([]);
  const [health, setHealth] = useState<DatabaseHealth | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch database metrics
      const metricsResponse = await fetch("/api/database-monitoring/metrics");
      const metricsData = await metricsResponse.json();
      if (metricsData.success) {
        setMetrics(metricsData.data);
      }

      // Fetch table sizes
      const tableSizesResponse = await fetch("/api/database-monitoring/tables/sizes?limit=20");
      const tableSizesData = await tableSizesResponse.json();
      if (tableSizesData.success) {
        setTableSizes(tableSizesData.data);
      }

      // Fetch index usage
      const indexUsageResponse = await fetch("/api/database-monitoring/indexes/usage?limit=20");
      const indexUsageData = await indexUsageResponse.json();
      if (indexUsageData.success) {
        setIndexUsage(indexUsageData.data);
      }

      // Fetch table statistics
      const tableStatsResponse = await fetch("/api/database-monitoring/tables/statistics");
      const tableStatsData = await tableStatsResponse.json();
      if (tableStatsData.success) {
        setTableStats(tableStatsData.data);
      }

      // Fetch security events
      const securityEventsResponse = await fetch("/api/database-monitoring/security/events?time_range=24h");
      const securityEventsData = await securityEventsResponse.json();
      if (securityEventsData.success) {
        setSecurityEvents(securityEventsData.data);
      }

      // Fetch database health
      const healthResponse = await fetch("/api/database-monitoring/health");
      const healthData = await healthResponse.json();
      if (healthData.success) {
        setHealth(healthData.data);
      }
    } catch (err) {
      setError("Failed to fetch database monitoring data");
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case "HEALTHY":
        return "success";
      case "WARNING":
        return "warning";
      case "CRITICAL":
        return "error";
      default:
        return "info";
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "HIGH":
        return "error";
      case "MEDIUM":
        return "warning";
      case "LOW":
        return "info";
      default:
        return "default";
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "CRITICAL":
        return "error";
      case "HIGH":
        return "error";
      case "MEDIUM":
        return "warning";
      case "LOW":
        return "info";
      default:
        return "default";
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" fontWeight="bold">
          Database Monitoring
        </Typography>
        <Button variant="outlined" startIcon={<RefreshIcon />} onClick={fetchData} disabled={loading}>
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          <AlertTitle>Error</AlertTitle>
          {error}
        </Alert>
      )}

      {health && (
        <Alert severity={getHealthColor(health.overall_status) as any} sx={{ mb: 3 }}>
          <AlertTitle>
            Database Health: {health.overall_status} (Score: {health.health_score}/100)
          </AlertTitle>
          <Box sx={{ mt: 1 }}>
            <Typography variant="body2">Last checked: {new Date(health.last_check).toLocaleString()}</Typography>
            {health.issues.length > 0 && (
              <Box sx={{ mt: 1 }}>
                <Typography variant="subtitle2" fontWeight="bold">
                  Issues:
                </Typography>
                {health.issues.map((issue, index) => (
                  <Typography key={index} variant="body2">
                    • {issue}
                  </Typography>
                ))}
              </Box>
            )}
          </Box>
        </Alert>
      )}

      <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Overview" />
        <Tab label="Tables" />
        <Tab label="Indexes" />
        <Tab label="Statistics" />
        <Tab label="Security" />
      </Tabs>

      {activeTab === 0 && metrics && (
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Database Size
                  </Typography>
                  <StorageIcon color="action" />
                </Box>
                <Typography variant="h4" fontWeight="bold">
                  {metrics.total_size_formatted}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {metrics.total_tables} tables, {metrics.total_indexes} indexes
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Cache Hit Ratio
                  </Typography>
                  <SpeedIcon color="action" />
                </Box>
                <Typography variant="h4" fontWeight="bold">
                  {(metrics.cache_hit_ratio * 100).toFixed(2)}%
                </Typography>
                <LinearProgress variant="determinate" value={metrics.cache_hit_ratio * 100} sx={{ mt: 1 }} />
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Connections
                  </Typography>
                  <SpeedIcon color="action" />
                </Box>
                <Typography variant="h4" fontWeight="bold">
                  {metrics.active_connections}/{metrics.max_connections}
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={(metrics.active_connections / metrics.max_connections) * 100}
                  sx={{ mt: 1 }}
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Sequences
                  </Typography>
                  <StorageIcon color="action" />
                </Box>
                <Typography variant="h4" fontWeight="bold">
                  {metrics.total_sequences}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Auto-increment sequences
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Table Sizes
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Schema</TableCell>
                  <TableCell>Table Name</TableCell>
                  <TableCell>Size</TableCell>
                  <TableCell>Rows</TableCell>
                  <TableCell>Index Size</TableCell>
                  <TableCell>Type</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tableSizes.map((table) => (
                  <TableRow key={`${table.schema_name}.${table.table_name}`}>
                    <TableCell>{table.schema_name}</TableCell>
                    <TableCell>{table.table_name}</TableCell>
                    <TableCell>{table.size_formatted}</TableCell>
                    <TableCell>{table.row_count.toLocaleString()}</TableCell>
                    <TableCell>{table.index_size_formatted}</TableCell>
                    <TableCell>
                      <Chip
                        label={table.partition_type}
                        size="small"
                        color={table.partition_type === "REGULAR" ? "default" : "primary"}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {activeTab === 2 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Index Usage
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Schema</TableCell>
                  <TableCell>Table</TableCell>
                  <TableCell>Index Name</TableCell>
                  <TableCell>Scans</TableCell>
                  <TableCell>Tuples Read</TableCell>
                  <TableCell>Size</TableCell>
                  <TableCell>Recommendation</TableCell>
                  <TableCell>Priority</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {indexUsage.map((index) => (
                  <TableRow key={`${index.schema_name}.${index.table_name}.${index.index_name}`}>
                    <TableCell>{index.schema_name}</TableCell>
                    <TableCell>{index.table_name}</TableCell>
                    <TableCell>{index.index_name}</TableCell>
                    <TableCell>{index.index_scans.toLocaleString()}</TableCell>
                    <TableCell>{index.tuples_read.toLocaleString()}</TableCell>
                    <TableCell>{index.index_size_formatted}</TableCell>
                    <TableCell>{index.recommendation}</TableCell>
                    <TableCell>
                      <Chip label={index.priority} size="small" color={getPriorityColor(index.priority) as any} />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {activeTab === 3 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Table Statistics
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Schema</TableCell>
                  <TableCell>Table</TableCell>
                  <TableCell>Live Tuples</TableCell>
                  <TableCell>Dead Tuples</TableCell>
                  <TableCell>Bloat %</TableCell>
                  <TableCell>Last Vacuum</TableCell>
                  <TableCell>Requires Action</TableCell>
                  <TableCell>Recommended Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tableStats.map((stat) => (
                  <TableRow key={`${stat.schema_name}.${stat.table_name}`}>
                    <TableCell>{stat.schema_name}</TableCell>
                    <TableCell>{stat.table_name}</TableCell>
                    <TableCell>{stat.live_tuples.toLocaleString()}</TableCell>
                    <TableCell>{stat.dead_tuples.toLocaleString()}</TableCell>
                    <TableCell>{stat.bloat_percentage.toFixed(2)}%</TableCell>
                    <TableCell>
                      {stat.last_autovacuum ? new Date(stat.last_autovacuum).toLocaleDateString() : "Never"}
                    </TableCell>
                    <TableCell>
                      {stat.requires_action ? (
                        <Chip icon={<WarningIcon />} label="Yes" size="small" color="warning" />
                      ) : (
                        <Chip icon={<CheckCircleIcon />} label="No" size="small" color="success" />
                      )}
                    </TableCell>
                    <TableCell>{stat.recommended_action}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {activeTab === 4 && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Security Events (Last 24h)
          </Typography>
          {securityEvents.length === 0 ? (
            <Alert severity="success">
              <AlertTitle>No Security Events</AlertTitle>
              No security events detected in the last 24 hours.
            </Alert>
          ) : (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Event Type</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell>Severity</TableCell>
                    <TableCell>User ID</TableCell>
                    <TableCell>IP Address</TableCell>
                    <TableCell>Time</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {securityEvents.map((event) => (
                    <TableRow key={event.id}>
                      <TableCell>{event.event_type}</TableCell>
                      <TableCell>{event.event_description}</TableCell>
                      <TableCell>
                        <Chip label={event.severity} size="small" color={getSeverityColor(event.severity) as any} />
                      </TableCell>
                      <TableCell>{event.user_id}</TableCell>
                      <TableCell>{event.ip_address}</TableCell>
                      <TableCell>{new Date(event.event_time).toLocaleString()}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Paper>
      )}
    </Box>
  );
}
