import {AspectRatio, Box, Button, Flex, Link, Text} from 'shared/ui'
import {Braces, Download} from 'shared/iconpack'
import {useCurrentVideo} from '../lib'

function VideoInfo() {
    const data = useCurrentVideo()

    return (
        <Flex w={'100%'} h={'100%'} flexDir={'column'} gap={'10px'}>
            <Flex justifyContent={'space-between'} alignItems={'center'}>
                <Text fontSize={'20px'} fontWeight={600}>{data?.name}</Text>
                <Flex gap={'14px'}>
                    <Link href={data.processed_video_url != "" ? data.processed_video_url : data.original_video_url}
                          download>
                        <Button
                            leftIcon={<Download/>}
                        >
                            Скачать видео
                        </Button>
                    </Link>
                    <Link href={`http://narl0durn01.fvds.ru/api/v1/video/${data.id}/json`} download>
                        <Button
                            leftIcon={<Braces/>}
                        >
                            Скачать json
                        </Button>
                    </Link>
                </Flex>
            </Flex>
            <Box>
                <AspectRatio
                    w={'100%'}
                    h={'470px'}
                >
                    <video
                        controls
                        autoPlay
                        muted
                        style={{
                            borderRadius: '10px',
                        }}
                    >
                        <source
                            src={data.processed_video_url != "" ? data.processed_video_url : data.original_video_url}
                            type="video/mp4"
                        />
                        <source
                            src={data.processed_video_url != "" ? data.processed_video_url : data.original_video_url}
                            type="video/quicktime"
                        />
                        Your browser does not support the video tag.
                    </video>
                </AspectRatio>
            </Box>
            <Text fontSize={'25px'}>
                Транскрибация
            </Text>
            <Text fontSize={'20px'}>
                {data.processed?.whisper_full.full_transcribation}
            </Text>
        </Flex>
    )
}

export default VideoInfo