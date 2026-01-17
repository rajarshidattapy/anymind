import { Terminal } from 'lucide-react';

export function EmptyAgents() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center rounded-2xl border border-border bg-gradient-to-b from-card to-background p-12">
      {/* Abstract Nodes Illustration */}
      <div className="relative mb-8">
        <div className="absolute -left-8 -top-4 h-3 w-3 rounded-full bg-primary/30 animate-pulse" />
        <div className="absolute -right-6 top-2 h-2 w-2 rounded-full bg-accent/40 animate-pulse delay-300" />
        <div className="absolute -bottom-2 left-4 h-2.5 w-2.5 rounded-full bg-primary/20 animate-pulse delay-500" />
        
        <div className="flex h-20 w-20 items-center justify-center rounded-2xl border border-border bg-muted/50">
          <Terminal className="h-10 w-10 text-muted-foreground" />
        </div>
        
        {/* Connection lines */}
        <svg className="absolute inset-0 -z-10 h-32 w-32 -translate-x-6 -translate-y-6" viewBox="0 0 100 100">
          <line x1="20" y1="30" x2="45" y2="50" stroke="hsl(var(--border))" strokeWidth="1" />
          <line x1="80" y1="35" x2="55" y2="50" stroke="hsl(var(--border))" strokeWidth="1" />
          <line x1="35" y1="85" x2="50" y2="60" stroke="hsl(var(--border))" strokeWidth="1" />
        </svg>
      </div>

      {/* Text */}
      <h2 className="mb-2 text-xl font-semibold text-foreground">
        No agents deployed yet
      </h2>
      <p className="mb-6 text-center text-muted-foreground">
        Deploy your first agent from the CLI.
      </p>

      {/* CLI Command */}
      <div className="terminal-panel flex items-center gap-3">
        <span className="text-muted-foreground">$</span>
        <code className="text-primary">anymind deploy</code>
      </div>
    </div>
  );
}
