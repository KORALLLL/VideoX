// import { useState, useMemo } from 'react'
import { useToast } from '@chakra-ui/react'
// import { AxiosResponse } from 'axios'
import { sendVideo } from 'entities/video/api'

// interface VideoData {
//   video: string | null
// }

interface UploadVideo {
  (name: string, file: File): void
}

interface VideoUploadResult {
  uploadVideo: UploadVideo
}

export const useVideoUpload = (): VideoUploadResult => {
  // const [video, setVideo] = useState<string | null>(null)
  const toast = useToast()

  const uploadVideo: UploadVideo = (name: string, file: File) => {
    if (file) {
      sendVideo(name, file)
        .then(() => {
          // const newAvatarUrl: string = response.data.image_url
          // setVideo(data)
          toast({
            position: 'bottom-right',
            title: 'Успех',
            description: 'Видео успешно отправлено',
            status: 'success',
            duration: 9000,
            isClosable: true,
            variant: 'top-accent',
          })
        })
        .catch(() => {
          toast({
            position: 'bottom-right',
            title: 'Ошибка',
            description: 'Не удалось загрузить видео',
            status: 'error',
            duration: 9000,
            isClosable: true,
            variant: 'top-accent',
          })
        })
    } else {
      toast({
        position: 'bottom-right',
        title: 'Ошибка',
        description: 'Нет файла для загрузки',
        status: 'error',
        duration: 9000,
        isClosable: true,
        variant: 'top-accent',
      })
    }
  }

  // const videoData: VideoData = useMemo(() => {
  //   return {
  //     video,
  //   }
  // }, [video])

  return {
    uploadVideo,
  }
}
