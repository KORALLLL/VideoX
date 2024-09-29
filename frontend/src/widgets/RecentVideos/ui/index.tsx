import { useMatch } from 'react-router-dom'
import { PageRoutes } from 'shared/config/pages/PageRoutes'
import RecentVideo from './RecentVideo'
import RecentVideoAccordion from './RecentVideoAccordion'
import AllVideo from './AllVideo'

function RecentVideoWidget() {
    const isMain = useMatch(PageRoutes.Main)
    const isHistory = useMatch(PageRoutes.History)
    const isVideo = useMatch(PageRoutes.Video)

  return (
    <>
      {isMain && (<RecentVideo />)} 
      {isHistory && (<AllVideo />)}
      {isVideo && (<RecentVideoAccordion />)}
    </>
  )
}

export default RecentVideoWidget
