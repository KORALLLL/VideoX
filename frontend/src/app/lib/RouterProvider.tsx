import MainPage from 'pages/main-page'
import { ReactNode, Suspense } from 'react'
import { BrowserRouter } from 'react-router-dom'

interface RouterProviderProps {
  children: ReactNode
}

export const RouterProvider = ({ children }: RouterProviderProps) => (
  <BrowserRouter>
    <Suspense fallback={<MainPage />}>{children}</Suspense>
  </BrowserRouter>
)
