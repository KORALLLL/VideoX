import { useNavigate } from 'react-router-dom'
import { Button, Heading, Stack, Text } from 'shared/ui'

const ReactError = () => {
  const navigate = useNavigate()
  return (
    <Stack gap="10px" align="center" my="auto" px="10px">
      <Heading as="h1" fontWeight={600} size="xl">
        Что-то пошло не так
      </Heading>
      <Text align="center" fontSize="20px">
        Наша команда уже в курсе возникшей проблемы, мы прилагаем
        <br />
        все усилия, чтобы решить ее в ближайшее время, спасибо за ваше терпение!
      </Text>
      <Button onClick={() => navigate('/home')}>Главная страница</Button>
    </Stack>
  )
}

export default ReactError
