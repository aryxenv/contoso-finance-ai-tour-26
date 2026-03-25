import { useLocation, useNavigate } from 'react-router-dom'
import { makeStyles, tokens, Text } from '@fluentui/react-components'
import {
  BoardRegular,
  ReceiptRegular,
  WalletRegular,
  ChartMultipleRegular,
  BuildingBankRegular,
} from '@fluentui/react-icons'

const navItems = [
  { to: '/', label: 'Dashboard', icon: <BoardRegular /> },
  { to: '/billing', label: 'Billing', icon: <ReceiptRegular /> },
  { to: '/payments', label: 'Payments', icon: <WalletRegular /> },
  { to: '/reporting', label: 'Reporting', icon: <ChartMultipleRegular /> },
  { to: '/settlements', label: 'Settlements', icon: <BuildingBankRegular /> },
]

const useStyles = makeStyles({
  sidebar: {
    width: '220px',
    backgroundColor: '#161b22',
    borderRight: `1px solid ${tokens.colorNeutralStroke1}`,
    paddingTop: '8px',
    paddingBottom: '8px',
  },
  navItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '8px 16px',
    cursor: 'pointer',
    color: tokens.colorNeutralForeground2,
    borderRadius: '6px',
    marginLeft: '8px',
    marginRight: '8px',
    marginBottom: '2px',
    textDecoration: 'none',
    border: 'none',
    backgroundColor: 'transparent',
    width: 'calc(100% - 16px)',
    textAlign: 'left' as const,
    ':hover': {
      backgroundColor: '#21262d',
      color: tokens.colorNeutralForeground1,
    },
  },
  navItemActive: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '8px 16px',
    cursor: 'pointer',
    color: '#ffffff',
    borderRadius: '6px',
    marginLeft: '8px',
    marginRight: '8px',
    marginBottom: '2px',
    textDecoration: 'none',
    border: 'none',
    backgroundColor: '#30363d',
    width: 'calc(100% - 16px)',
    textAlign: 'left' as const,
  },
})

export function Sidebar() {
  const styles = useStyles()
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <nav className={styles.sidebar}>
      {navItems.map((item) => {
        const isActive =
          item.to === '/'
            ? location.pathname === '/'
            : location.pathname.startsWith(item.to)
        return (
          <button
            key={item.to}
            className={isActive ? styles.navItemActive : styles.navItem}
            onClick={() => navigate(item.to)}
          >
            {item.icon}
            <Text size={300} weight={isActive ? 'semibold' : 'regular'}>
              {item.label}
            </Text>
          </button>
        )
      })}
    </nav>
  )
}
