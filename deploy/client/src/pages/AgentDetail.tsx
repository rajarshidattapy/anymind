import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { mockAgents, mockAgentVersions } from '@/lib/mock-data';
import { cn } from '@/lib/utils';
import { Copy, ArrowLeft, Info, Play, RotateCcw } from 'lucide-react';
import { toast } from 'sonner';
import { AgentLogs } from '@/components/agents/AgentLogs';

type TabType = 'overview' | 'runtime' | 'logs' | 'versions';

export default function AgentDetail() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [testInput, setTestInput] = useState('');
  const [testOutput, setTestOutput] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const agent = mockAgents.find((a) => a.id === id);
  const versions = mockAgentVersions(id || '');

  if (!agent) {
    return (
      <MainLayout>
        <div className="flex min-h-[60vh] items-center justify-center">
          <p className="text-muted-foreground">Agent not found</p>
        </div>
      </MainLayout>
    );
  }

  const statusClasses = {
    running: 'bg-status-running/20 text-status-running',
    building: 'bg-status-building/20 text-status-building',
    failed: 'bg-status-failed/20 text-status-failed',
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`${label} copied to clipboard`);
  };

  const handleRunTest = async () => {
    setIsRunning(true);
    setTestOutput(null);
    
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));
    
    setTestOutput(JSON.stringify({
      success: true,
      response: {
        message: "Agent processed your request successfully",
        data: { input: testInput, processed_at: new Date().toISOString() }
      },
      latency_ms: 127
    }, null, 2));
    setIsRunning(false);
  };

  const tabs: { id: TabType; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'runtime', label: 'Runtime' },
    { id: 'logs', label: 'Logs' },
    { id: 'versions', label: 'Versions' },
  ];

  return (
    <MainLayout>
      {/* Back Link */}
      <Link
        to="/"
        className="mb-6 inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Agents
      </Link>

      {/* Header */}
      <div className="mb-8 flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-foreground">{agent.name}</h1>
            <span className={cn('rounded-full px-2.5 py-1 text-xs font-medium', statusClasses[agent.status])}>
              {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
            </span>
          </div>
          <button
            onClick={() => copyToClipboard(agent.id, 'Agent ID')}
            className="mt-2 flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <code className="font-mono">{agent.id}</code>
            <Copy className="h-3.5 w-3.5" />
          </button>
        </div>
        
        <div className="flex items-center gap-2 text-muted-foreground">
          <Info className="h-4 w-4" />
          <span className="text-xs">Runtime: Node.js 20.x</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-6 flex gap-1 border-b border-border">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={cn(
              'px-4 py-3 text-sm font-medium transition-colors border-b-2 -mb-px',
              activeTab === tab.id
                ? 'border-primary text-primary'
                : 'border-transparent text-muted-foreground hover:text-foreground'
            )}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="rounded-xl border border-border bg-card p-6">
        {activeTab === 'overview' && (
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium text-muted-foreground">Current Version</label>
                <p className="mt-1 font-mono text-sm">{agent.version}</p>
              </div>
              <div>
                <label className="text-xs font-medium text-muted-foreground">Entrypoint</label>
                <p className="mt-1 font-mono text-sm">{agent.entrypoint}</p>
              </div>
              <div>
                <label className="text-xs font-medium text-muted-foreground">Framework</label>
                <p className="mt-1 text-sm">{agent.framework}</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium text-muted-foreground">CPU</label>
                <p className="mt-1 text-sm">{agent.cpu}</p>
              </div>
              <div>
                <label className="text-xs font-medium text-muted-foreground">Memory</label>
                <p className="mt-1 text-sm">{agent.memory}</p>
              </div>
              <div>
                <label className="text-xs font-medium text-muted-foreground">Deployed At</label>
                <p className="mt-1 text-sm">
                  {new Date(agent.deployedAt).toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'runtime' && (
          <div className="space-y-6">
            {/* Endpoint */}
            <div>
              <label className="text-xs font-medium text-muted-foreground">Live Endpoint</label>
              <div className="mt-2 flex items-center gap-2">
                <code className="flex-1 rounded-lg bg-background px-4 py-2.5 font-mono text-sm">
                  {agent.endpoint}
                </code>
                <button
                  onClick={() => copyToClipboard(agent.endpoint, 'Endpoint')}
                  className="rounded-lg bg-muted p-2.5 text-muted-foreground hover:bg-muted/80 hover:text-foreground transition-colors"
                >
                  <Copy className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Test Input */}
            <div>
              <label className="text-xs font-medium text-muted-foreground">Test Input</label>
              <textarea
                value={testInput}
                onChange={(e) => setTestInput(e.target.value)}
                placeholder='{"prompt": "Hello, agent!"}'
                className="mt-2 w-full rounded-lg border border-border bg-background px-4 py-3 font-mono text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                rows={4}
              />
            </div>

            {/* Run Button */}
            <button
              onClick={handleRunTest}
              disabled={isRunning || !testInput}
              className={cn(
                'inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-colors',
                isRunning || !testInput
                  ? 'opacity-50 cursor-not-allowed'
                  : 'hover:bg-primary/90'
              )}
            >
              <Play className="h-4 w-4" />
              {isRunning ? 'Running...' : 'Run'}
            </button>

            {/* Response */}
            {testOutput && (
              <div>
                <label className="text-xs font-medium text-muted-foreground">Response</label>
                <pre className="mt-2 terminal-panel overflow-auto max-h-64">
                  <code className="text-accent">{testOutput}</code>
                </pre>
              </div>
            )}
          </div>
        )}

        {activeTab === 'logs' && (
          <AgentLogs agentId={agent.id} />
        )}

        {activeTab === 'versions' && (
          <div className="space-y-3">
            {versions.map((version, index) => (
              <div
                key={version.hash}
                className="flex items-center justify-between rounded-lg border border-border bg-background p-4"
              >
                <div className="flex items-center gap-4">
                  <code className="font-mono text-sm text-muted-foreground">
                    {version.hash}
                  </code>
                  <span className="font-medium">{version.version}</span>
                  <span
                    className={cn(
                      'rounded-full px-2 py-0.5 text-xs font-medium',
                      version.status === 'live'
                        ? 'bg-status-running/20 text-status-running'
                        : version.status === 'stable'
                        ? 'bg-muted text-muted-foreground'
                        : 'bg-muted/50 text-muted-foreground/70'
                    )}
                  >
                    {version.status}
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-xs text-muted-foreground">
                    {new Date(version.deployedAt).toLocaleDateString()}
                  </span>
                  <button
                    disabled={index === 0}
                    className={cn(
                      'inline-flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors',
                      index === 0
                        ? 'bg-muted/50 text-muted-foreground/50 cursor-not-allowed'
                        : 'bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground'
                    )}
                  >
                    <RotateCcw className="h-3 w-3" />
                    Rollback
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
}
