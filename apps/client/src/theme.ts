import { createDarkTheme } from '@fluentui/react-components'
import type { BrandVariants, Theme } from '@fluentui/react-components'

const brandVariants: BrandVariants = {
  10: '#020508',
  20: '#0a1a2e',
  30: '#0d2847',
  40: '#0e345e',
  50: '#0f4076',
  60: '#104d8e',
  70: '#1059a5',
  80: '#58a6ff',
  90: '#6db4ff',
  100: '#80c0ff',
  110: '#93ccff',
  120: '#a6d7ff',
  130: '#b9e1ff',
  140: '#ccebff',
  150: '#dff3ff',
  160: '#f2faff',
}

const darkTheme = createDarkTheme(brandVariants)

export const contosoTheme: Theme = {
  ...darkTheme,
  colorNeutralBackground1: '#0d1117',
  colorNeutralBackground2: '#161b22',
  colorNeutralBackground3: '#21262d',
  colorNeutralStroke1: '#30363d',
  colorNeutralForeground1: '#e6edf3',
  colorNeutralForeground2: '#8b949e',
  colorBrandForegroundLink: '#58a6ff',
}
