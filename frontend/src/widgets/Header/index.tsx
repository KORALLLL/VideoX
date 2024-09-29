import { Flex, Text } from 'shared/ui'
import { chakra } from '@chakra-ui/react'

function Header() {
  return (
    <Flex
      w={'100%'}
      p={'30px 40px'}
      alignItems={'center'}
    >
      <Text
        fontSize={'28px'}
        fontWeight={600}
      >
        Video<chakra.span color={'blue.100'}>X</chakra.span>
      </Text>
    </Flex>
  )
}

export { Header }
