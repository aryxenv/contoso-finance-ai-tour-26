import { apiClient } from './client'
import type {
  PaginatedResponse,
  Payment,
  PaymentCreate,
  PaymentMethod,
  PaymentStatusResponse,
  RefundRequest,
} from '@contoso-finance/shared-types'

export async function listPayments(
  page = 1,
  pageSize = 20
): Promise<PaginatedResponse<Payment>> {
  return apiClient<PaginatedResponse<Payment>>(
    `/api/payments/?page=${page}&page_size=${pageSize}`
  )
}

export async function getPayment(id: string): Promise<Payment> {
  return apiClient<Payment>(`/api/payments/${id}`)
}

export async function createPayment(data: PaymentCreate): Promise<Payment> {
  return apiClient<Payment>('/api/payments/', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function processPayment(id: string): Promise<Payment> {
  return apiClient<Payment>(`/api/payments/${id}/process`, {
    method: 'POST',
  })
}

export async function getPaymentStatus(id: string): Promise<PaymentStatusResponse> {
  return apiClient<PaymentStatusResponse>(`/api/payments/${id}/status`)
}

export async function refundPayment(id: string, data: RefundRequest): Promise<Payment> {
  return apiClient<Payment>(`/api/payments/${id}/refund`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function listPaymentMethods(): Promise<PaymentMethod[]> {
  return apiClient<PaymentMethod[]>('/api/payments/methods')
}
