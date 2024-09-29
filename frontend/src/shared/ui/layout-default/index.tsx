import { Flex } from '@chakra-ui/react'
import { ReactNode } from 'react'

export const DefaultLayout = ({ children }: { children: ReactNode }) => (
  <Flex
    w="100%"
    h="100%"
    bg="gray.300"
    direction="column"
    position="relative"
    justifyContent="center"
  >
    {children}
  </Flex>
)
