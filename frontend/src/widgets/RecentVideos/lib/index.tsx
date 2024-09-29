import { useState, useMemo, useEffect } from 'react'
import { useToast } from '@chakra-ui/toast'
import { getVideos } from 'entities/video/api'
import { reformatDate } from 'shared/lib/reformatDate/reformatDate'

interface VideoItem {
    id: number,
    name: string,
    created_at: string,
    image_url: string
}

export const useRecentVideos = () => {
  const toast = useToast()
  const [videoList, setVideoList] = useState<VideoItem[]>([])

  useEffect(() => {
    getVideos()
      .then(({ data }) => {
        setVideoList(data.result)
      })
      .catch(() => {
        toast({
          position: 'bottom-right',
          title: 'Ошибка',
          description: 'Не удалось получить историю проектов',
          status: 'error',
          duration: 9000,
          isClosable: true,
          variant: 'top-accent',
        })
      })
  }, [toast])

  const data = useMemo(() => {
    return videoList.map((video) => ({
        ...video,
        created_at: reformatDate(video.created_at || '')
    }))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [videoList])

  return data
}
