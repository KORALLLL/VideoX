import { useRecentVideos } from '../lib'
import { Grid, Text, VideoCard } from 'shared/ui'

function AllVideo() {
    const data = useRecentVideos()

  return (
    <>
        {data && data.length != 0 ? (
            <Grid 
                templateColumns={'repeat(4, 1fr)'}
                columnGap={'40px'}
                rowGap={'40px'}
            >
                {data.map((item) => (
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
                fontSize={'20px'}
                align={'center'}
            >
                Здесь пока пусто
            </Text>
        )}
    </>
  )
}

export default AllVideo