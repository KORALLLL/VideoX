import { ContainerPage } from 'shared/ui'
import AddFile from 'widgets/AddFile/ui'
import RecentVideo from 'widgets/RecentVideos/ui'

const MainPage = () => {
  return (
    <ContainerPage>
      <AddFile />
      <RecentVideo />
    </ContainerPage>
  )
}

export default MainPage
