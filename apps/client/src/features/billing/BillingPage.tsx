import { Title1, Text, makeStyles, tokens } from '@fluentui/react-components'

const useStyles = makeStyles({
  page: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  subtitle: {
    color: tokens.colorNeutralForeground2,
  },
})

export function BillingPage() {
  const styles = useStyles()
  return (
    <div className={styles.page}>
      <Title1>Billing</Title1>
      <Text className={styles.subtitle}>
        Manage invoices, billing cycles, and payment terms.
      </Text>
    </div>
  )
}
