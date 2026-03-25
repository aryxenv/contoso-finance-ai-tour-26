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

export function ReportingPage() {
  const styles = useStyles()
  return (
    <div className={styles.page}>
      <Title1>Reporting</Title1>
      <Text className={styles.subtitle}>
        Generate and view financial reports and analytics.
      </Text>
    </div>
  )
}
