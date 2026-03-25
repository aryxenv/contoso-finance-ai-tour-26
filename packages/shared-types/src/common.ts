/** Generic status for domain entities. */
export type Status = 'draft' | 'pending' | 'active' | 'completed' | 'cancelled';

/** Supported currency codes. */
export type CurrencyCode = 'USD' | 'EUR' | 'GBP';

/** Sort direction. */
export type SortOrder = 'asc' | 'desc';

/** Standard paginated response envelope. */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/** Monetary amount with currency. */
export interface Money {
  amount: number;
  currency: CurrencyCode;
}
