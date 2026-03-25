import type { CurrencyCode, Money, Status } from './common';

export interface LineItem {
  id: string;
  description: string;
  quantity: number;
  unit_price: Money;
  total: Money;
}

export interface Invoice {
  id: string;
  invoice_number: string;
  customer_name: string;
  customer_email: string;
  status: Status;
  currency: CurrencyCode;
  line_items: LineItem[];
  subtotal: Money;
  tax: Money;
  total: Money;
  due_date: string;
  created_at: string;
  updated_at: string;
}

export interface InvoiceCreate {
  customer_name: string;
  customer_email: string;
  currency: CurrencyCode;
  line_items: Omit<LineItem, 'id' | 'total'>[];
  due_date: string;
}

export interface InvoiceUpdate {
  customer_name?: string;
  customer_email?: string;
  status?: Status;
  line_items?: Omit<LineItem, 'id' | 'total'>[];
  due_date?: string;
}
