import { Routes, Route } from 'react-router-dom'
import { DashboardPage } from './features/dashboard/DashboardPage'
import { BillingPage } from './features/billing/BillingPage'
import { PaymentsPage } from './features/payments/PaymentsPage'
import { ReportingPage } from './features/reporting/ReportingPage'
import { SettlementsPage } from './features/settlements/SettlementsPage'

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/billing" element={<BillingPage />} />
      <Route path="/payments" element={<PaymentsPage />} />
      <Route path="/reporting" element={<ReportingPage />} />
      <Route path="/settlements" element={<SettlementsPage />} />
    </Routes>
  )
}
