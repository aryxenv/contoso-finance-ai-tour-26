import type { CurrencyCode, Money } from './common';

export type ReportType = 'cash_flow' | 'revenue' | 'expenses' | 'settlements';
export type ReportPeriod = 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly';

export interface MetricDataPoint {
  label: string;
  value: number;
}

export interface DashboardMetrics {
  total_revenue: Money;
  total_expenses: Money;
  net_income: Money;
  pending_invoices: number;
  pending_payments: number;
  currency: CurrencyCode;
  period: ReportPeriod;
}

export interface ReportRequest {
  type: ReportType;
  period: ReportPeriod;
  currency: CurrencyCode;
  start_date: string;
  end_date: string;
}

export interface Report {
  id: string;
  type: ReportType;
  period: ReportPeriod;
  currency: CurrencyCode;
  data_points: MetricDataPoint[];
  generated_at: string;
}
