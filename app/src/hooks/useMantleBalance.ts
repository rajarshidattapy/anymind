import { useState, useEffect } from 'react';
import { useWallet } from '../contexts/WalletContextProvider';

interface MantleBalanceData {
  balance: string;
  loading: boolean;
  error: string | null;
}

export const useMantleBalance = (): MantleBalanceData => {
  const [balance, setBalance] = useState<string>('0');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { connected, address, provider } = useWallet();

  useEffect(() => {
    const fetchBalance = async () => {
      if (!connected || !address || !provider) {
        setBalance('0');
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const balanceWei = await provider.getBalance(address);
        const balanceEth = (Number(balanceWei) / 1e18).toFixed(4);
        setBalance(balanceEth);
      } catch (err) {
        console.error('Error fetching Mantle balance:', err);
        setError('Failed to fetch balance');
        setBalance('0');
      } finally {
        setLoading(false);
      }
    };

    fetchBalance();
  }, [connected, address, provider]);

  return { balance, loading, error };
};
