import type { CurrencyCode } from './common';

export type PaymentStatus = 'pending' | 'processing' | 'completed' | 'failed' | 'refunded';

export type PaymentMethodType = 'credit_card' | 'bank_transfer' | 'wire';

export interface PaymentMethod {
  id: string;
  type: PaymentMethodType;
  last_four: string;
  is_default: boolean;
}

export interface Payment {
  id: string;
  invoice_id: string | null;
  amount: number;
  currency: CurrencyCode;
  status: PaymentStatus;
  payment_method: PaymentMethod;
  reference: string;
  created_at: string;
  updated_at: string;
}

export interface PaymentCreate {
  invoice_id?: string;
  amount: number;
  currency: CurrencyCode;
  payment_method_id: string;
}

export interface RefundRequest {
  payment_id: string;
  amount?: number;
  reason: string;
}

export interface PaymentStatusResponse {
  id: string;
  status: PaymentStatus;
  reference: string;
  updated_at: string;
}
