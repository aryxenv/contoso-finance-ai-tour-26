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

export function SettlementsPage() {
  const styles = useStyles()
  return (
    <div className={styles.page}>
      <Title1>Settlements</Title1>
      <Text className={styles.subtitle}>
        Review and reconcile financial settlements.
      </Text>
    </div>
  )
}
