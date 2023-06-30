import './globals.css'
import { Inter } from 'next/font/google'
import RecoilWrapper from './RecoilWrapper'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'V playlist',
  description: 'A playlist generator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
          <RecoilWrapper>
            {children}
          </RecoilWrapper>
      </body>
    </html>
  )
}
