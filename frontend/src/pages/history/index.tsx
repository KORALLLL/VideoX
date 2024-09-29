import { ContainerPage, Text } from 'shared/ui'
import RecentVideo from 'widgets/RecentVideos/ui'

const History = () => {
  return (
    <ContainerPage>
      <Text fontSize={'20px'} fontWeight={600} mb={'20px'}>Все проекты</Text>
      <RecentVideo />
    </ContainerPage>
  )
}

export default History
