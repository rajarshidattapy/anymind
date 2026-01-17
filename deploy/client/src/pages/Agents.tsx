import { MainLayout } from '@/components/layout/MainLayout';
import { AgentCard } from '@/components/agents/AgentCard';
import { EmptyAgents } from '@/components/agents/EmptyAgents';
import { mockAgents } from '@/lib/mock-data';

export default function Agents() {
  const hasAgents = mockAgents.length > 0;

  return (
    <MainLayout>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Agents</h1>
        <p className="mt-1 text-muted-foreground">
          Manage and monitor your deployed agents
        </p>
      </div>

      {/* Content */}
      {hasAgents ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {mockAgents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>
      ) : (
        <EmptyAgents />
      )}
    </MainLayout>
  );
}
