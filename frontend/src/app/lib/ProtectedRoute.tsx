import { Flex } from '@chakra-ui/react'
import { getUserInfo } from 'entities/user/api'
import Loading from 'pages/loading'
import { ReactNode, useEffect, useState } from 'react'
import { useLocation, useMatch, useNavigate } from 'react-router-dom'
import { refresh as postRefresh } from 'shared/api/axios'
import { PageRoutes } from 'shared/config/pages'
import { AuthLayout } from 'shared/ui'
import { useUserStatusStore } from 'entities/user/model'
import { UserRole } from 'entities/user/types'

interface ProtectedRouteProps {
  children: ReactNode
  rolesPage?: Array<UserRole>
}

export const ProtectedRoute = ({
  children,
  rolesPage = ['patient'],
}: ProtectedRouteProps) => {
  const [isLoaded, setIsLoaded] = useState(false)
  const role = useUserStatusStore((state) => state.role)
  const setUserStatus = useUserStatusStore((state) => state.setUserStatus)
  const removeUserStatus = useUserStatusStore((state) => state.removeUserStatus)
  const setRecovery = useUserStatusStore((state) => state.setRecovery)
  const location = useLocation()
  const navigate = useNavigate()
  const isLogin = useMatch(PageRoutes.Login)
  const isRestorePassword = useMatch(PageRoutes.RestorePassword)

  const refresh = localStorage.getItem('refresh')
  useEffect(() => {
    if (isRestorePassword) {
      setRecovery(false)
    } else if (!refresh) {
      localStorage.removeItem('refresh')
      navigate(PageRoutes.Login)
      setIsLoaded(true)
    } else if (!isLoaded) {
      postRefresh(refresh)
        .then(({ data }) => {
          localStorage.setItem('refresh', data.refresh)
        })
        .catch(() => {
          localStorage.removeItem('refresh')
          navigate(PageRoutes.Login)
        })
        .finally(() => {
          setIsLoaded(true)
        })
      getUserInfo()
        .then(({ data }) => {
          setUserStatus(data.role)
        })
        .catch(() => {
          removeUserStatus()
        })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    refresh,
    navigate,
    isLoaded,
    setIsLoaded,
    setUserStatus,
    removeUserStatus,
  ])

  if (!(rolesPage.indexOf(role) != -1) && !isLogin) {
    navigate(PageRoutes.Page404)
  }

  if (!refresh || isLogin || isRestorePassword) {
    return (
      <AuthLayout key={location.pathname + location.hash}>
        {children}
      </AuthLayout>
    )
  } else {
    if (!isLoaded) return <Loading />

    return (
      <Flex
        key={location.pathname + location.hash}
        w="100%"
        h="100%"
        pl="137px"
        pb="30px"
        pr="43px"
      >
        {children}
      </Flex>
    )
  }
}
