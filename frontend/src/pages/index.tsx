import { lazy } from 'react'
import { Route, Routes } from 'react-router-dom'

import { PageRoutes } from 'shared/config/pages/PageRoutes'
import { DefaultLayout } from 'shared/ui'
import { Menu, Header } from 'widgets/index'

const MainPage = lazy(() => import('./main-page'))
const History = lazy(() => import('./history'))
const VideoPage = lazy(() => import('./video-page'))
const Error404 = lazy(() => import('./error-404'))

export default function Routing() {
  return (
    <DefaultLayout>
      <Header />
      <Menu />
      <Routes>
        <Route path={PageRoutes.Page404} element={<Error404 />} />
        <Route
          path={PageRoutes.Main}
          element={
            <MainPage />
          }
        />
        <Route
          path={PageRoutes.History}
          element={
            <History />
          }
        />
        <Route
          path={PageRoutes.Video}
          element={
            <VideoPage />
          }
        />
      </Routes>
    </DefaultLayout>
  )
}
