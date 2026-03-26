import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { CurrencyCode, Payment, PaymentMethod, PaymentStatus, PaymentStatusResponse } from '@contoso-finance/shared-types'
import {
  Badge,
  Button,
  Card,
  DataGrid,
  DataGridBody,
  DataGridCell,
  DataGridHeader,
  DataGridHeaderCell,
  DataGridRow,
  Dialog,
  DialogActions,
  DialogBody,
  DialogContent,
  DialogSurface,
  DialogTitle,
  DialogTrigger,
  Dropdown,
  Field,
  Input,
  Option,
  Spinner,
  Text,
  Title1,
  createTableColumn,
  makeStyles,
  tokens,
} from '@fluentui/react-components'
import type { TableColumnDefinition } from '@fluentui/react-components'
import { AddRegular, ArrowSyncRegular, PlayRegular } from '@fluentui/react-icons'
import { createPayment, getPaymentStatus, listPaymentMethods, listPayments, processPayment } from '../../api/payments'

const useStyles = makeStyles({
  page: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  subtitle: {
    color: tokens.colorNeutralForeground2,
  },
  headerCard: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '16px',
    backgroundColor: tokens.colorNeutralBackground2,
  },
  titleBlock: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  actions: {
    display: 'flex',
    gap: '8px',
  },
  tableCard: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    paddingTop: '12px',
    paddingBottom: '12px',
  },
  grid: {
    minWidth: '100%',
  },
  amountCell: {
    fontVariantNumeric: 'tabular-nums',
  },
  dialogBody: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  inlineError: {
    color: tokens.colorPaletteRedForeground1,
  },
  emptyState: {
    color: tokens.colorNeutralForeground3,
    padding: '16px',
  },
})

const TERMINAL_STATUSES: PaymentStatus[] = ['completed', 'failed', 'refunded']

const CURRENCIES: CurrencyCode[] = ['USD', 'EUR', 'GBP']

function getBadgeAppearance(status: PaymentStatus): {
  color: 'warning' | 'brand' | 'success' | 'danger' | 'subtle'
  label: string
} {
  switch (status) {
    case 'pending':
      return { color: 'warning', label: 'Pending' }
    case 'processing':
      return { color: 'brand', label: 'Processing' }
    case 'completed':
      return { color: 'success', label: 'Completed' }
    case 'failed':
      return { color: 'danger', label: 'Failed' }
    case 'refunded':
      return { color: 'subtle', label: 'Refunded' }
    default:
      return { color: 'subtle', label: status }
  }
}

function formatPaymentMethod(method: PaymentMethod): string {
  const methodTypeLabel = method.type.replace('_', ' ')
  return `${methodTypeLabel} •••• ${method.last_four}`
}

export function PaymentsPage() {
  const styles = useStyles()
  const [payments, setPayments] = useState<Payment[]>([])
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([])
  const [loading, setLoading] = useState(true)
  const [loadingMethods, setLoadingMethods] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [processingId, setProcessingId] = useState<string | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [amount, setAmount] = useState('')
  const [currency, setCurrency] = useState<CurrencyCode>('USD')
  const [paymentMethodId, setPaymentMethodId] = useState<string>('')
  const pollingIntervalRef = useRef<number | null>(null)
  const pollingBusyRef = useRef(false)

  const stopPolling = useCallback(() => {
    if (pollingIntervalRef.current !== null) {
      window.clearInterval(pollingIntervalRef.current)
      pollingIntervalRef.current = null
    }
  }, [])

  const fetchPayments = useCallback(async (showSpinner: boolean) => {
    if (showSpinner) {
      setLoading(true)
    }
    setError(null)
    try {
      const response = await listPayments()
      setPayments(response.items)
    } catch {
      setError('Failed to load payments. Please try again.')
    } finally {
      if (showSpinner) {
        setLoading(false)
      }
    }
  }, [])

  const fetchPaymentMethods = useCallback(async () => {
    setLoadingMethods(true)
    try {
      const methods = await listPaymentMethods()
      setPaymentMethods(methods)
      if (methods.length > 0) {
        setPaymentMethodId(methods[0].id)
      }
    } catch {
      setError('Failed to load payment methods. Please refresh and try again.')
    } finally {
      setLoadingMethods(false)
    }
  }, [])

  useEffect(() => {
    void Promise.all([fetchPayments(true), fetchPaymentMethods()])
  }, [fetchPaymentMethods, fetchPayments])

  const pollStatuses = useCallback(
    async (processingPaymentIds: string[]) => {
      if (pollingBusyRef.current) {
        return
      }

      pollingBusyRef.current = true
      try {
        const statusResponses = await Promise.all(
          processingPaymentIds.map(async (id) => {
            try {
              return await getPaymentStatus(id)
            } catch {
              return null
            }
          })
        )
        const hasTerminalUpdate = statusResponses.some((response: PaymentStatusResponse | null) => {
          if (!response) {
            return false
          }
          return TERMINAL_STATUSES.includes(response.status)
        })

        if (hasTerminalUpdate) {
          await fetchPayments(false)
        }
      } finally {
        pollingBusyRef.current = false
      }
    },
    [fetchPayments]
  )

  useEffect(() => {
    stopPolling()

    const processingPaymentIds = payments
      .filter((payment) => payment.status === 'processing')
      .map((payment) => payment.id)

    if (processingPaymentIds.length === 0) {
      return
    }

    pollingIntervalRef.current = window.setInterval(() => {
      void pollStatuses(processingPaymentIds)
    }, 2000)

    return stopPolling
  }, [payments, pollStatuses, stopPolling])

  useEffect(() => stopPolling, [stopPolling])

  const resetForm = useCallback(() => {
    setAmount('')
    setCurrency('USD')
    setPaymentMethodId(paymentMethods[0]?.id ?? '')
    setFormError(null)
  }, [paymentMethods])

  const handleCreatePayment = useCallback(async () => {
    setFormError(null)
    const parsedAmount = Number(amount)
    if (!Number.isFinite(parsedAmount) || parsedAmount <= 0) {
      setFormError('Amount must be greater than zero.')
      return
    }
    if (!paymentMethodId) {
      setFormError('Please select a payment method.')
      return
    }

    setSubmitting(true)
    try {
      await createPayment({
        amount: parsedAmount,
        currency,
        payment_method_id: paymentMethodId,
      })
      setDialogOpen(false)
      resetForm()
      await fetchPayments(false)
    } catch {
      setFormError('Unable to create payment. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }, [amount, currency, fetchPayments, paymentMethodId, resetForm])

  const handleProcessPayment = useCallback(
    async (id: string) => {
      setError(null)
      setProcessingId(id)
      try {
        await processPayment(id)
        await fetchPayments(false)
      } catch {
        setError('Unable to process payment. Please try again.')
      } finally {
        setProcessingId(null)
      }
    },
    [fetchPayments]
  )

  const selectedPaymentMethodLabel = useMemo(() => {
    const selectedMethod = paymentMethods.find((method) => method.id === paymentMethodId)
    return selectedMethod ? formatPaymentMethod(selectedMethod) : ''
  }, [paymentMethodId, paymentMethods])

  const columns: TableColumnDefinition<Payment>[] = useMemo(
    () => [
      createTableColumn<Payment>({
        columnId: 'reference',
        renderHeaderCell: () => 'Reference',
        renderCell: (item) => <Text>{item.reference}</Text>,
      }),
      createTableColumn<Payment>({
        columnId: 'amount',
        renderHeaderCell: () => 'Amount',
        renderCell: (item) => (
          <Text className={styles.amountCell}>
            {item.amount.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </Text>
        ),
      }),
      createTableColumn<Payment>({
        columnId: 'currency',
        renderHeaderCell: () => 'Currency',
        renderCell: (item) => <Text>{item.currency}</Text>,
      }),
      createTableColumn<Payment>({
        columnId: 'status',
        renderHeaderCell: () => 'Status',
        renderCell: (item) => {
          const badge = getBadgeAppearance(item.status)
          return (
            <Badge color={badge.color} appearance="filled">
              {badge.label}
            </Badge>
          )
        },
      }),
      createTableColumn<Payment>({
        columnId: 'date',
        renderHeaderCell: () => 'Date',
        renderCell: (item) => <Text>{new Date(item.created_at).toLocaleDateString()}</Text>,
      }),
      createTableColumn<Payment>({
        columnId: 'actions',
        renderHeaderCell: () => 'Actions',
        renderCell: (item) =>
          item.status === 'pending' ? (
            <Button
              size="small"
              appearance="secondary"
              icon={<PlayRegular />}
              disabled={processingId === item.id}
              onClick={() => {
                void handleProcessPayment(item.id)
              }}
            >
              {processingId === item.id ? 'Processing...' : 'Process'}
            </Button>
          ) : (
            <Text>—</Text>
          ),
      }),
    ],
    [handleProcessPayment, processingId, styles.amountCell]
  )

  return (
    <Card className={styles.page}>
      <Card className={styles.headerCard}>
        <Card className={styles.titleBlock}>
          <Title1>Payments</Title1>
          <Text className={styles.subtitle}>
            Track and process incoming and outgoing payments.
          </Text>
        </Card>
        <Card className={styles.actions}>
          <Button
            icon={<ArrowSyncRegular />}
            appearance="subtle"
            disabled={loading}
            onClick={() => {
              void fetchPayments(true)
            }}
          >
            Refresh
          </Button>
          <Dialog
            open={dialogOpen}
            onOpenChange={(_, data) => {
              setDialogOpen(data.open)
              if (!data.open) {
                resetForm()
              }
            }}
          >
            <DialogTrigger disableButtonEnhancement>
              <Button appearance="primary" icon={<AddRegular />} disabled={loadingMethods}>
                New Payment
              </Button>
            </DialogTrigger>
            <DialogSurface>
              <DialogBody>
                <DialogTitle>Create Payment</DialogTitle>
                <DialogContent className={styles.dialogBody}>
                  <Field label="Amount" validationMessage={formError ?? undefined}>
                    <Input
                      type="number"
                      value={amount}
                      onChange={(_, data) => {
                        setAmount(data.value)
                      }}
                    />
                  </Field>
                  <Field label="Currency">
                    <Dropdown
                      value={currency}
                      selectedOptions={[currency]}
                      onOptionSelect={(_, data) => {
                        if (data.optionValue) {
                          setCurrency(data.optionValue as CurrencyCode)
                        }
                      }}
                    >
                      {CURRENCIES.map((currencyCode) => (
                        <Option key={currencyCode} value={currencyCode}>
                          {currencyCode}
                        </Option>
                      ))}
                    </Dropdown>
                  </Field>
                  <Field label="Payment Method">
                    <Dropdown
                      value={selectedPaymentMethodLabel}
                      selectedOptions={paymentMethodId ? [paymentMethodId] : []}
                      onOptionSelect={(_, data) => {
                        if (data.optionValue) {
                          setPaymentMethodId(data.optionValue)
                        }
                      }}
                    >
                      {paymentMethods.map((method) => (
                        <Option key={method.id} value={method.id}>
                          {formatPaymentMethod(method)}
                        </Option>
                      ))}
                    </Dropdown>
                  </Field>
                  {formError ? <Text className={styles.inlineError}>{formError}</Text> : null}
                </DialogContent>
                <DialogActions>
                  <DialogTrigger disableButtonEnhancement>
                    <Button appearance="secondary">Cancel</Button>
                  </DialogTrigger>
                  <Button appearance="primary" onClick={() => void handleCreatePayment()} disabled={submitting}>
                    {submitting ? 'Creating...' : 'Create Payment'}
                  </Button>
                </DialogActions>
              </DialogBody>
            </DialogSurface>
          </Dialog>
        </Card>
      </Card>

      <Card className={styles.tableCard}>
        {error ? <Text className={styles.inlineError}>{error}</Text> : null}
        {loading ? (
          <Spinner label="Loading payments..." />
        ) : payments.length === 0 ? (
          <Text className={styles.emptyState}>No payments found.</Text>
        ) : (
          <DataGrid className={styles.grid} items={payments} columns={columns} getRowId={(item) => item.id}>
            <DataGridHeader>
              <DataGridRow>
                {({ renderHeaderCell }) => (
                  <DataGridHeaderCell>{renderHeaderCell()}</DataGridHeaderCell>
                )}
              </DataGridRow>
            </DataGridHeader>
            <DataGridBody<Payment>>
              {({ item, rowId }) => (
                <DataGridRow<Payment> key={rowId}>
                  {({ renderCell }) => <DataGridCell>{renderCell(item)}</DataGridCell>}
                </DataGridRow>
              )}
            </DataGridBody>
          </DataGrid>
        )}
      </Card>
    </Card>
  )
}
