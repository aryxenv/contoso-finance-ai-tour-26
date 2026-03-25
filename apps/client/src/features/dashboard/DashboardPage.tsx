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

export function DashboardPage() {
  const styles = useStyles()
  return (
    <div className={styles.page}>
      <Title1>Dashboard</Title1>
      <Text className={styles.subtitle}>
        Financial overview and key metrics at a glance.
      </Text>
    </div>
  )
}
