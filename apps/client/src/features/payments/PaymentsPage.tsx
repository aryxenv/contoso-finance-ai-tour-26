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

export function PaymentsPage() {
  const styles = useStyles()
  return (
    <div className={styles.page}>
      <Title1>Payments</Title1>
      <Text className={styles.subtitle}>
        Track and process incoming and outgoing payments.
      </Text>
    </div>
  )
}
