import { useState, useEffect, useRef } from 'react';
import { generateMockLogs, LogEntry } from '@/lib/mock-data';
import { cn } from '@/lib/utils';

interface AgentLogsProps {
  agentId: string;
}

type FilterType = 'all' | 'build' | 'runtime' | 'errors';

export function AgentLogs({ agentId }: AgentLogsProps) {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [filter, setFilter] = useState<FilterType>('all');
  const logsEndRef = useRef<HTMLDivElement>(null);

  // Initial logs
  useEffect(() => {
    setLogs(generateMockLogs(15).filter(log => log.agentId === agentId || Math.random() > 0.5));
  }, [agentId]);

  // Real-time streaming simulation
  useEffect(() => {
    const interval = setInterval(() => {
      const newLog = generateMockLogs(1)[0];
      newLog.agentId = agentId;
      newLog.timestamp = new Date().toISOString();
      newLog.id = `log_${Date.now()}`;
      
      setLogs((prev) => [newLog, ...prev.slice(0, 49)]);
    }, 3000);

    return () => clearInterval(interval);
  }, [agentId]);

  const filteredLogs = logs.filter((log) => {
    if (filter === 'all') return true;
    if (filter === 'errors') return log.level === 'error' || log.level === 'warn';
    return log.type === filter;
  });

  const filters: { id: FilterType; label: string }[] = [
    { id: 'all', label: 'All' },
    { id: 'build', label: 'Build' },
    { id: 'runtime', label: 'Runtime' },
    { id: 'errors', label: 'Errors' },
  ];

  const levelColors = {
    info: 'text-muted-foreground',
    warn: 'text-status-building',
    error: 'text-status-failed',
    debug: 'text-accent',
  };

  const levelBadges = {
    info: 'bg-muted/50 text-muted-foreground',
    warn: 'bg-status-building/20 text-status-building',
    error: 'bg-status-failed/20 text-status-failed',
    debug: 'bg-accent/20 text-accent',
  };

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex gap-2">
        {filters.map((f) => (
          <button
            key={f.id}
            onClick={() => setFilter(f.id)}
            className={cn(
              'rounded-md px-3 py-1.5 text-xs font-medium transition-colors',
              filter === f.id
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground'
            )}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Logs Container */}
      <div className="terminal-panel max-h-[400px] overflow-auto">
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
              <span className={cn('text-sm', levelColors[log.level])}>
                {log.message}
              </span>
            </div>
          ))}
          <div ref={logsEndRef} />
        </div>
      </div>

      {/* Live indicator */}
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        <span className="status-dot status-running animate-pulse" />
        Streaming live logs...
      </div>
    </div>
  );
}
