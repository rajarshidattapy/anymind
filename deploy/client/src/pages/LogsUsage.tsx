import { useState, useEffect } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { mockUsageMetrics, generateMockLogs, LogEntry } from '@/lib/mock-data';
import { cn } from '@/lib/utils';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, Clock, AlertTriangle } from 'lucide-react';

export default function LogsUsage() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [filter, setFilter] = useState<'all' | 'build' | 'runtime' | 'errors'>('all');

  useEffect(() => {
    setLogs(generateMockLogs(30));
  }, []);

  // Real-time log simulation
  useEffect(() => {
    const interval = setInterval(() => {
      const newLog = generateMockLogs(1)[0];
      newLog.timestamp = new Date().toISOString();
      newLog.id = `log_${Date.now()}`;
      setLogs((prev) => [newLog, ...prev.slice(0, 49)]);
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  const filteredLogs = logs.filter((log) => {
    if (filter === 'all') return true;
    if (filter === 'errors') return log.level === 'error' || log.level === 'warn';
    return log.type === filter;
  });

  const levelBadges = {
    info: 'bg-muted/50 text-muted-foreground',
    warn: 'bg-status-building/20 text-status-building',
    error: 'bg-status-failed/20 text-status-failed',
    debug: 'bg-accent/20 text-accent',
  };

  const metrics = [
    {
      label: 'Total Calls',
      value: mockUsageMetrics.totalCalls.toLocaleString(),
      icon: Activity,
      color: 'text-primary',
    },
    {
      label: 'Avg Latency',
      value: `${mockUsageMetrics.avgLatency}ms`,
      icon: Clock,
      color: 'text-accent',
    },
    {
      label: 'Errors',
      value: mockUsageMetrics.errorCount.toLocaleString(),
      icon: AlertTriangle,
      color: 'text-status-failed',
    },
  ];

  return (
    <MainLayout>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Logs & Usage</h1>
        <p className="mt-1 text-muted-foreground">
          Monitor your platform activity and usage metrics
        </p>
      </div>

      {/* Metrics Cards */}
      <div className="mb-8 grid gap-4 sm:grid-cols-3">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="rounded-xl border border-border bg-card p-6"
          >
            <div className="flex items-center gap-3">
              <div className={cn('rounded-lg bg-muted p-2.5', metric.color)}>
                <metric.icon className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">{metric.label}</p>
                <p className="text-2xl font-bold text-foreground">
                  {metric.value}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Usage Chart */}
      <div className="mb-8 rounded-xl border border-border bg-card p-6">
        <h2 className="mb-6 text-lg font-semibold text-foreground">
          Calls Over Time
        </h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockUsageMetrics.callsOverTime}>
              <XAxis
                dataKey="date"
                stroke="hsl(var(--muted-foreground))"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tickFormatter={(value) =>
                  new Date(value).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                  })
                }
              />
              <YAxis
                stroke="hsl(var(--muted-foreground))"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(222 47% 11%)',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '8px',
                  fontSize: '12px',
                }}
                labelStyle={{ color: 'hsl(var(--muted-foreground))' }}
                itemStyle={{ color: 'hsl(var(--primary))' }}
                formatter={(value: number) => [value.toLocaleString(), 'Calls']}
                labelFormatter={(label) =>
                  new Date(label).toLocaleDateString('en-US', {
                    weekday: 'short',
                    month: 'short',
                    day: 'numeric',
                  })
                }
              />
              <Line
                type="monotone"
                dataKey="calls"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: 'hsl(var(--primary))' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* System Logs */}
      <div className="rounded-xl border border-border bg-card p-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-foreground">System Logs</h2>
          <div className="flex gap-2">
            {(['all', 'build', 'runtime', 'errors'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={cn(
                  'rounded-md px-3 py-1.5 text-xs font-medium transition-colors',
                  filter === f
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground'
                )}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="terminal-panel max-h-[350px] overflow-auto">
          <div className="space-y-1">
            {filteredLogs.map((log) => (
              <div
                key={log.id}
                className="flex items-start gap-3 py-1 animate-fade-in"
              >
                <span className="shrink-0 text-xs text-muted-foreground/70">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <span
                  className={cn(
                    'shrink-0 rounded px-1.5 py-0.5 text-xs font-medium uppercase',
                    levelBadges[log.level]
                  )}
                >
                  {log.level}
                </span>
                <span className="shrink-0 rounded bg-muted/30 px-1.5 py-0.5 text-xs text-muted-foreground">
                  {log.type}
                </span>
                <span className="text-sm text-foreground/80">{log.message}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Live indicator */}
        <div className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
          <span className="status-dot status-running animate-pulse" />
          Streaming live logs...
        </div>
      </div>
    </MainLayout>
  );
}
