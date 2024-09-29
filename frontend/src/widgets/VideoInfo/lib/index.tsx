import { useState, useMemo, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useToast } from '@chakra-ui/toast'
import { getVideo } from 'entities/video/api'
import { VideoData } from 'entities/video/types'
// import { reformatDate } from 'shared/lib/reformatDate/reformatDate'

export const useCurrentVideo = () => {
    const toast = useToast()
    const [videoData, setVideoData] = useState<VideoData>()
    const { id } = useParams()

    useEffect(() => {
        getVideo({id: id})
            .then(({ data }) => {
                setVideoData(data)
            })
            .catch(() => {
                toast({
                    position: 'bottom-right',
                    title: 'Ошибка',
                    description: 'Не удалось получить видео',
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                    variant: 'top-accent',
                })
            })
    }, [toast])

    const data = useMemo(() => {
        return {
            ...videoData,
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [videoData])

  return data
}
