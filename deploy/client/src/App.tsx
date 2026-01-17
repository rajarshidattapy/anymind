import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Agents from "./pages/Agents";
import AgentDetail from "./pages/AgentDetail";
import Deployments from "./pages/Deployments";
import ApiKeys from "./pages/ApiKeys";
import LogsUsage from "./pages/LogsUsage";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Agents />} />
          <Route path="/agents/:id" element={<AgentDetail />} />
          <Route path="/deployments" element={<Deployments />} />
          <Route path="/api-keys" element={<ApiKeys />} />
          <Route path="/logs" element={<LogsUsage />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
