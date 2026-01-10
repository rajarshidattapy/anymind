import { Link } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { Agent } from '@/lib/mock-data';
import { Copy } from 'lucide-react';
import { toast } from 'sonner';

interface AgentCardProps {
  agent: Agent;
}

export function AgentCard({ agent }: AgentCardProps) {
  const statusClasses = {
    running: 'status-running',
    building: 'status-building',
    failed: 'status-failed',
  };

  const statusLabels = {
    running: 'Running',
    building: 'Building',
    failed: 'Failed',
  };

  const copyId = (e: React.MouseEvent) => {
    e.preventDefault();
    navigator.clipboard.writeText(agent.id);
    toast.success('Agent ID copied to clipboard');
  };

  return (
    <Link
      to={`/agents/${agent.id}`}
      className={cn(
        'group block rounded-xl border border-border bg-card p-5 transition-all duration-200',
        'hover:border-primary/50 hover:shadow-lg',
        agent.status === 'running' && 'hover:glow-primary'
      )}
    >
      {/* Header */}
      <div className="mb-4 flex items-start justify-between">
        <div className="flex items-center gap-2">
          <span className={cn('status-dot', statusClasses[agent.status])} />
          <span className="text-xs font-medium text-muted-foreground">
            {statusLabels[agent.status]}
          </span>
        </div>
        <span
          className={cn(
            'rounded-full px-2 py-0.5 text-xs font-medium',
            agent.visibility === 'public'
              ? 'bg-accent/20 text-accent'
              : 'bg-muted text-muted-foreground'
          )}
        >
          {agent.visibility}
        </span>
      </div>

      {/* Agent Name */}
      <h3 className="mb-1 text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
        {agent.name}
      </h3>

      {/* Agent ID */}
      <button
        onClick={copyId}
        className="mb-3 flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
      >
        <code className="font-mono">{agent.id}</code>
        <Copy className="h-3 w-3" />
      </button>

      {/* Details */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="rounded bg-secondary px-2 py-0.5 text-xs font-medium text-secondary-foreground">
            {agent.framework}
          </span>
        </div>
        <span className="font-mono text-xs text-muted-foreground">
          {agent.version}
        </span>
      </div>
    </Link>
  );
}
