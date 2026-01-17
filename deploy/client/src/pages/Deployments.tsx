import { MainLayout } from '@/components/layout/MainLayout';
import { mockDeployments } from '@/lib/mock-data';
import { cn } from '@/lib/utils';
import { Check, Loader2, X, Upload, Hammer, Shield, Rocket } from 'lucide-react';

const stepIcons = {
  uploaded: Upload,
  building: Hammer,
  validated: Shield,
  running: Rocket,
  failed: X,
};

const stepLabels = ['Uploaded', 'Building', 'Validated', 'Running'];

export default function Deployments() {
  const getStepIndex = (status: string) => {
    const steps = ['uploaded', 'building', 'validated', 'running'];
    return steps.indexOf(status);
  };

  return (
    <MainLayout>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Deployments</h1>
        <p className="mt-1 text-muted-foreground">
          Track your agent deployments in real-time
        </p>
      </div>

      {/* CLI Reference */}
      <div className="mb-8 rounded-xl border border-border bg-card p-6">
        <p className="mb-3 text-sm text-muted-foreground">
          Deploy from your terminal:
        </p>
        <div className="terminal-panel inline-flex items-center gap-3">
          <span className="text-muted-foreground">$</span>
          <code className="text-primary">anymind deploy --api-key sk-****</code>
        </div>
      </div>

      {/* Deployments Timeline */}
      <div className="space-y-4">
        {mockDeployments.map((deployment) => {
          const currentStep = getStepIndex(deployment.status);
          const isFailed = deployment.status === 'failed';

          return (
            <div
              key={deployment.id}
              className="rounded-xl border border-border bg-card p-6"
            >
              {/* Header */}
              <div className="mb-6 flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-foreground">
                    {deployment.agentName}
                  </h3>
                  <p className="mt-0.5 font-mono text-xs text-muted-foreground">
                    {deployment.version}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-muted-foreground">
                    {new Date(deployment.timestamp).toLocaleString()}
                  </p>
                  {deployment.duration && (
                    <p className="mt-0.5 text-xs text-muted-foreground">
                      Duration: {deployment.duration}
                    </p>
                  )}
                </div>
              </div>

              {/* Steps Timeline */}
              <div className="relative flex items-center justify-between">
                {/* Progress Line Background */}
                <div className="absolute left-0 top-1/2 h-0.5 w-full -translate-y-1/2 bg-border" />
                
                {/* Progress Line Active */}
                <div
                  className={cn(
                    'absolute left-0 top-1/2 h-0.5 -translate-y-1/2 transition-all duration-500',
                    isFailed ? 'bg-status-failed' : 'bg-primary'
                  )}
                  style={{
                    width: isFailed
                      ? `${(currentStep / 3) * 100}%`
                      : `${(currentStep / 3) * 100}%`,
                  }}
                />

                {stepLabels.map((label, index) => {
                  const isCompleted = index < currentStep;
                  const isCurrent = index === currentStep;
                  const isFailedStep = isFailed && isCurrent;
                  const Icon = isFailedStep ? X : stepIcons[label.toLowerCase() as keyof typeof stepIcons];

                  return (
                    <div
                      key={label}
                      className="relative z-10 flex flex-col items-center"
                    >
                      <div
                        className={cn(
                          'flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all duration-300',
                          isCompleted
                            ? 'border-primary bg-primary text-primary-foreground'
                            : isCurrent && !isFailedStep
                            ? 'border-primary bg-background text-primary animate-pulse'
                            : isFailedStep
                            ? 'border-status-failed bg-status-failed/20 text-status-failed'
                            : 'border-border bg-background text-muted-foreground'
                        )}
                      >
                        {isCompleted ? (
                          <Check className="h-5 w-5" />
                        ) : isCurrent && !isFailedStep && deployment.status === 'building' ? (
                          <Loader2 className="h-5 w-5 animate-spin" />
                        ) : (
                          <Icon className="h-5 w-5" />
                        )}
                      </div>
                      <span
                        className={cn(
                          'mt-2 text-xs font-medium',
                          isCompleted || isCurrent
                            ? isFailedStep
                              ? 'text-status-failed'
                              : 'text-foreground'
                            : 'text-muted-foreground'
                        )}
                      >
                        {label}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </MainLayout>
  );
}
