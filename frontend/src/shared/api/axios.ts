import axios from 'axios'

const $api = axios.create({ withCredentials: true, responseType: 'json' })

/* ==$API with  response interceptors== */

$api.interceptors.response.use(
  (config) => config,
  async (error) => {
    const originalRequest = error.config
    if (
      error.response.status === 401 &&
      originalRequest &&
      !originalRequest._isRetry
    ) {
      originalRequest._isRetry = true
      try {
        return await $api.request(originalRequest)
      } catch (e) {
        // eslint-disable-next-line
        console.log(e)
      }
    }
    throw error
  }
)

export default $api