export interface UXEvent {
  id: string;
  type: "feature" | "page_load" | "error" | "abandonment";
  name: string;
  timestamp: string;
  durationMs?: number;
  metadata?: any;
}

class UXAnalyticsService {
  private storageKey = "sim_sekolah_ux_analytics_v1";

  constructor() {
    if (typeof window !== "undefined") {
      this.initGlobalErrorHandler();
    }
  }

  // Retrieve stored events from LocalStorage
  public getEvents(): UXEvent[] {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.error("Failed to parse UX Analytics logs", e);
      return [];
    }
  }

  // Save event locally
  private saveEvent(event: UXEvent) {
    try {
      const events = this.getEvents();
      events.push(event);
      // Cap log history to last 200 events to prevent localstorage bloat
      if (events.length > 200) {
        events.shift();
      }
      localStorage.setItem(this.storageKey, JSON.stringify(events));

      // Stream to server log endpoint (optional background sync)
      this.syncToServer(event);
    } catch (e) {
      console.warn("UX Analytics buffering failed:", e);
    }
  }

  // Stream UX data to backend OTel/Loki logging service
  private async syncToServer(event: UXEvent) {
    const token = localStorage.getItem("accessToken");
    if (!token) return;

    try {
      // Disable client log streaming to backend for now to avoid 404 errors
      // await fetch(`${DEFAULTS.API_URL}/api/v1/system/client-logs`, {
      //   method: "POST",
      //   headers: {
      //     Authorization: `Bearer ${token}`,
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify({
      //     level: event.type === "error" ? "ERROR" : "INFO",
      //     message: `[UX Analytics] Type: ${event.type} | Name: ${event.name} | Details: ${JSON.stringify(event.metadata || {})}`,
      //     context: {
      //       event_id: event.id,
      //       duration_ms: event.durationMs,
      //       timestamp: event.timestamp,
      //     }
      //   }),
      // });
      console.debug(`[UX Analytics Sync Pending] ${event.type}: ${event.name}`);
    } catch (e) {
      // Fail silently in background
    }
  }

  // 1. Track features heavily used
  public trackFeature(featureName: string, metadata?: any) {
    const event: UXEvent = {
      id: crypto.randomUUID(),
      type: "feature",
      name: featureName,
      timestamp: new Date().toISOString(),
      metadata,
    };
    this.saveEvent(event);
    console.debug(`[UX Analytics] Feature Tracked: ${featureName}`, metadata);
  }

  // 2. Track page performance and load times
  public trackPageLoad(pagePath: string, durationMs: number) {
    const event: UXEvent = {
      id: crypto.randomUUID(),
      type: "page_load",
      name: pagePath,
      timestamp: new Date().toISOString(),
      durationMs,
      metadata: {
        path: pagePath,
        performance_rating: durationMs > 1000 ? "Slow" : durationMs > 500 ? "Average" : "Excellent",
      },
    };
    this.saveEvent(event);
    console.debug(`[UX Analytics] Page Load Time: ${pagePath} - ${durationMs}ms`);
  }

  // 3. Track client errors
  public trackError(errorName: string, errorMessage: string, stack?: string) {
    const event: UXEvent = {
      id: crypto.randomUUID(),
      type: "error",
      name: errorName,
      timestamp: new Date().toISOString(),
      metadata: {
        message: errorMessage,
        stack: stack?.substring(0, 300),
        url: window.location.href,
        userAgent: navigator.userAgent,
      },
    };
    this.saveEvent(event);
    console.error(`[UX Analytics] Captured Error: ${errorName} - ${errorMessage}`);
  }

  // 4. Track Flow Abandonment (e.g. starting a form and leaving without saving)
  public trackFlowAbandonment(flowName: string, stepReached: string, reason: string) {
    const event: UXEvent = {
      id: crypto.randomUUID(),
      type: "abandonment",
      name: flowName,
      timestamp: new Date().toISOString(),
      metadata: {
        stepReached,
        reason,
        url: window.location.href,
      },
    };
    this.saveEvent(event);
    console.debug(`[UX Analytics] Flow Abandonment: ${flowName} at step ${stepReached} (${reason})`);
  }

  // Auto-initialize global JavaScript error tracking
  private initGlobalErrorHandler() {
    window.addEventListener("error", (ev) => {
      this.trackError("RuntimeError", ev.message, ev.error?.stack);
    });

    window.addEventListener("unhandledrejection", (ev) => {
      this.trackError("PromiseRejection", String(ev.reason?.message || ev.reason));
    });
  }

  // Compute calculated metrics for dashboard widgets
  public getAnalyticsSummary() {
    const events = this.getEvents();

    // Top features
    const features: Record<string, number> = {};
    const pageLoads: Record<string, { totalTime: number; count: number }> = {};
    const errors: Record<string, number> = {};
    const abandonments: Record<string, number> = {};

    events.forEach((e) => {
      if (e.type === "feature") {
        features[e.name] = (features[e.name] || 0) + 1;
      } else if (e.type === "page_load" && e.durationMs !== undefined) {
        if (!pageLoads[e.name]) {
          pageLoads[e.name] = { totalTime: 0, count: 0 };
        }
        pageLoads[e.name].totalTime += e.durationMs;
        pageLoads[e.name].count += 1;
      } else if (e.type === "error") {
        errors[e.name] = (errors[e.name] || 0) + 1;
      } else if (e.type === "abandonment") {
        abandonments[e.name] = (abandonments[e.name] || 0) + 1;
      }
    });

    const topFeatures = Object.entries(features)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count);

    const slowPages = Object.entries(pageLoads)
      .map(([name, data]) => ({ name, averageTime: Math.round(data.totalTime / data.count) }))
      .sort((a, b) => b.averageTime - a.averageTime);

    const topErrors = Object.entries(errors)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count);

    const topAbandonments = Object.entries(abandonments)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count);

    return {
      totalLogsCount: events.length,
      topFeatures,
      slowPages,
      topErrors,
      topAbandonments,
    };
  }

  // Reset local buffer
  public clearLogs() {
    localStorage.removeItem(this.storageKey);
  }
}

export const uxAnalytics = new UXAnalyticsService();
