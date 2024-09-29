import axios from 'shared/api/axios'

export function getVideos() {
  return axios.get(`/api/v1/video`, {
    withCredentials: true,
  })
}

export function getVideo({ id }: { id: string | undefined }) {
  return axios.get(`/api/v1/video/${id}`, {
    withCredentials: true,
  })
}

export function sendVideo(name: string, file: File) {
  const formDate = new FormData()
  formDate.append('video', file)

  return axios.post(`/api/v1/video?name=${name}`, formDate, {
    withCredentials: true,
  })
}