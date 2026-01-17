import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';

const navItems = [
  { label: 'Agents', href: '/' },
  { label: 'Deployments', href: '/deployments' },
  { label: 'Logs', href: '/logs' },
  { label: 'API Keys', href: '/api-keys' },
];

export function TopNav() {
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <span className="text-sm font-bold text-primary-foreground">A</span>
          </div>
          <span className="text-lg font-semibold tracking-tight">Anymind</span>
        </Link>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.href}
                to={item.href}
                className={cn(
                  'px-4 py-2 text-sm font-medium transition-colors rounded-md',
                  isActive
                    ? 'text-primary bg-primary/10'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </div>

        {/* Right Side: Usage + Account */}
        <div className="flex items-center gap-4">
          {/* Usage Indicator */}
          <div className="flex items-center gap-2 rounded-full bg-secondary px-3 py-1.5">
            <div className="h-2 w-2 rounded-full bg-status-running" />
            <span className="text-xs font-medium text-muted-foreground">
              12.4k / 50k calls
            </span>
          </div>

          {/* Account */}
          <button className="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-sm font-medium text-muted-foreground transition-colors hover:bg-muted/80 hover:text-foreground">
            U
          </button>
        </div>
      </div>
    </nav>
  );
}
