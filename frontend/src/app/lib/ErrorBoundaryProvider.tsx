import { ErrorBoundary as ErrorCoreBoundary } from 'react-error-boundary'
import ReactErrorPage from 'pages/error-react'
import { ReactNode } from 'react'

export const ErrorBoundaryProvider = ({
  children,
}: {
  children: ReactNode
}) => (
  <ErrorCoreBoundary fallback={<ReactErrorPage />}>
    {children}
  </ErrorCoreBoundary>
)
