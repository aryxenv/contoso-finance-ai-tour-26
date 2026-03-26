import type { CurrencyCode, Money } from './common';

export type SettlementStatus = 'pending' | 'reconciling' | 'approved' | 'completed' | 'rejected';

export interface SettlementItem {
  id: string;
  payment_id: string;
  amount: Money;
  fee: Money;
  net_amount: Money;
}

export interface Settlement {
  id: string;
  settlement_number: string;
  status: SettlementStatus;
  currency: CurrencyCode;
  items: SettlementItem[];
  total_amount: Money;
  total_fees: Money;
  net_amount: Money;
  settlement_date: string;
  created_at: string;
  updated_at: string;
}

export interface SettlementCreate {
  payment_ids: string[];
  currency: CurrencyCode;
  settlement_date: string;
}
