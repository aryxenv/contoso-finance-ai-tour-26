import type { ReactNode } from 'react'
import { makeStyles, tokens } from '@fluentui/react-components'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

const useStyles = makeStyles({
  layout: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    backgroundColor: tokens.colorNeutralBackground1,
  },
  body: {
    display: 'flex',
    flex: '1',
  },
  content: {
    flex: '1',
    padding: '24px 32px',
  },
})

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  const styles = useStyles()
  return (
    <div className={styles.layout}>
      <Header />
      <div className={styles.body}>
        <Sidebar />
        <main className={styles.content}>{children}</main>
      </div>
    </div>
  )
}
