import { useState } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { mockApiKeys, ApiKey } from '@/lib/mock-data';
import { cn } from '@/lib/utils';
import { Plus, Copy, Trash2, AlertTriangle, Eye, EyeOff } from 'lucide-react';
import { toast } from 'sonner';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function ApiKeys() {
  const [keys, setKeys] = useState<ApiKey[]>(mockApiKeys);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [newKeyScope, setNewKeyScope] = useState('full-access');
  const [createdKey, setCreatedKey] = useState<string | null>(null);
  const [showKey, setShowKey] = useState(false);

  const handleCreateKey = () => {
    if (!newKeyName) return;

    const newKey: ApiKey = {
      id: `key_${Date.now()}`,
      name: newKeyName,
      scope: newKeyScope,
      lastUsed: 'Never',
      createdAt: new Date().toISOString(),
      prefix: `sk-${newKeyName.toLowerCase().slice(0, 4)}-****`,
    };

    // Simulate a full key for display
    const fullKey = `sk-${newKeyName.toLowerCase().slice(0, 4)}-${Math.random().toString(36).slice(2, 14)}${Math.random().toString(36).slice(2, 14)}`;
    
    setKeys((prev) => [...prev, newKey]);
    setCreatedKey(fullKey);
    setNewKeyName('');
  };

  const handleCopyKey = (key: string) => {
    navigator.clipboard.writeText(key);
    toast.success('API key copied to clipboard');
  };

  const handleDeleteKey = (id: string) => {
    setKeys((prev) => prev.filter((key) => key.id !== id));
    toast.success('API key deleted');
  };

  const handleCloseDialog = () => {
    setIsCreateOpen(false);
    setCreatedKey(null);
    setShowKey(false);
    setNewKeyName('');
    setNewKeyScope('full-access');
  };

  return (
    <MainLayout>
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">API Keys</h1>
          <p className="mt-1 text-muted-foreground">
            Manage your API keys for authentication
          </p>
        </div>
        <button
          onClick={() => setIsCreateOpen(true)}
          className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
        >
          <Plus className="h-4 w-4" />
          Create new key
        </button>
      </div>

      {/* Warning */}
      <div className="mb-6 flex items-start gap-3 rounded-lg border border-status-building/30 bg-status-building/10 p-4">
        <AlertTriangle className="h-5 w-5 shrink-0 text-status-building" />
        <p className="text-sm text-muted-foreground">
          API keys are only shown once when created. Store them securely — you won't be able to view them again.
        </p>
      </div>

      {/* Keys List */}
      <div className="rounded-xl border border-border bg-card">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              <th className="px-6 py-4 text-left text-xs font-medium uppercase text-muted-foreground">
                Name
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium uppercase text-muted-foreground">
                Key
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium uppercase text-muted-foreground">
                Scope
              </th>
              <th className="px-6 py-4 text-left text-xs font-medium uppercase text-muted-foreground">
                Last Used
              </th>
              <th className="px-6 py-4 text-right text-xs font-medium uppercase text-muted-foreground">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {keys.map((key) => (
              <tr
                key={key.id}
                className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors"
              >
                <td className="px-6 py-4 font-medium">{key.name}</td>
                <td className="px-6 py-4">
                  <code className="font-mono text-sm text-muted-foreground">
                    {key.prefix}
                  </code>
                </td>
                <td className="px-6 py-4">
                  <span className="rounded-full bg-muted px-2.5 py-1 text-xs font-medium text-muted-foreground">
                    {key.scope}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-muted-foreground">
                  {key.lastUsed === 'Never'
                    ? 'Never'
                    : new Date(key.lastUsed).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 text-right">
                  <button
                    onClick={() => handleDeleteKey(key.id)}
                    className="rounded-md p-2 text-muted-foreground hover:bg-destructive/10 hover:text-destructive transition-colors"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create Key Dialog */}
      <Dialog open={isCreateOpen} onOpenChange={handleCloseDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>
              {createdKey ? 'API Key Created' : 'Create new API key'}
            </DialogTitle>
            <DialogDescription>
              {createdKey
                ? 'Copy your key now. You won\'t be able to see it again.'
                : 'Give your key a name and select the access scope.'}
            </DialogDescription>
          </DialogHeader>

          {createdKey ? (
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <div className="relative flex-1">
                  <Input
                    value={showKey ? createdKey : '•'.repeat(40)}
                    readOnly
                    className="pr-10 font-mono text-sm"
                  />
                  <button
                    onClick={() => setShowKey(!showKey)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => handleCopyKey(createdKey)}
                >
                  <Copy className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex items-start gap-2 rounded-lg bg-status-building/10 p-3">
                <AlertTriangle className="h-4 w-4 shrink-0 text-status-building mt-0.5" />
                <p className="text-xs text-muted-foreground">
                  This key will only be shown once. Please copy it now and store it securely.
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-foreground">Name</label>
                <Input
                  value={newKeyName}
                  onChange={(e) => setNewKeyName(e.target.value)}
                  placeholder="e.g., Production"
                  className="mt-1.5"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-foreground">Scope</label>
                <select
                  value={newKeyScope}
                  onChange={(e) => setNewKeyScope(e.target.value)}
                  className="mt-1.5 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                >
                  <option value="full-access">Full Access</option>
                  <option value="read-only">Read Only</option>
                  <option value="deploy-only">Deploy Only</option>
                </select>
              </div>
            </div>
          )}

          <DialogFooter>
            {createdKey ? (
              <Button onClick={handleCloseDialog}>Done</Button>
            ) : (
              <>
                <Button variant="outline" onClick={handleCloseDialog}>
                  Cancel
                </Button>
                <Button onClick={handleCreateKey} disabled={!newKeyName}>
                  Create key
                </Button>
              </>
            )}
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </MainLayout>
  );
}
