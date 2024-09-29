import { useRecentVideos } from '../lib'
import { Flex, Grid, Text, VideoCard } from 'shared/ui'

function RecentVideo() {
    const data = useRecentVideos()

  return (
    <Flex
        w={'100%'}
        h={'40%'}
        flexDir={'column'}
        borderRadius={'10px'}
        gap={'10px'}
    >
        <Text fontSize={'14px'} fontWeight={600}>Недавно обработанные</Text>
        {data && data.length != 0 ? (
            <Grid 
                templateColumns={'repeat(4, 1fr)'}
                columnGap={'40px'}
            >
                {data.slice(0, 4).map((item) => (
                    <VideoCard
                        key={item.id}
                        id={item.id}
                        name={item.name}
                        date={item.created_at}
                        url={item.image_url}
                    />
                ))}
            </Grid>
        ) : (
            <Text
                fontSize={'14px'}
                align={'center'}
                mt={'20px'}
            >
                Здесь пока пусто
            </Text>
        )}
    </Flex>
  )
}

export default RecentVideo
